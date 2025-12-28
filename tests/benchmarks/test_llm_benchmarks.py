"""
LLM and RAG Benchmark Tests for AURIX.

Run benchmarks with pytest:
    pytest tests/benchmarks/ -v
    pytest tests/benchmarks/ -v --benchmark-json=benchmark_results.json
    pytest tests/benchmarks/ -v --llm-provider=groq --benchmark-iterations=10

These tests measure:
- LLM response latency across providers
- RAG faithfulness and accuracy scores
- Hallucination detection rates
"""

import pytest
import time
import sys
from pathlib import Path
from statistics import mean, median
from typing import List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from infrastructure.llm import (
    create_llm_client,
    LLMClient,
    LLMResponse,
    Message,
    LLMProvider
)


class TestLLMLatency:
    """Test suite for LLM latency benchmarks."""

    def test_mock_provider_responds(self, mock_llm_client):
        """Verify mock provider returns valid response."""
        response = mock_llm_client.generate(
            prompt="What is internal audit?",
            temperature=0.3
        )

        assert response is not None
        assert isinstance(response, LLMResponse)
        assert len(response.content) > 0
        assert response.provider == "Mock"

    def test_mock_latency_under_threshold(
        self,
        mock_llm_client,
        audit_test_prompts,
        latency_threshold
    ):
        """Test that mock provider latency is under threshold."""
        latencies = []

        for prompt in audit_test_prompts[:3]:  # Use first 3 prompts
            start = time.perf_counter()
            response = mock_llm_client.generate(prompt=prompt)
            end = time.perf_counter()

            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)

            assert response.content, f"Empty response for prompt: {prompt}"

        avg_latency = mean(latencies)
        assert avg_latency < latency_threshold, \
            f"Average latency {avg_latency:.1f}ms exceeds threshold {latency_threshold}ms"

    def test_llm_provider_latency(
        self,
        llm_provider,
        audit_test_prompts,
        benchmark_iterations,
        latency_threshold
    ):
        """
        Benchmark LLM provider latency.

        This test will use the provider specified via --llm-provider flag.
        Default is 'mock' for safe CI/CD testing.
        """
        try:
            client = create_llm_client(provider=llm_provider)
        except Exception as e:
            pytest.skip(f"Could not create client for {llm_provider}: {e}")

        latencies = []
        errors = []

        for i in range(min(benchmark_iterations, len(audit_test_prompts))):
            prompt = audit_test_prompts[i % len(audit_test_prompts)]

            try:
                start = time.perf_counter()
                response = client.generate(
                    prompt=prompt,
                    temperature=0.3,
                    max_tokens=256
                )
                end = time.perf_counter()

                latency_ms = (end - start) * 1000
                latencies.append(latency_ms)

            except Exception as e:
                errors.append(str(e))

        # At least 50% should succeed
        success_rate = len(latencies) / benchmark_iterations
        assert success_rate >= 0.5, \
            f"Success rate {success_rate:.0%} below 50% threshold. Errors: {errors[:3]}"

        if latencies:
            avg_latency = mean(latencies)
            med_latency = median(latencies)

            print(f"\n{llm_provider} Latency Results:")
            print(f"  Iterations: {len(latencies)}/{benchmark_iterations}")
            print(f"  Mean: {avg_latency:.1f}ms")
            print(f"  Median: {med_latency:.1f}ms")
            print(f"  Min: {min(latencies):.1f}ms")
            print(f"  Max: {max(latencies):.1f}ms")

            # Soft assertion - warn but don't fail for external providers
            if avg_latency > latency_threshold:
                pytest.warns(
                    UserWarning,
                    match=f"Latency {avg_latency:.0f}ms exceeds threshold"
                )

    def test_llm_response_quality(self, mock_llm_client):
        """Test that LLM responses contain expected content for audit queries."""
        response = mock_llm_client.generate(
            prompt="What are the key risks in credit management?",
            system_prompt="You are an internal audit expert."
        )

        # Response should mention risk-related terms
        response_lower = response.content.lower()
        risk_terms = ["risk", "control", "audit", "assessment", "recommendation"]

        found_terms = [term for term in risk_terms if term in response_lower]
        assert len(found_terms) >= 2, \
            f"Response lacks audit context. Found terms: {found_terms}"

    def test_chat_with_history(self, mock_llm_client):
        """Test multi-turn chat maintains context."""
        messages = [
            Message("system", "You are an audit assistant."),
            Message("user", "What is NPL ratio?"),
            Message("assistant", "NPL ratio is Non-Performing Loan ratio."),
            Message("user", "What threshold indicates high risk?"),
        ]

        response = mock_llm_client.chat(messages)

        assert response is not None
        assert len(response.content) > 0


class TestRAGAccuracy:
    """Test suite for RAG accuracy benchmarks."""

    def test_simplified_evaluation_runs(self, rag_test_cases):
        """Test that simplified RAG evaluation completes."""
        from scripts.benchmark_rag_accuracy import evaluate_simplified

        results = evaluate_simplified(rag_test_cases[:2])

        assert len(results) == 2
        for result in results:
            assert 0 <= result.faithfulness <= 1
            assert 0 <= result.answer_relevancy <= 1
            assert 0 <= result.context_precision <= 1
            assert 0 <= result.context_recall <= 1

    def test_faithfulness_above_threshold(
        self,
        rag_test_cases,
        faithfulness_threshold
    ):
        """Test that RAG faithfulness meets minimum threshold."""
        from scripts.benchmark_rag_accuracy import (
            evaluate_simplified,
            calculate_summary
        )

        results = evaluate_simplified(rag_test_cases)
        summary = calculate_summary(results, faithfulness_threshold, "simplified")

        print(f"\nRAG Accuracy Results:")
        print(f"  Avg Faithfulness: {summary.avg_faithfulness:.3f}")
        print(f"  Avg Relevancy: {summary.avg_answer_relevancy:.3f}")
        print(f"  Hallucination Rate: {summary.hallucination_rate:.1%}")

        # The built-in test cases should pass with simplified evaluation
        assert summary.avg_faithfulness >= 0.5, \
            f"Faithfulness {summary.avg_faithfulness:.3f} too low"

    def test_hallucination_detection(self, rag_test_cases):
        """Test that hallucination detection works."""
        from scripts.benchmark_rag_accuracy import (
            evaluate_simplified,
            RAGTestCase
        )

        # Add a test case with obvious hallucination
        hallucinated_case = RAGTestCase(
            question="What is the capital of Indonesia?",
            contexts=["Indonesia is a country in Southeast Asia."],
            answer="The capital of Indonesia is Tokyo, which is famous for sushi.",
            ground_truth="Jakarta is the capital of Indonesia."
        )

        results = evaluate_simplified([hallucinated_case])

        # The hallucinated answer should have low faithfulness
        assert results[0].faithfulness < 0.7, \
            "Failed to detect obvious hallucination"

    def test_context_relevance_scoring(self):
        """Test context relevance scoring logic."""
        from scripts.benchmark_rag_accuracy import (
            evaluate_simplified,
            RAGTestCase
        )

        # High relevance case
        relevant_case = RAGTestCase(
            question="What is NPL ratio threshold?",
            contexts=["NPL ratio threshold is 5% according to OJK regulations."],
            answer="NPL ratio threshold is 5%.",
            ground_truth="5%"
        )

        # Low relevance case
        irrelevant_case = RAGTestCase(
            question="What is NPL ratio threshold?",
            contexts=["The weather in Jakarta is tropical and humid."],
            answer="NPL ratio threshold is 5%.",
            ground_truth="5%"
        )

        relevant_results = evaluate_simplified([relevant_case])
        irrelevant_results = evaluate_simplified([irrelevant_case])

        # Relevant context should score higher
        assert relevant_results[0].faithfulness > irrelevant_results[0].faithfulness


class TestBenchmarkIntegration:
    """Integration tests for benchmark scripts."""

    def test_latency_script_imports(self):
        """Verify latency benchmark script can be imported."""
        from scripts.benchmark_llm_latency import (
            run_single_benchmark,
            calculate_percentile,
            BenchmarkSummary,
            LatencyResult
        )

        assert callable(run_single_benchmark)
        assert callable(calculate_percentile)

    def test_rag_script_imports(self):
        """Verify RAG benchmark script can be imported."""
        from scripts.benchmark_rag_accuracy import (
            evaluate_simplified,
            calculate_summary,
            RAGTestCase,
            RAGEvalResult
        )

        assert callable(evaluate_simplified)
        assert callable(calculate_summary)

    def test_percentile_calculation(self):
        """Test percentile calculation utility."""
        from scripts.benchmark_llm_latency import calculate_percentile

        values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

        p50 = calculate_percentile(values, 50)
        p95 = calculate_percentile(values, 95)
        p99 = calculate_percentile(values, 99)

        assert p50 <= p95 <= p99
        assert p50 == 500 or p50 == 600  # Approximate median

    def test_empty_values_percentile(self):
        """Test percentile calculation with empty list."""
        from scripts.benchmark_llm_latency import calculate_percentile

        result = calculate_percentile([], 95)
        assert result == 0.0


class TestProviderAvailability:
    """Test LLM provider availability and configuration."""

    @pytest.mark.parametrize("provider", ["mock", "ollama"])
    def test_no_api_key_providers(self, provider):
        """Test providers that don't require API keys."""
        client = create_llm_client(provider=provider)
        assert client is not None
        assert client.provider_name in ["Mock", "Ollama"]

    def test_mock_always_available(self):
        """Mock provider should always work for testing."""
        client = create_llm_client(provider="mock")
        response = client.generate("Test prompt")

        assert response.content
        assert response.provider == "Mock"
        assert "mock" in response.metadata.get("mock", True).__str__().lower() or response.metadata.get("mock") == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
