# 🛡️ AURIX Excellence 2026

**AUdit Risk Intelligence eXcellence** - Agentic Audit Platform for Indonesian Financial Industry

[![Version](https://img.shields.io/badge/version-4.2%20Excellence%202026-blue.svg)](https://github.com/mshadianto/aurix)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red.svg)](https://streamlit.io)

---

## 🆕 What's New in 2026 Excellence

### 1. 🏛️ Executive Dashboard (NEW)
- **5-Second Rule KPI Scorecard** - Dominant visual hierarchy for instant comprehension
- **So-What Auto-Narrative** - AI-generated strategic insights explaining business impact
- **Flight Simulator** - What-if scenario analysis for proactive decision making
- **Data Lineage Transparency** - Source system, quality score, refresh frequency
- **Executive Report Export** - PowerPoint, PDF, Excel, Email formats

### 2. 🎯 Grouped Navigation + Floating AI Copilot
- **Grouped sidebar navigation** - Organized into Core Audit, Intelligence, Labs, Admin
- **Floating Action Button (FAB)** - Persistent AI Copilot accessible from any page
- **Contextual suggestions** - AI adapts recommendations based on current page

### 3. ⚡ Active KRI Cards with AI Analysis
- **Smart metric cards** - Visual status indicators (Normal/Warning/Danger)
- **One-click AI analysis** - Automatic root cause identification when thresholds breached
- **Modal dialog** - Shows root causes, severity ratings, evidence, and recommendations

### 4. 🔄 Process Mining
- **Automated process discovery** - Upload event logs, get DFG visualization
- **Bottleneck detection** - Identifies process inefficiencies automatically
- **Process variants analysis** - Compare different execution paths

### 5. 📜 Regulatory RAG
- **Indonesian regulations** - OJK, BI, BPKH compliance validation
- **ESG Taxonomy** - POJK 6/2022 green/brown/transition classification
- **Sharia compliance** - BPKH haram activity detection

### 6. 📊 Benchmarking & Quality Assurance (NEW)
- **LLM Latency Benchmarks** - Measure response times across providers
- **RAG Accuracy Evaluation** - RAGAS/G-Eval framework for hallucination detection
- **Pydantic Schema Enforcement** - Strict validation to prevent data drift

---

## 🚀 Quick Start

### Installation

```bash
# Clone or extract the project
cd aurix_integrated

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Graphviz (required for Process Mining)
# macOS: brew install graphviz
# Ubuntu: sudo apt-get install graphviz
# Windows: choco install graphviz

# Run the application
streamlit run streamlit_app.py
```

### Environment Configuration

Create `.env` file from example:

```bash
cp .env.example .env
```

Configure your LLM API keys (optional for demo mode):

```env
GROQ_API_KEY=your_groq_key
TOGETHER_API_KEY=your_together_key
GOOGLE_API_KEY=your_google_key
OPENAI_API_KEY=your_openai_key
```

---

## 📁 Project Structure

```
aurix_integrated/
├── streamlit_app.py          # Main entry point
├── app/
│   ├── config.py             # Pydantic configuration
│   ├── constants.py          # App constants
│   ├── main.py               # App initialization
│   └── router.py             # Page routing (updated for 2026)
├── modules/                  # 🆕 2026 Modules
│   ├── __init__.py
│   ├── process_mining.py     # DFG, bottleneck detection
│   └── regulatory_rag.py     # OJK/BI/BPKH compliance
├── ui/
│   ├── components/
│   │   ├── sidebar.py        # 🆕 Grouped navigation
│   │   ├── active_kri_card.py # 🆕 AI analysis trigger
│   │   ├── floating_copilot.py # 🆕 FAB chat
│   │   ├── executive.py      # 🆕 Executive-grade components
│   │   └── badges.py
│   ├── pages/
│   │   ├── dashboard.py
│   │   ├── executive_dashboard.py # 🆕 Executive Dashboard
│   │   ├── kri_dashboard.py  # 🆕 Active cards
│   │   ├── process_mining.py # 🆕 New page
│   │   ├── regulatory_rag.py # 🆕 New page
│   │   └── ...               # 26+ existing pages
│   └── styles/
│       └── css_builder.py
├── scripts/                   # 🆕 Utility scripts
│   ├── benchmark_llm_latency.py  # LLM performance benchmarks
│   └── benchmark_rag_accuracy.py # RAG quality evaluation
├── data/
│   ├── models/
│   └── seeds/
├── services/
│   ├── audit_service.py
│   └── visitor_service.py
├── infrastructure/
│   ├── database/
│   ├── llm/
│   └── rag/
├── utils/
│   ├── logger.py
│   └── exceptions.py
├── docs/
│   ├── USER_MANUAL.md
│   └── ARCHITECTURE.md
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🎯 Features Overview

### Core Audit
| Feature | Description |
|---------|-------------|
| 📊 Dashboard | Executive overview with key metrics |
| 🏛️ Executive Dashboard | **5-Second Rule KPI + So-What Narratives + Flight Simulator** |
| 🎛️ Command Center | Mission control for audit activities |
| 📁 Documents | Document management with RAG |
| 🎭 PTCF Builder | Process/Transaction Control Framework |
| ⚖️ Risk Assessment | Risk scoring and evaluation |
| 📋 Findings Tracker | Audit finding management (CCCE) |
| 📝 Workpapers | Audit documentation |

### Intelligence (2026)
| Feature | Description |
|---------|-------------|
| 📈 KRI Dashboard | **Active cards with AI analysis** |
| 🔄 Process Mining | **DFG visualization, bottleneck detection** |
| 📜 Regulatory RAG | **OJK/BI/BPKH compliance validation** |
| 🔍 Fraud Detection | Benford's law, anomaly detection |
| 🔄 Continuous Audit | Rule-based monitoring |

### AI Copilot
| Feature | Description |
|---------|-------------|
| 🤖 Floating FAB | Accessible from any page |
| 💡 Smart Suggestions | Context-aware recommendations |
| 📊 KRI Analysis | Root cause identification |
| 📜 Compliance Checks | Regulatory validation |

### Executive Features (2026)
| Feature | Description |
|---------|-------------|
| 📊 5-Second Rule | Dominant KPI scorecard for instant comprehension |
| 💡 So-What Narrative | AI-generated strategic insights per metric |
| 🎮 Flight Simulator | What-if scenario simulation |
| 🔍 Data Lineage | Source transparency and quality scores |
| 📑 Report Export | PowerPoint, PDF, Excel, Email formats |

---

## 📊 KRI Active Cards

The enhanced KRI Dashboard features smart metric cards:

```python
from ui.components.active_kri_card import render_active_kri_card

render_active_kri_card(
    metric_id="npl_ratio",
    label="NPL Ratio",
    value=5.54,
    threshold=5.0,
    unit="%",
    trend_value=0.8,
    trend_direction="up"
)
# Shows "⚡ Analyze Risk" button when threshold breached
# Opens AI analysis modal with root causes
```

### Indonesian Banking KRI Thresholds
- **NPL Ratio**: Warning 3%, Danger 5%
- **LDR Ratio**: Warning 92%, Danger 98%
- **CAR Ratio**: Warning 12%, Danger 8% (lower is worse)
- **RoR Ratio**: Warning 85%, Danger 75% (lower is worse)

---

## 🔄 Process Mining

Upload event logs (CSV) to discover process flows:

```python
from modules.process_mining import (
    generate_sample_event_log,
    calculate_dfg,
    detect_bottlenecks,
    generate_dfg_graphviz
)

# Load event log
event_log = generate_sample_event_log(100)

# Calculate Directly-Follows Graph
dfg, counts = calculate_dfg(event_log)

# Detect bottlenecks
bottlenecks = detect_bottlenecks(event_log)

# Generate visualization
dot_string = generate_dfg_graphviz(dfg, counts, durations)
```

### Required CSV Format
| case_id | activity | timestamp |
|---------|----------|-----------|
| LOAN-001 | Application Received | 2024-01-15 09:00:00 |
| LOAN-001 | Document Verification | 2024-01-15 14:30:00 |

---

## 📜 Regulatory RAG

Validate compliance against Indonesian regulations:

```python
from modules.regulatory_rag import RegulatoryValidator

validator = RegulatoryValidator()

# Check compliance
result = validator.validate("We invest in coal mining")

print(result.overall_status)      # NON_COMPLIANT
print(result.compliance_score)    # 22.5
print(result.esg_category)        # BROWN
print(result.risk_factors)        # ["Brown activity under POJK 6/2022"]
```

### Supported Regulations
| Regulation | Description |
|------------|-------------|
| POJK 6/2022 | ESG Taxonomy (Green/Brown/Transition) |
| POJK 51/2017 | Sustainable Finance (20% target) |
| PBI 23/2021 | Climate Risk Management |
| BPKH 2023 | Sharia Compliance |

---

## 🛠️ Configuration

### Theme Support
- Light mode ☀️
- Dark mode 🌙

### LLM Providers
- Groq (Free tier available)
- Together AI (Free tier)
- Google AI Studio (Free tier)
- OpenAI (Paid)
- Mock mode (No API needed)

---

## 📖 Documentation

- [User Manual](docs/USER_MANUAL.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Demo Guide](docs/DEMO_GUIDE.md)
- [FAQ](docs/FAQ.md)

---

## 🏛️ Executive Dashboard

The Executive Dashboard provides C-Suite level insights:

```python
from ui.components.executive import (
    KPIMetric,
    TrendDirection,
    render_executive_scorecard,
    render_so_what_panel,
    generate_so_what_insight,
    render_flight_simulator,
    render_data_lineage
)

# Define executive KPI
kpi = KPIMetric(
    id="npl_ratio",
    label="NPL Ratio",
    value=5.54,
    unit="%",
    target=3.50,
    threshold_warning=4.00,
    threshold_danger=5.00,
    trend_direction=TrendDirection.UP,
    trend_value=0.82,
    source="Core Banking System"
)

# Render KPI Scorecard (5-Second Rule)
render_executive_scorecard([kpi], title="Executive Dashboard")

# Generate So-What insight
insight = generate_so_what_insight(kpi)
render_so_what_panel(insight)

# Run Flight Simulator scenario
render_flight_simulator(kpi)
```

### Executive Dashboard Tabs
| Tab | Description |
|-----|-------------|
| Strategic Insights | So-What narratives for critical/warning metrics |
| Scenario Simulator | Flight Simulator with pre-built stress scenarios |
| Detailed Analytics | KPI comparison table with data lineage |
| Reports | Export to PowerPoint, PDF, Excel, Email |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Run benchmark tests only
pytest tests/benchmarks/ -v
```

### Benchmarking

```bash
# LLM Latency Benchmark
python scripts/benchmark_llm_latency.py --provider mock --iterations 10

# RAG Accuracy Benchmark (RAGAS/G-Eval)
python scripts/benchmark_rag_accuracy.py --eval-framework simplified --output reports/

# All providers benchmark
python scripts/benchmark_llm_latency.py --all-providers --iterations 50
```

**Benchmark Thresholds:**
- LLM Latency: < 3000ms mean response time
- RAG Faithfulness: >= 0.85 (85% accuracy)

---

## 🐳 Docker

```bash
# Build
docker build -t aurix:2026 .

# Run
docker run -p 8501:8501 aurix:2026
```

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Sopian (mshadianto)**
- GitHub: [@mshadianto](https://github.com/mshadianto)
- LinkedIn: [mshadianto](https://linkedin.com/in/mshadianto)

---

## ⚠️ Disclaimer

Platform AURIX adalah alat bantu untuk Internal Auditor dan bukan pengganti professional judgment. Hasil analisis AI harus divalidasi oleh auditor yang kompeten. Developer tidak bertanggung jawab atas keputusan yang diambil berdasarkan output platform ini.

---

**AURIX Excellence 2026** - *Intelligent Audit. Elevated Assurance.* 🛡️
