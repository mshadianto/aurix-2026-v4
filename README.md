# 🛡️ AURIX Excellence 2026

**AUdit Risk Intelligence eXcellence** - Agentic Audit Platform for Indonesian Financial Industry

[![Version](https://img.shields.io/badge/version-4.2%20Excellence%202026-blue.svg)](https://github.com/mshadianto/aurix)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red.svg)](https://streamlit.io)

---

## 🆕 What's New in 2026 Excellence

### 1. 🎯 Grouped Navigation + Floating AI Copilot
- **Grouped sidebar navigation** - Organized into Core Audit, Intelligence, Labs, Admin
- **Floating Action Button (FAB)** - Persistent AI Copilot accessible from any page
- **Contextual suggestions** - AI adapts recommendations based on current page

### 2. ⚡ Active KRI Cards with AI Analysis
- **Smart metric cards** - Visual status indicators (Normal/Warning/Danger)
- **One-click AI analysis** - Automatic root cause identification when thresholds breached
- **Modal dialog** - Shows root causes, severity ratings, evidence, and recommendations

### 3. 🔄 Process Mining
- **Automated process discovery** - Upload event logs, get DFG visualization
- **Bottleneck detection** - Identifies process inefficiencies automatically
- **Process variants analysis** - Compare different execution paths

### 4. 📜 Regulatory RAG
- **Indonesian regulations** - OJK, BI, BPKH compliance validation
- **ESG Taxonomy** - POJK 6/2022 green/brown/transition classification
- **Sharia compliance** - BPKH haram activity detection

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
│   │   └── badges.py
│   ├── pages/
│   │   ├── dashboard.py
│   │   ├── kri_dashboard.py  # 🆕 Active cards
│   │   ├── process_mining.py # 🆕 New page
│   │   ├── regulatory_rag.py # 🆕 New page
│   │   └── ...               # 26+ existing pages
│   └── styles/
│       └── css_builder.py
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

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

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
