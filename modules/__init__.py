"""
AURIX 2026 Excellence Modules.
New intelligent modules for agentic audit platform.
"""

from modules.process_mining import (
    generate_sample_event_log,
    parse_event_log,
    calculate_dfg,
    calculate_activity_durations,
    detect_bottlenecks,
    get_process_variants,
    generate_dfg_graphviz,
    calculate_process_metrics,
    BottleneckInfo
)

from modules.regulatory_rag import (
    RegulatoryValidator,
    ComplianceResult,
    ComplianceStatus,
    ESGCategory,
    RegulatoryReference,
    REGULATORY_KNOWLEDGE_BASE,
    SAMPLE_QUERIES
)

__all__ = [
    # Process Mining
    "generate_sample_event_log",
    "parse_event_log",
    "calculate_dfg",
    "calculate_activity_durations",
    "detect_bottlenecks",
    "get_process_variants",
    "generate_dfg_graphviz",
    "calculate_process_metrics",
    "BottleneckInfo",
    # Regulatory RAG
    "RegulatoryValidator",
    "ComplianceResult",
    "ComplianceStatus",
    "ESGCategory",
    "RegulatoryReference",
    "REGULATORY_KNOWLEDGE_BASE",
    "SAMPLE_QUERIES",
]
