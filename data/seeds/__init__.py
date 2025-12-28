"""
Seed Data for AURIX - Static reference data.
Contains audit universe, regulations, KRI indicators, fraud red flags, etc.
"""

from typing import Dict, List, Any


# ============================================
# Regulations Database
# ============================================

REGULATIONS: Dict[str, List[Dict[str, str]]] = {
    "OJK": [
        {"code": "POJK 18/2016", "title": "Penerapan Manajemen Risiko bagi Bank Umum", "category": "Risk Management"},
        {"code": "POJK 55/2016", "title": "Penerapan Tata Kelola bagi Bank Umum", "category": "Governance"},
        {"code": "POJK 12/2017", "title": "Penerapan APU-PPT sektor Jasa Keuangan", "category": "AML/CFT"},
        {"code": "POJK 13/2017", "title": "Penggunaan Jasa Akuntan Publik dan KAP", "category": "External Audit"},
        {"code": "POJK 40/2019", "title": "Penilaian Kualitas Aset Bank Umum", "category": "Credit"},
        {"code": "POJK 11/2022", "title": "Penyelenggaraan Teknologi Informasi oleh Bank Umum", "category": "IT"},
    ],
    "BI": [
        {"code": "PBI 23/6/2021", "title": "Penyedia Jasa Pembayaran", "category": "Payment System"},
        {"code": "PBI 19/12/2017", "title": "Penyelenggaraan Teknologi Finansial", "category": "Fintech"},
    ],
    "BPKH": [
        {"code": "PP 5/2018", "title": "Pengelolaan Keuangan Haji", "category": "Hajj Finance"},
        {"code": "UU 34/2014", "title": "Pengelolaan Keuangan Haji", "category": "Hajj Finance"},
    ],
    "ISO": [
        {"code": "ISO 37001:2016", "title": "Anti-Bribery Management Systems", "category": "Anti-Corruption"},
        {"code": "ISO 31000:2018", "title": "Risk Management Guidelines", "category": "Risk Management"},
        {"code": "ISO 27001:2022", "title": "Information Security Management", "category": "IT Security"},
    ]
}


# ============================================
# Audit Universe
# ============================================

AUDIT_UNIVERSE: Dict[str, List[str]] = {
    "Governance & Compliance": [
        "Board Effectiveness",
        "Committee Governance",
        "Regulatory Compliance",
        "Ethics & Code of Conduct",
        "Whistleblowing System",
        "Conflict of Interest"
    ],
    "Risk Management": [
        "Enterprise Risk Management",
        "Credit Risk",
        "Market Risk",
        "Operational Risk",
        "Liquidity Risk",
        "Reputational Risk"
    ],
    "Financial Operations": [
        "Treasury Management",
        "Investment Portfolio",
        "Credit Administration",
        "Financial Reporting",
        "Tax Compliance",
        "Asset Liability Management"
    ],
    "Operational Processes": [
        "Customer Onboarding (KYC)",
        "Transaction Processing",
        "Account Reconciliation",
        "Vendor Management",
        "Procurement",
        "HR Management"
    ],
    "Technology & Security": [
        "IT General Controls",
        "Application Controls",
        "Cybersecurity",
        "Data Privacy",
        "Business Continuity",
        "Core Banking System"
    ],
    "Anti-Money Laundering": [
        "AML Program",
        "Transaction Monitoring",
        "STR Reporting",
        "Sanctions Screening",
        "Customer Due Diligence",
        "Beneficial Ownership"
    ]
}


# ============================================
# Risk Factors
# ============================================

RISK_FACTORS: Dict[str, List[str]] = {
    "inherent": [
        "Complexity",
        "Transaction Volume",
        "Regulatory Scrutiny",
        "Issue History",
        "Organizational Changes"
    ],
    "control": [
        "Control Design",
        "Operating Effectiveness",
        "Management Oversight",
        "Segregation of Duties",
        "Automation Level"
    ]
}


# ============================================
# KRI Indicators
# ============================================

KRI_INDICATORS: Dict[str, List[Dict[str, Any]]] = {
    "Credit Risk": [
        {"name": "NPL Ratio", "threshold": 5.0, "unit": "%", "good_direction": "lower"},
        {"name": "CKPN Coverage", "threshold": 100.0, "unit": "%", "good_direction": "higher"},
        {"name": "BMPK Violations", "threshold": 0, "unit": "cases", "good_direction": "lower"},
        {"name": "Concentration Top 10", "threshold": 25.0, "unit": "%", "good_direction": "lower"},
    ],
    "Liquidity Risk": [
        {"name": "LCR", "threshold": 100.0, "unit": "%", "good_direction": "higher"},
        {"name": "NSFR", "threshold": 100.0, "unit": "%", "good_direction": "higher"},
        {"name": "LDR", "threshold": 92.0, "unit": "%", "good_direction": "optimal"},
    ],
    "Operational Risk": [
        {"name": "Loss Ratio", "threshold": 5.0, "unit": "%", "good_direction": "lower"},
        {"name": "System Downtime", "threshold": 2.0, "unit": "hours", "good_direction": "lower"},
        {"name": "Transaction Errors", "threshold": 0.1, "unit": "%", "good_direction": "lower"},
    ],
    "Compliance Risk": [
        {"name": "Regulatory Breaches", "threshold": 0, "unit": "cases", "good_direction": "lower"},
        {"name": "AML Alerts Backlog", "threshold": 10, "unit": "days", "good_direction": "lower"},
        {"name": "Policy Exceptions", "threshold": 5, "unit": "cases", "good_direction": "lower"},
    ],
    "IT/Cyber Risk": [
        {"name": "Patch Compliance", "threshold": 95.0, "unit": "%", "good_direction": "higher"},
        {"name": "Critical Vulnerabilities", "threshold": 0, "unit": "cases", "good_direction": "lower"},
        {"name": "Failed Login Attempts", "threshold": 100, "unit": "daily", "good_direction": "lower"},
        {"name": "Security Incidents", "threshold": 0, "unit": "cases", "good_direction": "lower"},
    ],
    "Market Risk": [
        {"name": "VaR Utilization", "threshold": 80.0, "unit": "%", "good_direction": "lower"},
        {"name": "Interest Rate Sensitivity", "threshold": 10.0, "unit": "%", "good_direction": "lower"},
        {"name": "FX Exposure", "threshold": 20.0, "unit": "%", "good_direction": "lower"},
    ]
}


# ============================================
# Fraud Red Flags
# ============================================

FRAUD_RED_FLAGS: Dict[str, List[str]] = {
    "Financial Statement Fraud": [
        "Unusual year-end transactions",
        "Significant related party transactions",
        "Aggressive revenue recognition",
        "Inadequate disclosure of liabilities",
        "Changes in accounting policies without justification",
        "Management override of controls",
        "Unusual journal entries",
        "Weaknesses in internal controls",
        "High management turnover",
        "Pressure to meet targets",
    ],
    "Asset Misappropriation": [
        "Missing inventory or assets",
        "Duplicate vendor payments",
        "Unauthorized petty cash withdrawals",
        "Fictitious vendors or employees",
        "Excessive write-offs",
        "Unexplained inventory shrinkage",
        "Altered or missing documents",
        "Lifestyle beyond means",
        "Reluctance to take vacation",
        "Close relationship with vendors",
    ],
    "Corruption & Bribery": [
        "Gifts and hospitality not disclosed",
        "Unusual payment patterns to vendors",
        "Split purchases to avoid approval limits",
        "Sole source procurement without justification",
        "Conflicts of interest not declared",
        "Favoring certain vendors",
        "Commission payments without contracts",
        "Unusual consultancy fees",
        "Payments to offshore entities",
        "Lack of due diligence on third parties",
    ],
    "Cyber Fraud": [
        "Unauthorized access to systems",
        "Data exfiltration attempts",
        "Unusual login patterns",
        "Privilege escalation",
        "Disabled security controls",
        "Unusual network traffic",
        "Multiple failed login attempts",
        "Access from unusual locations",
        "After-hours system access",
        "Unauthorized software installations",
    ],
    "Credit Fraud": [
        "False income documentation",
        "Identity theft indicators",
        "Rapid account opening and usage",
        "Straw borrowers",
        "Inflated collateral valuations",
        "Missing documentation",
        "Inconsistent information",
        "Early payment default",
        "Multiple applications",
        "Circular transactions",
    ],
    "AML Red Flags": [
        "Structuring transactions below reporting threshold",
        "Unusual wire transfer patterns",
        "Complex ownership structures",
        "Cash-intensive businesses",
        "Transactions inconsistent with business profile",
        "Reluctance to provide information",
        "Use of multiple accounts",
        "Transactions involving high-risk jurisdictions",
        "No apparent legitimate purpose",
        "PEP involvement without disclosure",
    ]
}


# ============================================
# Continuous Audit Rules
# ============================================

CONTINUOUS_AUDIT_RULES: List[Dict[str, Any]] = [
    {"id": 1, "name": "Large Cash Transaction", "description": "Detect cash transactions > $10,000", "category": "AML", "threshold": 10000},
    {"id": 2, "name": "Duplicate Payment", "description": "Identify duplicate vendor payments", "category": "Financial", "threshold": None},
    {"id": 3, "name": "After Hours Access", "description": "System access outside business hours", "category": "IT", "threshold": "18:00-06:00"},
    {"id": 4, "name": "Failed Login", "description": "Multiple failed login attempts", "category": "Security", "threshold": 5},
    {"id": 5, "name": "Segregation Violation", "description": "Same user approval and payment", "category": "Controls", "threshold": None},
    {"id": 6, "name": "Credit Limit Breach", "description": "Transaction exceeds approved limit", "category": "Credit", "threshold": "Limit+10%"},
    {"id": 7, "name": "Vendor Master Change", "description": "Bank account change in vendor master", "category": "Financial", "threshold": None},
    {"id": 8, "name": "Dormant Account Activity", "description": "Transaction in dormant account", "category": "Operations", "threshold": "90 days"},
    {"id": 9, "name": "Round Amount", "description": "Payments in round amounts", "category": "Financial", "threshold": None},
    {"id": 10, "name": "Privilege Escalation", "description": "User role elevation", "category": "Security", "threshold": None},
    {"id": 11, "name": "Journal Entry Anomaly", "description": "Manual journal entries > threshold", "category": "Financial", "threshold": 50000},
    {"id": 12, "name": "Reconciliation Delay", "description": "Account reconciliation overdue", "category": "Controls", "threshold": "5 days"},
    {"id": 13, "name": "Unusual Time Transaction", "description": "Transaction timestamp anomaly", "category": "Operations", "threshold": None},
    {"id": 14, "name": "Multiple Refunds", "description": "Excessive refunds to single customer", "category": "Operations", "threshold": 3},
    {"id": 15, "name": "Parameter Change", "description": "System parameter modification", "category": "IT", "threshold": None},
    {"id": 16, "name": "High Value Transfer", "description": "Wire transfer > $100,000", "category": "Treasury", "threshold": 100000},
    {"id": 17, "name": "Velocity Check", "description": "Rapid successive transactions", "category": "Fraud", "threshold": "5 in 1 hour"},
    {"id": 18, "name": "Geolocation Anomaly", "description": "Access from unusual location", "category": "Security", "threshold": None},
]


# ============================================
# System Prompts for LLM
# ============================================

SYSTEM_PROMPTS: Dict[str, str] = {
    "default": """Anda adalah expert Internal Audit profesional yang berspesialisasi dalam institusi keuangan Indonesia.
Keahlian Anda meliputi:
- Metodologi risk-based audit (IIA Standards)
- Regulasi Indonesia (OJK, BI, BPKH)
- Standar ISO (37001, 31000, 27001)
- Pendekatan audit Big 4 dan McKinsey

Berikan respons yang profesional dan actionable dengan rekomendasi spesifik.
Selalu pertimbangkan implikasi kepatuhan regulasi untuk industri keuangan Indonesia.
Gunakan bahasa Indonesia yang baik dan formal.""",

    "risk_assessment": """Anda adalah Risk Assessment Specialist yang menganalisis risiko institusi keuangan Indonesia.
Fokus pada:
- Identifikasi faktor inherent risk
- Evaluasi efektivitas kontrol
- Penentuan tingkat residual risk
- Prioritasi fokus area audit
Gunakan matriks risiko terstruktur dan rating risiko yang jelas (High/Medium/Low).""",

    "procedure_generation": """Anda adalah Senior Auditor yang mengembangkan program kerja audit.
Buat prosedur audit yang detail dan praktis yang:
- Spesifik dan dapat dilaksanakan
- Mencakup sample size yang tepat
- Mereferensi regulasi yang berlaku
- Menentukan nature of testing (Inquiry, Observation, Inspection, Reperformance)
- Mempertimbangkan IT controls yang relevan""",

    "compliance_officer": """Anda adalah Senior Compliance Officer specializing in Indonesian financial services regulations.
Expertise includes:
- OJK regulations (POJK, SEOJK)
- Bank Indonesia regulations (PBI)
- Anti-Money Laundering (APU-PPT)
- Know Your Customer (KYC/CDD)
- Whistleblowing systems

Focus on regulatory compliance gaps, control recommendations, reporting requirements.""",

    "it_auditor": """Anda adalah IT Auditor specializing in financial services technology.
Expertise includes:
- IT General Controls (ITGC)
- Application Controls
- Cybersecurity frameworks (ISO 27001)
- Core Banking Systems
- Fintech regulations (PBI 19/2017)

Focus on access control testing, change management, data integrity controls, business continuity."""
}


# ============================================
# PTCF Templates
# ============================================

PTCF_TEMPLATES: Dict[str, Dict[str, str]] = {
    "risk_identification": {
        "persona": "Internal Audit Manager with expertise in risk assessment",
        "task": "Identify and prioritize the top {num_risks} high-risk areas",
        "context": "Based on the provided documents: {documents}. Consider Indonesian regulatory requirements.",
        "format": "Present findings in a risk assessment table with: Risk Area, Inherent Risk Rating, Key Risk Factors, and Recommended Audit Focus"
    },
    "control_assessment": {
        "persona": "Internal Auditor evaluating control effectiveness",
        "task": "Assess the design and operating effectiveness of controls for {audit_area}",
        "context": "Reference documents: {documents}. Apply COSO Internal Control Framework.",
        "format": "Provide a control matrix showing: Control Activity, Control Objective, Design Assessment, Operating Effectiveness, and Gaps Identified"
    },
    "compliance_review": {
        "persona": "Compliance Specialist reviewing regulatory adherence",
        "task": "Evaluate compliance with {regulation} requirements",
        "context": "Based on: {documents}. Focus on material compliance gaps.",
        "format": "Create a compliance checklist with: Requirement, Current Status, Evidence Reviewed, Gap Description, and Remediation Priority"
    },
    "procedure_generation": {
        "persona": "Senior Auditor developing audit work programs",
        "task": "Generate detailed audit procedures for {audit_area}",
        "context": "Consider: {documents}. Apply risk-based audit methodology.",
        "format": "Table format with: Step Number, Procedure Description, Nature of Test, Sample Size, and Expected Evidence"
    },
    "finding_documentation": {
        "persona": "Audit Report Writer documenting observations",
        "task": "Document audit finding for {issue_description}",
        "context": "Supporting evidence: {documents}. Follow IIA Standards for reporting.",
        "format": "Structure as: Condition (What was found), Criteria (What should be), Cause (Why it happened), Effect (Impact), and Recommendation"
    }
}


# ============================================
# Helper Functions
# ============================================

def get_regulations_by_category(category: str) -> List[Dict[str, str]]:
    """Get regulations by category (OJK, BI, BPKH, ISO)."""
    return REGULATIONS.get(category, [])


def get_audit_areas_by_category(category: str) -> List[str]:
    """Get audit areas by category."""
    return AUDIT_UNIVERSE.get(category, [])


def get_all_audit_areas() -> List[str]:
    """Get flat list of all audit areas."""
    return [area for areas in AUDIT_UNIVERSE.values() for area in areas]


def get_kri_by_category(category: str) -> List[Dict[str, Any]]:
    """Get KRI indicators by category."""
    return KRI_INDICATORS.get(category, [])


def get_fraud_flags_by_category(category: str) -> List[str]:
    """Get fraud red flags by category."""
    return FRAUD_RED_FLAGS.get(category, [])


def get_ca_rules_by_category(category: str) -> List[Dict[str, Any]]:
    """Get continuous audit rules by category."""
    return [r for r in CONTINUOUS_AUDIT_RULES if r["category"] == category]


def get_system_prompt(persona: str) -> str:
    """Get system prompt by persona."""
    return SYSTEM_PROMPTS.get(persona, SYSTEM_PROMPTS["default"])
