# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AURIX (AUdit Risk Intelligence eXcellence) is an AI-powered Internal Audit platform for Indonesian financial industry. It's a Python/Streamlit application (v4.2 Excellence 2026) with 26+ audit modules including Process Mining, Regulatory RAG, KRI Dashboard, and fraud detection.

## Common Commands

```bash
# Run the application
streamlit run streamlit_app.py

# Install dependencies
pip install -r requirements.txt

# Install Graphviz (required for Process Mining DFG visualization)
# Windows: choco install graphviz
# macOS: brew install graphviz
# Ubuntu: sudo apt-get install graphviz

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html

# Run a single test file
pytest tests/test_basic.py -v

# Format code
black .
isort .

# Type checking
mypy .

# Docker build and run
docker build -t aurix:2026 .
docker run -p 8501:8501 aurix:2026

# Benchmarking: Measure LLM latency and RAG accuracy
pytest tests/benchmarks/ -v --benchmark-json=benchmark_results.json
python scripts/benchmark_llm_latency.py --provider groq --iterations 100
python scripts/benchmark_rag_accuracy.py --eval-framework ragas --output reports/

# Schema validation check
python -m mypy data/models/ --strict
```

## Development Guidelines

### Benchmarking

Run LLM latency and RAG accuracy benchmarks periodically to detect performance regressions:
- Use G-Eval or RAGAS framework for RAG hallucination detection
- Track latency metrics per LLM provider in `benchmark_results.json`
- Set baseline thresholds: LLM response < 3s, RAG faithfulness > 0.85

### Schema Enforcement

All new data models MUST use Pydantic with strict validation to prevent data drift on KRI dashboard:
```python
from pydantic import BaseModel, Field, field_validator

class KRIMetric(BaseModel):
    model_config = {"strict": True}

    metric_id: str = Field(..., min_length=1)
    value: float = Field(..., ge=0)
    threshold: float = Field(..., ge=0)

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError("metric_id must be valid identifier")
        return v
```

## Architecture

The codebase follows Clean Architecture with modular design:

```
app/           - Application layer (config, router, constants, entry point)
ui/            - Presentation layer (Streamlit pages and components)
  pages/       - 26+ page modules (dashboard, kri_dashboard, process_mining, etc.)
  components/  - Reusable UI components (sidebar, floating_copilot, active_kri_card)
  styles/      - CSS builder for dynamic theming
modules/       - 2026 feature modules (process_mining.py, regulatory_rag.py)
infrastructure/
  llm/         - LLM provider adapters (Strategy pattern: Groq, Together, Google, OpenRouter, Ollama, Mock)
  database/    - Database adapters
  rag/         - RAG engine for document retrieval
services/      - Application services (audit_service, visitor_service)
data/
  models/      - Pydantic data models
  seeds/       - Seed data (regulations, KRI indicators, audit universe, fraud red flags)
utils/         - Logger, exceptions, helpers
tests/         - Test suite
```

### Key Design Patterns

1. **Strategy Pattern**: LLM providers in `infrastructure/llm/__init__.py` - `LLMStrategy` base class with implementations for each provider (GroqStrategy, GoogleStrategy, etc.)

2. **Router Pattern**: `app/router.py` - `Router` class maps page names to render functions, organizes pages into categories

3. **Pydantic Settings**: `app/config.py` - Hierarchical configuration (AppSettings, LLMSettings, DatabaseSettings, RAGSettings, AuditSettings)

### Data Flow

```
UI Pages → Services → Core Logic → Infrastructure (LLM/DB/RAG)
```

### Adding a New Page

1. Create module in `ui/pages/new_page.py` with a `render()` function
2. Import in `app/router.py`
3. Add to `self.routes` dict and appropriate category in `self.page_categories`

### Adding a New LLM Provider

1. Create strategy class extending `LLMStrategy` in `infrastructure/llm/__init__.py`
2. Add to `LLMClient.STRATEGIES` dict
3. Add provider info to `LLM_PROVIDER_INFO`

## Configuration

Environment variables loaded via `.env` file:

- `GROQ_API_KEY`, `TOGETHER_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY` - LLM API keys
- `NEON_HOST`, `NEON_DATABASE`, `NEON_USER`, `NEON_PASSWORD` - PostgreSQL (Neon) database
- `LLM_PROVIDER` - Default LLM provider (defaults to "mock" for demo mode)
- `APP_ENV` - Environment (development/staging/production)

## Indonesian Financial Context

This platform is designed for Indonesian banking/financial audit with:
- OJK (Financial Services Authority), BI (Bank Indonesia), BPKH regulations
- Indonesian banking KRI thresholds (NPL, LDR, CAR, RoR ratios)
- POJK 6/2022 ESG Taxonomy (Green/Brown/Transition classification)
- Sharia compliance validation

## Session State

Streamlit session state initialized in `app/config.py:init_app()` with keys: `theme`, `documents`, `chat_history`, `risk_assessments`, `kri_data`, `findings`, `current_page`, etc.
