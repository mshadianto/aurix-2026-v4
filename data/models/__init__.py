"""
Data Models for AURIX using Pydantic.
Provides type safety and validation for all data structures.
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator
import uuid


# ============================================
# Enums
# ============================================

class RiskLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class FindingStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"
    OVERDUE = "Overdue"


class ControlEffectiveness(str, Enum):
    EFFECTIVE = "Effective"
    PARTIALLY_EFFECTIVE = "Partially Effective"
    NOT_EFFECTIVE = "Not Effective"


class DocumentCategory(str, Enum):
    AUDIT_REPORTS = "Audit Reports"
    SOP_POLICIES = "SOP/Policies"
    REGULATIONS = "Regulations"
    WORKING_PAPERS = "Working Papers"
    RISK_ASSESSMENT = "Risk Assessment"
    FINANCIAL_DATA = "Financial Data"
    IT_DOCUMENTATION = "IT Documentation"
    COMPLIANCE_REPORTS = "Compliance Reports"


# ============================================
# Base Models
# ============================================

class BaseEntity(BaseModel):
    """Base model for all entities with common fields."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True


# ============================================
# Document Models
# ============================================

class Document(BaseEntity):
    """Document model for uploaded files."""
    name: str
    content: str = ""
    category: DocumentCategory = DocumentCategory.AUDIT_REPORTS
    file_type: str = ""
    file_size: int = 0
    hash: str = ""
    chunks: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Document name cannot be empty')
        return v.strip()


class DocumentChunk(BaseModel):
    """Chunk of processed document for RAG."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    document_id: str
    content: str
    sequence: int
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============================================
# Risk Models
# ============================================

class RiskFactor(BaseModel):
    """Individual risk factor."""
    name: str
    score: float = Field(ge=0.0, le=1.0)
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    description: str = ""


class RiskAssessment(BaseEntity):
    """Risk assessment model."""
    name: str
    area: str
    description: str = ""
    
    # Risk factors
    inherent_factors: List[RiskFactor] = Field(default_factory=list)
    control_factors: List[RiskFactor] = Field(default_factory=list)
    
    # Calculated scores
    inherent_risk_score: float = 0.0
    control_effectiveness_score: float = 0.0
    residual_risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    
    # Metadata
    assessed_by: str = ""
    assessed_date: date = Field(default_factory=date.today)
    
    def calculate_scores(self, inherent_weight: float = 0.6):
        """Calculate risk scores based on factors."""
        if self.inherent_factors:
            total_weight = sum(f.weight for f in self.inherent_factors)
            if total_weight > 0:
                self.inherent_risk_score = sum(
                    f.score * f.weight for f in self.inherent_factors
                ) / total_weight
        
        if self.control_factors:
            total_weight = sum(f.weight for f in self.control_factors)
            if total_weight > 0:
                self.control_effectiveness_score = sum(
                    f.score * f.weight for f in self.control_factors
                ) / total_weight
        
        # Residual risk = Inherent * (1 - Control Effectiveness)
        control_weight = 1 - inherent_weight
        self.residual_risk_score = (
            self.inherent_risk_score * inherent_weight +
            (1 - self.control_effectiveness_score) * control_weight
        )
        
        # Determine risk level
        if self.residual_risk_score >= 0.7:
            self.risk_level = RiskLevel.HIGH
        elif self.residual_risk_score >= 0.4:
            self.risk_level = RiskLevel.MEDIUM
        else:
            self.risk_level = RiskLevel.LOW


# ============================================
# Finding Models
# ============================================

class FindingCreate(BaseModel):
    """Model for creating a new finding."""
    title: str
    area: str
    rating: RiskLevel = RiskLevel.MEDIUM
    category: str = ""
    description: str = ""
    owner: str = ""
    due_date: date = Field(default_factory=lambda: date.today())


class Finding(BaseEntity):
    """Audit finding model."""
    title: str
    area: str
    rating: RiskLevel = RiskLevel.MEDIUM
    category: str = ""
    description: str = ""
    
    # 5 Cs
    condition: str = ""      # What was found
    criteria: str = ""       # What should be
    cause: str = ""          # Why it happened
    consequence: str = ""    # Impact/Effect
    corrective_action: str = ""  # Recommendation
    
    # Tracking
    owner: str = ""
    status: FindingStatus = FindingStatus.OPEN
    due_date: date = Field(default_factory=date.today)
    closed_date: Optional[date] = None
    
    # Management response
    management_response: str = ""
    action_plan: str = ""
    progress_percentage: int = Field(default=0, ge=0, le=100)
    
    # References
    audit_report_id: str = ""
    working_paper_ids: List[str] = Field(default_factory=list)
    
    @property
    def is_overdue(self) -> bool:
        """Check if finding is overdue."""
        if self.status == FindingStatus.CLOSED:
            return False
        return date.today() > self.due_date
    
    @property
    def days_remaining(self) -> int:
        """Calculate days remaining until due date."""
        return (self.due_date - date.today()).days


# ============================================
# KRI Models
# ============================================

class KRIIndicator(BaseModel):
    """Key Risk Indicator definition."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str
    category: str
    threshold: float
    unit: str
    good_direction: str = "lower"  # lower, higher, or optimal
    description: str = ""
    
    def calculate_status(self, value: float) -> str:
        """Calculate KRI status based on threshold."""
        if self.threshold == 0:
            if value == 0:
                return "success"
            elif value <= 2:
                return "warning"
            return "danger"
        
        if self.good_direction == "lower":
            if value <= self.threshold * 0.8:
                return "success"
            elif value <= self.threshold:
                return "warning"
            return "danger"
        
        elif self.good_direction == "higher":
            if value >= self.threshold:
                return "success"
            elif value >= self.threshold * 0.9:
                return "warning"
            return "danger"
        
        else:  # optimal
            if abs(value - self.threshold) <= self.threshold * 0.1:
                return "success"
            elif abs(value - self.threshold) <= self.threshold * 0.2:
                return "warning"
            return "danger"


class KRIValue(BaseModel):
    """KRI measurement value."""
    indicator_id: str
    value: float
    recorded_at: datetime = Field(default_factory=datetime.now)
    status: str = "success"
    notes: str = ""


# ============================================
# Continuous Audit Models
# ============================================

class ContinuousAuditRule(BaseEntity):
    """Continuous audit rule definition."""
    name: str
    description: str = ""
    category: str
    threshold: Optional[str] = None
    is_active: bool = False
    triggers_count: int = 0
    last_triggered: Optional[datetime] = None
    
    # Rule configuration
    sql_query: str = ""
    alert_level: RiskLevel = RiskLevel.MEDIUM


class CARuleAlert(BaseModel):
    """Alert generated by continuous audit rule."""
    rule_id: str
    rule_name: str
    triggered_at: datetime = Field(default_factory=datetime.now)
    details: Dict[str, Any] = Field(default_factory=dict)
    status: str = "new"
    reviewed_by: str = ""
    reviewed_at: Optional[datetime] = None


# ============================================
# Working Paper Models
# ============================================

class WorkingPaper(BaseEntity):
    """Working paper model."""
    reference: str
    template_type: str
    audit_area: str
    preparer: str = ""
    reviewer: str = ""
    audit_objective: str = ""
    sections: Dict[str, str] = Field(default_factory=dict)
    
    # Status
    is_reviewed: bool = False
    review_date: Optional[date] = None
    review_notes: str = ""


# ============================================
# Visitor/Analytics Models
# ============================================

class VisitorSession(BaseModel):
    """Visitor session model."""
    visitor_id: str
    session_start: datetime
    session_end: Optional[datetime] = None
    total_page_views: int = 0
    theme: str = "dark"
    pages_visited: List[Dict[str, Any]] = Field(default_factory=list)


class PageView(BaseModel):
    """Page view model."""
    visitor_id: str
    page_name: str
    view_timestamp: datetime = Field(default_factory=datetime.now)
    session_duration: int = 0


class VisitorStats(BaseModel):
    """Aggregated visitor statistics."""
    total_visits: int = 0
    unique_visitors: int = 0
    total_page_views: int = 0
    avg_session_duration: int = 0
    today_visits: int = 0
    today_visitors: int = 0
    popular_pages: List[tuple] = Field(default_factory=list)
    hourly_traffic: List[int] = Field(default_factory=lambda: [0] * 24)
    is_mock: bool = False


# ============================================
# LLM Models
# ============================================

class LLMResponse(BaseModel):
    """Response from LLM provider."""
    content: str
    model: str
    tokens_used: int = 0
    finish_reason: str = "stop"
    provider: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
