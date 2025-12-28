"""
Pytest configuration for benchmark tests.

Fixtures and configuration for LLM/RAG benchmarking.
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def pytest_addoption(parser):
    """Add custom command line options for benchmarks."""
    parser.addoption(
        "--llm-provider",
        action="store",
        default="mock",
        help="LLM provider to use for benchmarks (default: mock)"
    )
    parser.addoption(
        "--benchmark-iterations",
        action="store",
        default=5,
        type=int,
        help="Number of iterations for latency benchmarks (default: 5)"
    )
    parser.addoption(
        "--latency-threshold",
        action="store",
        default=3000,
        type=float,
        help="Maximum acceptable latency in ms (default: 3000)"
    )
    parser.addoption(
        "--faithfulness-threshold",
        action="store",
        default=0.85,
        type=float,
        help="Minimum acceptable faithfulness score (default: 0.85)"
    )


@pytest.fixture
def llm_provider(request):
    """Get LLM provider from command line or environment."""
    cli_provider = request.config.getoption("--llm-provider")
    env_provider = os.getenv("BENCHMARK_LLM_PROVIDER")
    return env_provider or cli_provider


@pytest.fixture
def benchmark_iterations(request):
    """Get number of benchmark iterations."""
    return request.config.getoption("--benchmark-iterations")


@pytest.fixture
def latency_threshold(request):
    """Get latency threshold in ms."""
    return request.config.getoption("--latency-threshold")


@pytest.fixture
def faithfulness_threshold(request):
    """Get faithfulness threshold."""
    return request.config.getoption("--faithfulness-threshold")


@pytest.fixture
def mock_llm_client():
    """Create a mock LLM client for testing."""
    from infrastructure.llm import create_llm_client
    return create_llm_client(provider="mock")


@pytest.fixture
def audit_test_prompts():
    """Standard audit test prompts for benchmarking."""
    return [
        "What are the key risk indicators for credit risk in banking?",
        "Explain the difference between inherent risk and residual risk.",
        "List 5 common audit procedures for testing internal controls.",
        "What is the purpose of Benford's Law in fraud detection?",
        "Describe the three lines of defense model in risk management.",
    ]


@pytest.fixture
def rag_test_cases():
    """RAG test cases for accuracy benchmarking."""
    from scripts.benchmark_rag_accuracy import AUDIT_TEST_CASES
    return AUDIT_TEST_CASES
