#!/usr/bin/env python3
"""
LLM Latency Benchmark Script for AURIX.

Measures response latency across different LLM providers to detect performance regressions.

Usage:
    python scripts/benchmark_llm_latency.py --provider groq --iterations 100
    python scripts/benchmark_llm_latency.py --all-providers --iterations 50
    python scripts/benchmark_llm_latency.py --provider google --output reports/latency_report.json
"""

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from statistics import mean, median, stdev

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from infrastructure.llm import (
    LLMProvider,
    LLMConfig,
    LLMClient,
    create_llm_client,
    Message,
    LLM_PROVIDER_INFO
)


@dataclass
class LatencyResult:
    """Single latency measurement result."""
    provider: str
    model: str
    iteration: int
    latency_ms: float
    tokens_used: int
    success: bool
    error: Optional[str] = None


@dataclass
class BenchmarkSummary:
    """Summary statistics for a provider benchmark."""
    provider: str
    model: str
    total_iterations: int
    successful_iterations: int
    failed_iterations: int
    min_latency_ms: float
    max_latency_ms: float
    mean_latency_ms: float
    median_latency_ms: float
    std_dev_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    avg_tokens: float
    total_time_seconds: float
    timestamp: str


# Standard test prompts for consistent benchmarking
TEST_PROMPTS = [
    "What are the key risk indicators for credit risk in banking?",
    "Explain the difference between inherent risk and residual risk.",
    "List 5 common audit procedures for testing internal controls.",
    "What is the purpose of Benford's Law in fraud detection?",
    "Describe the three lines of defense model in risk management.",
]

# System prompt for audit context
AUDIT_SYSTEM_PROMPT = """You are an expert internal auditor specializing in Indonesian banking regulations.
Provide concise, professional responses focused on audit methodology and risk assessment."""


def get_available_providers() -> List[str]:
    """Get list of providers with configured API keys."""
    available = []

    env_keys = {
        "groq": "GROQ_API_KEY",
        "together": "TOGETHER_API_KEY",
        "google": "GOOGLE_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
    }

    for provider, env_var in env_keys.items():
        if os.getenv(env_var):
            available.append(provider)

    # Mock and Ollama don't need API keys
    available.extend(["mock", "ollama"])

    return available


def run_single_benchmark(
    client: LLMClient,
    prompt: str,
    iteration: int
) -> LatencyResult:
    """Run a single benchmark iteration."""
    try:
        start_time = time.perf_counter()

        response = client.generate(
            prompt=prompt,
            system_prompt=AUDIT_SYSTEM_PROMPT,
            temperature=0.3,
            max_tokens=512
        )

        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000

        return LatencyResult(
            provider=client.provider_name,
            model=client.config.get_model(),
            iteration=iteration,
            latency_ms=latency_ms,
            tokens_used=response.tokens_used,
            success=True
        )

    except Exception as e:
        return LatencyResult(
            provider=client.provider_name,
            model=client.config.get_model(),
            iteration=iteration,
            latency_ms=0,
            tokens_used=0,
            success=False,
            error=str(e)
        )


def calculate_percentile(values: List[float], percentile: float) -> float:
    """Calculate percentile value from list."""
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = int(len(sorted_values) * percentile / 100)
    return sorted_values[min(index, len(sorted_values) - 1)]


def run_provider_benchmark(
    provider: str,
    iterations: int,
    verbose: bool = True
) -> BenchmarkSummary:
    """Run benchmark for a single provider."""

    if verbose:
        print(f"\n{'='*60}")
        print(f"Benchmarking: {provider.upper()}")
        print(f"{'='*60}")

    # Create client
    try:
        client = create_llm_client(provider=provider)
    except Exception as e:
        print(f"Error creating client for {provider}: {e}")
        return None

    results: List[LatencyResult] = []
    start_time = time.time()

    for i in range(iterations):
        # Cycle through test prompts
        prompt = TEST_PROMPTS[i % len(TEST_PROMPTS)]

        result = run_single_benchmark(client, prompt, i + 1)
        results.append(result)

        if verbose:
            status = "OK" if result.success else f"FAIL: {result.error}"
            print(f"  Iteration {i+1}/{iterations}: {result.latency_ms:.1f}ms - {status}")

    total_time = time.time() - start_time

    # Calculate statistics
    successful_latencies = [r.latency_ms for r in results if r.success]
    successful_tokens = [r.tokens_used for r in results if r.success]

    if not successful_latencies:
        print(f"  WARNING: No successful iterations for {provider}")
        return None

    summary = BenchmarkSummary(
        provider=provider,
        model=client.config.get_model(),
        total_iterations=iterations,
        successful_iterations=len(successful_latencies),
        failed_iterations=iterations - len(successful_latencies),
        min_latency_ms=min(successful_latencies),
        max_latency_ms=max(successful_latencies),
        mean_latency_ms=mean(successful_latencies),
        median_latency_ms=median(successful_latencies),
        std_dev_ms=stdev(successful_latencies) if len(successful_latencies) > 1 else 0,
        p95_latency_ms=calculate_percentile(successful_latencies, 95),
        p99_latency_ms=calculate_percentile(successful_latencies, 99),
        avg_tokens=mean(successful_tokens) if successful_tokens else 0,
        total_time_seconds=total_time,
        timestamp=datetime.now().isoformat()
    )

    if verbose:
        print(f"\n  Summary for {provider}:")
        print(f"    Success Rate: {summary.successful_iterations}/{summary.total_iterations}")
        print(f"    Mean Latency: {summary.mean_latency_ms:.1f}ms")
        print(f"    Median Latency: {summary.median_latency_ms:.1f}ms")
        print(f"    P95 Latency: {summary.p95_latency_ms:.1f}ms")
        print(f"    P99 Latency: {summary.p99_latency_ms:.1f}ms")

    return summary


def check_thresholds(summaries: List[BenchmarkSummary], threshold_ms: float = 3000) -> bool:
    """Check if latencies are within acceptable thresholds."""
    all_passed = True

    print(f"\n{'='*60}")
    print("Threshold Check (target: < {:.0f}ms mean latency)".format(threshold_ms))
    print(f"{'='*60}")

    for summary in summaries:
        if summary is None:
            continue

        passed = summary.mean_latency_ms < threshold_ms
        status = "PASS" if passed else "FAIL"

        print(f"  {summary.provider}: {summary.mean_latency_ms:.1f}ms - {status}")

        if not passed:
            all_passed = False

    return all_passed


def save_results(
    summaries: List[BenchmarkSummary],
    output_path: str
):
    """Save benchmark results to JSON file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    results = {
        "benchmark_type": "llm_latency",
        "timestamp": datetime.now().isoformat(),
        "results": [asdict(s) for s in summaries if s is not None]
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark LLM provider latency for AURIX"
    )
    parser.add_argument(
        "--provider", "-p",
        type=str,
        help="LLM provider to benchmark (groq, together, google, openrouter, ollama, mock)"
    )
    parser.add_argument(
        "--all-providers", "-a",
        action="store_true",
        help="Benchmark all available providers"
    )
    parser.add_argument(
        "--iterations", "-n",
        type=int,
        default=10,
        help="Number of iterations per provider (default: 10)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="reports/llm_latency_benchmark.json",
        help="Output file path for results"
    )
    parser.add_argument(
        "--threshold", "-t",
        type=float,
        default=3000,
        help="Latency threshold in ms (default: 3000)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress verbose output"
    )

    args = parser.parse_args()

    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    print("AURIX LLM Latency Benchmark")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Determine providers to benchmark
    if args.all_providers:
        providers = get_available_providers()
        print(f"Benchmarking all available providers: {providers}")
    elif args.provider:
        providers = [args.provider]
    else:
        providers = ["mock"]  # Default to mock for safe testing
        print("No provider specified, using mock provider")

    # Run benchmarks
    summaries = []
    for provider in providers:
        summary = run_provider_benchmark(
            provider=provider,
            iterations=args.iterations,
            verbose=not args.quiet
        )
        if summary:
            summaries.append(summary)

    # Check thresholds
    if summaries:
        passed = check_thresholds(summaries, args.threshold)

        # Save results
        save_results(summaries, args.output)

        # Exit code based on threshold check
        sys.exit(0 if passed else 1)
    else:
        print("No successful benchmarks completed")
        sys.exit(1)


if __name__ == "__main__":
    main()
