"""
Process Mining Module for AURIX 2026.
Automated process discovery with Directly-Follows Graph (DFG) visualization.

Features:
- Event log parsing (CSV format)
- DFG calculation and visualization
- Bottleneck detection
- Process variant analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import random


@dataclass
class BottleneckInfo:
    """Information about a detected bottleneck."""
    activity: str
    avg_duration_hours: float
    event_count: int
    severity: str  # "high", "medium", "low"
    percentile_rank: float


def generate_sample_event_log(num_cases: int = 100) -> pd.DataFrame:
    """
    Generate sample event log for loan approval process.
    
    Columns: case_id, activity, timestamp, resource
    """
    activities = [
        ("Application Received", 0.5, 2),      # (name, min_hours, max_hours)
        ("Document Verification", 4, 24),
        ("Credit Check", 2, 8),
        ("Risk Assessment", 24, 72),           # Intentional bottleneck
        ("Manager Approval", 4, 12),
        ("Final Review", 2, 6),
        ("Loan Disbursement", 1, 4)
    ]
    
    resources = ["Ahmad", "Budi", "Citra", "Dewi", "Eko", "Fitri"]
    
    events = []
    base_date = datetime.now() - timedelta(days=90)
    
    for case_num in range(1, num_cases + 1):
        case_id = f"LOAN-2024-{case_num:04d}"
        current_time = base_date + timedelta(days=random.uniform(0, 60))
        
        # Determine if this case has variants
        skip_credit = random.random() < 0.1  # 10% skip credit check
        needs_escalation = random.random() < 0.15  # 15% need escalation
        
        for i, (activity, min_h, max_h) in enumerate(activities):
            # Skip credit check for some cases
            if activity == "Credit Check" and skip_credit:
                continue
            
            # Add event
            events.append({
                "case_id": case_id,
                "activity": activity,
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "resource": random.choice(resources)
            })
            
            # Calculate next timestamp
            duration_hours = random.uniform(min_h, max_h)
            
            # Add extra time for bottleneck (Risk Assessment)
            if activity == "Risk Assessment":
                duration_hours *= random.uniform(1.2, 2.0)
            
            current_time += timedelta(hours=duration_hours)
            
            # Add escalation loop
            if activity == "Manager Approval" and needs_escalation:
                events.append({
                    "case_id": case_id,
                    "activity": "Escalation Review",
                    "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "resource": "Manager"
                })
                current_time += timedelta(hours=random.uniform(8, 24))
    
    df = pd.DataFrame(events)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values(["case_id", "timestamp"]).reset_index(drop=True)


def parse_event_log(df: pd.DataFrame, case_col: str, activity_col: str, timestamp_col: str) -> pd.DataFrame:
    """Parse and validate event log dataframe."""
    required_cols = [case_col, activity_col, timestamp_col]
    
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Standardize column names
    result = df[[case_col, activity_col, timestamp_col]].copy()
    result.columns = ["case_id", "activity", "timestamp"]
    
    # Parse timestamp
    result["timestamp"] = pd.to_datetime(result["timestamp"])
    
    # Sort by case and timestamp
    result = result.sort_values(["case_id", "timestamp"]).reset_index(drop=True)
    
    return result


def calculate_dfg(df: pd.DataFrame) -> Tuple[Dict[Tuple[str, str], int], Dict[str, int]]:
    """
    Calculate Directly-Follows Graph from event log.
    
    Returns:
        dfg_frequencies: Dict mapping (source, target) to frequency
        activity_counts: Dict mapping activity to total count
    """
    dfg = defaultdict(int)
    activity_counts = defaultdict(int)
    
    for case_id, group in df.groupby("case_id"):
        activities = group.sort_values("timestamp")["activity"].tolist()
        
        for activity in activities:
            activity_counts[activity] += 1
        
        for i in range(len(activities) - 1):
            source = activities[i]
            target = activities[i + 1]
            dfg[(source, target)] += 1
    
    return dict(dfg), dict(activity_counts)


def calculate_activity_durations(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate average duration for each activity in hours."""
    durations = defaultdict(list)
    
    for case_id, group in df.groupby("case_id"):
        sorted_group = group.sort_values("timestamp")
        timestamps = sorted_group["timestamp"].tolist()
        activities = sorted_group["activity"].tolist()
        
        for i in range(len(timestamps) - 1):
            activity = activities[i]
            duration = (timestamps[i + 1] - timestamps[i]).total_seconds() / 3600
            durations[activity].append(duration)
    
    # Calculate averages
    avg_durations = {}
    for activity, dur_list in durations.items():
        if dur_list:
            avg_durations[activity] = sum(dur_list) / len(dur_list)
        else:
            avg_durations[activity] = 0
    
    return avg_durations


def detect_bottlenecks(
    df: pd.DataFrame,
    threshold_percentile: float = 75
) -> List[BottleneckInfo]:
    """
    Detect bottleneck activities based on duration.
    
    Args:
        df: Event log dataframe
        threshold_percentile: Percentile threshold for bottleneck detection
    
    Returns:
        List of BottleneckInfo objects
    """
    durations = calculate_activity_durations(df)
    activity_counts = df.groupby("activity").size().to_dict()
    
    if not durations:
        return []
    
    # Calculate threshold
    all_durations = list(durations.values())
    threshold = np.percentile(all_durations, threshold_percentile)
    
    bottlenecks = []
    
    for activity, avg_duration in sorted(durations.items(), key=lambda x: -x[1]):
        # Calculate percentile rank
        rank = sum(1 for d in all_durations if d <= avg_duration) / len(all_durations) * 100
        
        # Determine severity
        if avg_duration >= np.percentile(all_durations, 90):
            severity = "high"
        elif avg_duration >= threshold:
            severity = "medium"
        else:
            severity = "low"
        
        if avg_duration >= threshold:
            bottlenecks.append(BottleneckInfo(
                activity=activity,
                avg_duration_hours=round(avg_duration, 2),
                event_count=activity_counts.get(activity, 0),
                severity=severity,
                percentile_rank=round(rank, 1)
            ))
    
    return bottlenecks


def get_process_variants(df: pd.DataFrame, top_n: int = 5) -> List[Dict]:
    """Get top process variants by frequency."""
    variants = defaultdict(int)
    
    for case_id, group in df.groupby("case_id"):
        trace = " → ".join(group.sort_values("timestamp")["activity"].tolist())
        variants[trace] += 1
    
    # Sort by frequency
    sorted_variants = sorted(variants.items(), key=lambda x: -x[1])
    
    result = []
    total_cases = sum(variants.values())
    
    for i, (trace, count) in enumerate(sorted_variants[:top_n], 1):
        result.append({
            "rank": i,
            "trace": trace,
            "count": count,
            "percentage": round(count / total_cases * 100, 1)
        })
    
    return result


def generate_dfg_graphviz(
    dfg: Dict[Tuple[str, str], int],
    activity_counts: Dict[str, int],
    durations: Dict[str, float],
    bottleneck_activities: List[str] = None
) -> str:
    """
    Generate Graphviz DOT string for DFG visualization.
    
    Args:
        dfg: Dict mapping (source, target) to frequency
        activity_counts: Dict mapping activity to count
        durations: Dict mapping activity to average duration
        bottleneck_activities: List of activity names that are bottlenecks
    
    Returns:
        DOT string for Graphviz
    """
    if bottleneck_activities is None:
        bottleneck_activities = []
    
    lines = [
        'digraph DFG {',
        '    rankdir=TB;',
        '    node [shape=box, style="rounded,filled", fontname="Arial", fontsize=10];',
        '    edge [fontname="Arial", fontsize=9];',
        ''
    ]
    
    # Add nodes
    for activity, count in activity_counts.items():
        duration = durations.get(activity, 0)
        
        # Format duration
        if duration >= 24:
            dur_str = f"{duration/24:.1f}d"
        else:
            dur_str = f"{duration:.1f}h"
        
        # Style based on bottleneck status
        if activity in bottleneck_activities:
            fill_color = "#FFCDD2"  # Light red
            border_color = "#C62828"  # Dark red
            penwidth = "2"
        else:
            fill_color = "#E3F2FD"  # Light blue
            border_color = "#1565C0"  # Dark blue
            penwidth = "1"
        
        label = f"{activity}\\n({count} events, {dur_str})"
        lines.append(f'    "{activity}" [label="{label}", fillcolor="{fill_color}", color="{border_color}", penwidth={penwidth}];')
    
    lines.append('')
    
    # Add edges
    max_freq = max(dfg.values()) if dfg else 1
    
    for (source, target), freq in dfg.items():
        # Edge thickness based on frequency
        penwidth = max(1, (freq / max_freq) * 4)
        lines.append(f'    "{source}" -> "{target}" [label="{freq}", penwidth={penwidth:.1f}];')
    
    lines.append('}')
    
    return '\n'.join(lines)


def calculate_process_metrics(df: pd.DataFrame) -> Dict:
    """Calculate overall process metrics."""
    # Case durations
    case_durations = []
    for case_id, group in df.groupby("case_id"):
        sorted_group = group.sort_values("timestamp")
        start = sorted_group["timestamp"].min()
        end = sorted_group["timestamp"].max()
        duration_hours = (end - start).total_seconds() / 3600
        case_durations.append(duration_hours)
    
    unique_activities = df["activity"].nunique()
    total_events = len(df)
    total_cases = df["case_id"].nunique()
    
    return {
        "total_cases": total_cases,
        "total_events": total_events,
        "unique_activities": unique_activities,
        "avg_case_duration_hours": round(np.mean(case_durations), 2) if case_durations else 0,
        "median_case_duration_hours": round(np.median(case_durations), 2) if case_durations else 0,
        "min_case_duration_hours": round(min(case_durations), 2) if case_durations else 0,
        "max_case_duration_hours": round(max(case_durations), 2) if case_durations else 0,
        "events_per_case": round(total_events / total_cases, 1) if total_cases else 0
    }


# Export
__all__ = [
    "generate_sample_event_log",
    "parse_event_log",
    "calculate_dfg",
    "calculate_activity_durations",
    "detect_bottlenecks",
    "get_process_variants",
    "generate_dfg_graphviz",
    "calculate_process_metrics",
    "BottleneckInfo"
]
