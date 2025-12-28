# AURIX v4.0 - Enterprise Architecture Blueprint

## 📋 Overview

AURIX v4.0 mengadopsi **Clean Architecture** dengan modular design untuk:
- Maintainability & Scalability
- Testability 
- Separation of Concerns
- Plugin/Extension System

---

## 🏗️ Project Structure

```
aurix_v4/
├── 📁 app/                          # Main Application Layer
│   ├── __init__.py
│   ├── main.py                      # Streamlit entry point (minimal)
│   ├── config.py                    # Centralized configuration
│   └── constants.py                 # Application constants
│
├── 📁 core/                         # Core Business Logic (Domain Layer)
│   ├── __init__.py
│   ├── audit/                       # Audit domain
│   │   ├── __init__.py
│   │   ├── risk_calculator.py       # Risk assessment logic
│   │   ├── procedure_generator.py   # Audit procedure generation
│   │   ├── finding_manager.py       # Finding lifecycle management
│   │   └── kri_monitor.py           # Key Risk Indicators
│   │
│   ├── analytics/                   # Data Analytics domain
│   │   ├── __init__.py
│   │   ├── benford.py               # Benford's Law analysis
│   │   ├── outlier.py               # Outlier detection
│   │   ├── duplicate.py             # Duplicate detection
│   │   └── trend.py                 # Trend analysis
│   │
│   ├── fraud/                       # Fraud Detection domain
│   │   ├── __init__.py
│   │   ├── red_flags.py             # Red flag detection
│   │   ├── continuous_audit.py      # Continuous audit rules
│   │   └── alert_engine.py          # Alert generation
│   │
│   └── regulatory/                  # Regulatory domain
│       ├── __init__.py
│       ├── compliance.py            # Compliance checking
│       └── regulations.py           # Regulation database
│
├── 📁 infrastructure/               # Infrastructure Layer
│   ├── __init__.py
│   ├── database/                    # Database adapters
│   │   ├── __init__.py
│   │   ├── base.py                  # Abstract database interface
│   │   ├── postgres.py              # PostgreSQL implementation
│   │   └── sqlite.py                # SQLite fallback
│   │
│   ├── llm/                         # LLM Provider adapters
│   │   ├── __init__.py
│   │   ├── base.py                  # Abstract LLM interface
│   │   ├── groq_client.py           # Groq implementation
│   │   ├── together_client.py       # Together AI implementation
│   │   ├── google_client.py         # Google AI implementation
│   │   ├── openrouter_client.py     # OpenRouter implementation
│   │   └── mock_client.py           # Mock for testing
│   │
│   ├── rag/                         # RAG Engine
│   │   ├── __init__.py
│   │   ├── document_processor.py    # Document processing
│   │   ├── embeddings.py            # Embedding generation
│   │   ├── vector_store.py          # Vector storage
│   │   └── retriever.py             # Context retrieval
│   │
│   └── storage/                     # File storage
│       ├── __init__.py
│       ├── local.py                 # Local file storage
│       └── document_store.py        # Document management
│
├── 📁 services/                     # Application Services Layer
│   ├── __init__.py
│   ├── audit_service.py             # Audit orchestration
│   ├── analytics_service.py         # Analytics orchestration
│   ├── document_service.py          # Document management
│   ├── chat_service.py              # AI Chat service
│   └── visitor_service.py           # Visitor analytics
│
├── 📁 ui/                           # Presentation Layer (Streamlit)
│   ├── __init__.py
│   ├── components/                  # Reusable UI components
│   │   ├── __init__.py
│   │   ├── header.py                # Header component
│   │   ├── footer.py                # Footer component
│   │   ├── sidebar.py               # Sidebar component
│   │   ├── cards.py                 # Card components
│   │   ├── charts.py                # Chart components
│   │   ├── tables.py                # Table components
│   │   ├── forms.py                 # Form components
│   │   └── badges.py                # Badge components
│   │
│   ├── pages/                       # Page modules
│   │   ├── __init__.py
│   │   ├── dashboard.py             # Dashboard page
│   │   ├── documents.py             # Document management page
│   │   ├── ptcf_builder.py          # PTCF Builder page
│   │   ├── risk_assessment.py       # Risk assessment page
│   │   ├── audit_plan.py            # Audit planning page
│   │   ├── rag_search.py            # RAG search page
│   │   ├── procedures.py            # Procedures page
│   │   ├── regulations.py           # Regulations page
│   │   ├── ai_assistant.py          # AI Assistant page
│   │   ├── kri_monitor.py           # KRI Monitor page
│   │   ├── fraud_detection.py       # Fraud detection page
│   │   ├── data_analytics.py        # Data analytics page
│   │   ├── continuous_audit.py      # Continuous audit page
│   │   ├── findings_tracker.py      # Findings tracker page
│   │   ├── working_papers.py        # Working papers page
│   │   └── about.py                 # About page
│   │
│   ├── themes/                      # Theme management
│   │   ├── __init__.py
│   │   ├── base.py                  # Theme base class
│   │   ├── dark.py                  # Dark theme
│   │   └── light.py                 # Light theme
│   │
│   └── styles/                      # CSS management
│       ├── __init__.py
│       └── css_builder.py           # Dynamic CSS generation
│
├── 📁 data/                         # Data Layer
│   ├── __init__.py
│   ├── models/                      # Data models (Pydantic)
│   │   ├── __init__.py
│   │   ├── audit.py                 # Audit models
│   │   ├── document.py              # Document models
│   │   ├── finding.py               # Finding models
│   │   ├── risk.py                  # Risk models
│   │   └── user.py                  # User models
│   │
│   ├── repositories/                # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py                  # Repository interface
│   │   ├── finding_repo.py          # Finding repository
│   │   ├── document_repo.py         # Document repository
│   │   └── visitor_repo.py          # Visitor repository
│   │
│   └── seeds/                       # Seed data
│       ├── __init__.py
│       ├── regulations.py           # Regulation data
│       ├── audit_universe.py        # Audit universe data
│       ├── kri_indicators.py        # KRI data
│       ├── fraud_red_flags.py       # Fraud red flags data
│       └── ca_rules.py              # Continuous audit rules
│
├── 📁 utils/                        # Utility modules
│   ├── __init__.py
│   ├── logger.py                    # Logging configuration
│   ├── validators.py                # Input validation
│   ├── formatters.py                # Output formatting
│   ├── helpers.py                   # General helpers
│   └── exceptions.py                # Custom exceptions
│
├── 📁 tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── unit/                        # Unit tests
│   │   ├── core/
│   │   ├── services/
│   │   └── infrastructure/
│   ├── integration/                 # Integration tests
│   └── e2e/                         # End-to-end tests
│
├── 📁 scripts/                      # Utility scripts
│   ├── setup_db.py                  # Database setup
│   ├── migrate.py                   # Database migrations
│   └── seed_data.py                 # Data seeding
│
├── 📁 assets/                       # Static assets
│   ├── images/
│   ├── logos/
│   └── fonts/
│
├── 📁 docs/                         # Documentation
│   ├── ARCHITECTURE.md              # This file
│   ├── API.md                       # API documentation
│   ├── CONTRIBUTING.md              # Contribution guide
│   └── demo_files/                  # Demo files
│
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore
├── requirements.txt                 # Python dependencies
├── requirements-dev.txt             # Dev dependencies
├── pyproject.toml                   # Project configuration
├── Makefile                         # Build automation
└── README.md                        # Project README
```

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │Dashboard│  │Documents│  │Analytics│  │AI Chat  │  │Settings │           │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘           │
└───────┼────────────┼────────────┼────────────┼────────────┼─────────────────┘
        │            │            │            │            │
        ▼            ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SERVICES LAYER                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │AuditService  │  │DocService    │  │AnalyticsServ │  │ChatService   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────┘
          │                 │                 │                 │
          ▼                 ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             CORE LAYER                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Audit       │  │ Analytics   │  │ Fraud       │  │ Regulatory  │         │
│  │ Domain      │  │ Domain      │  │ Domain      │  │ Domain      │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INFRASTRUCTURE LAYER                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐                 │
│  │ Database  │  │ LLM       │  │ RAG       │  │ Storage   │                 │
│  │ Adapter   │  │ Providers │  │ Engine    │  │ Adapter   │                 │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘                 │
└─────────────────────────────────────────────────────────────────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
    ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
    │PostgreSQL │    │Groq/Google│    │ChromaDB   │    │Filesystem │
    │  Neon     │    │/Together  │    │/FAISS     │    │           │
    └───────────┘    └───────────┘    └───────────┘    └───────────┘
```

---

## 🔑 Key Design Patterns

### 1. Dependency Injection
```python
# Services receive dependencies through constructor
class AuditService:
    def __init__(
        self,
        risk_calculator: RiskCalculator,
        llm_client: BaseLLMClient,
        finding_repo: FindingRepository
    ):
        self.risk_calculator = risk_calculator
        self.llm_client = llm_client
        self.finding_repo = finding_repo
```

### 2. Repository Pattern
```python
# Abstract data access from business logic
class FindingRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Finding]: ...
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Finding]: ...
    
    @abstractmethod
    def save(self, finding: Finding) -> Finding: ...
```

### 3. Strategy Pattern (LLM Providers)
```python
# Interchangeable LLM providers
class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> LLMResponse: ...

class GroqClient(BaseLLMClient): ...
class GoogleClient(BaseLLMClient): ...
class MockClient(BaseLLMClient): ...
```

### 4. Factory Pattern
```python
# Create instances based on configuration
def create_llm_client(config: LLMConfig) -> BaseLLMClient:
    providers = {
        "groq": GroqClient,
        "google": GoogleClient,
        "mock": MockClient
    }
    return providers[config.provider](config)
```

---

## ⚙️ Configuration Management

### Environment Variables
```bash
# .env
# Database
DATABASE_URL=postgresql://...
DATABASE_POOL_SIZE=10

# LLM Providers (pick one or more)
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=AIza...
TOGETHER_API_KEY=...

# Application
APP_ENV=production
LOG_LEVEL=INFO
SECRET_KEY=...
```

### Configuration Classes
```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = ""
    database_pool_size: int = 10
    
    # LLM
    default_llm_provider: str = "groq"
    groq_api_key: str = ""
    google_api_key: str = ""
    
    # App
    app_env: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
```

---

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/unit/core/test_risk_calculator.py
def test_calculate_risk_high():
    calculator = RiskCalculator()
    result = calculator.calculate(
        inherent={"complexity": 0.9, "volume": 0.8},
        control={"effectiveness": 0.3}
    )
    assert result.level == RiskLevel.HIGH
```

### Integration Tests
```python
# tests/integration/test_audit_service.py
def test_create_finding_with_db(db_session):
    service = AuditService(...)
    finding = service.create_finding(FindingCreate(...))
    assert finding.id is not None
```

---

## 🚀 Deployment

### Docker Support
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app/main.py"]
```

### CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest tests/
```

---

## 📊 Benefits

| Aspect | Before (v3) | After (v4) |
|--------|-------------|------------|
| Maintainability | 3000+ lines in 1 file | Modular, ~100-200 lines/file |
| Testability | Difficult | Easy unit/integration tests |
| Extensibility | Hard to add features | Plugin system ready |
| Team Collaboration | Merge conflicts | Independent modules |
| Code Reuse | Copy-paste | Shared components |
| Configuration | Scattered | Centralized |
| Error Handling | Inconsistent | Standardized |

---

## 🔜 Migration Path

1. **Phase 1**: Create new structure, migrate core logic
2. **Phase 2**: Migrate UI components
3. **Phase 3**: Add testing suite
4. **Phase 4**: CI/CD setup
5. **Phase 5**: Documentation

---

*AURIX v4.0 - Enterprise Architecture for Scalable Audit Intelligence*
