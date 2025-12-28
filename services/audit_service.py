"""
Audit Service
Core business logic for audit operations
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk level classification"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FindingStatus(Enum):
    """Finding lifecycle status"""
    DRAFT = "Draft"
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    PENDING_VERIFICATION = "Pending Verification"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"


class ControlEffectiveness(Enum):
    """Control effectiveness rating"""
    EFFECTIVE = "Effective"
    PARTIALLY_EFFECTIVE = "Partially Effective"
    NOT_EFFECTIVE = "Not Effective"
    NOT_TESTED = "Not Tested"


@dataclass
class RiskAssessmentInput:
    """Input for risk assessment calculation"""
    area: str
    name: str
    description: str = ""
    
    # Inherent risk factors (1-5 scale)
    complexity: int = 3
    volume: int = 3
    regulatory_scrutiny: int = 3
    issue_history: int = 3
    organizational_change: int = 3
    
    # Control factors (1-5 scale)
    control_design: int = 3
    operating_effectiveness: int = 3
    management_oversight: int = 3
    segregation_of_duties: int = 3
    automation_level: int = 3


@dataclass
class RiskAssessmentResult:
    """Result of risk assessment calculation"""
    name: str
    area: str
    description: str
    
    inherent_score: float
    control_score: float
    residual_score: float
    risk_level: RiskLevel
    
    inherent_factors: Dict[str, int]
    control_factors: Dict[str, int]
    
    assessed_at: datetime = field(default_factory=datetime.now)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class Finding:
    """Audit finding entity"""
    id: str
    title: str
    audit_area: str
    risk_rating: RiskLevel
    category: str
    
    condition: str  # What was found
    criteria: str   # What should be
    cause: str      # Why it happened
    effect: str     # Impact/consequence
    recommendation: str
    
    owner: str = ""
    due_date: Optional[date] = None
    status: FindingStatus = FindingStatus.OPEN
    
    management_response: str = ""
    action_plan: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    closed_at: Optional[datetime] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_overdue(self) -> bool:
        """Check if finding is overdue"""
        if self.due_date and self.status not in [FindingStatus.CLOSED, FindingStatus.CANCELLED]:
            return date.today() > self.due_date
        return False
    
    @property
    def days_remaining(self) -> Optional[int]:
        """Days until due date"""
        if self.due_date:
            return (self.due_date - date.today()).days
        return None


@dataclass
class AuditProcedure:
    """Audit test procedure"""
    step: int
    description: str
    nature: str  # Inquiry, Observation, Inspection, Reperformance, Analytics
    sample_size: str
    timing: str = ""
    status: str = "Pending"
    result: str = ""
    workpaper_ref: str = ""


@dataclass
class WorkingPaper:
    """Audit working paper"""
    reference: str
    template_type: str
    audit_area: str
    objective: str
    
    preparer: str
    reviewer: str
    
    sections: Dict[str, str]
    status: str = "Draft"
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class RiskCalculator:
    """
    Risk calculation engine
    Implements risk-based audit methodology
    """
    
    # Default weights
    INHERENT_WEIGHT = 0.6
    CONTROL_WEIGHT = 0.4
    
    # Risk thresholds
    HIGH_THRESHOLD = 0.7
    MEDIUM_THRESHOLD = 0.4
    
    def calculate(self, input: RiskAssessmentInput) -> RiskAssessmentResult:
        """Calculate risk assessment"""
        
        # Calculate inherent risk score (normalize to 0-1)
        inherent_factors = {
            "complexity": input.complexity,
            "volume": input.volume,
            "regulatory_scrutiny": input.regulatory_scrutiny,
            "issue_history": input.issue_history,
            "organizational_change": input.organizational_change
        }
        inherent_score = sum(inherent_factors.values()) / (len(inherent_factors) * 5)
        
        # Calculate control score (normalize to 0-1)
        control_factors = {
            "control_design": input.control_design,
            "operating_effectiveness": input.operating_effectiveness,
            "management_oversight": input.management_oversight,
            "segregation_of_duties": input.segregation_of_duties,
            "automation_level": input.automation_level
        }
        control_score = sum(control_factors.values()) / (len(control_factors) * 5)
        
        # Calculate residual risk
        # Higher inherent + lower control = higher residual
        control_gap = 1 - control_score
        residual_score = (inherent_score * self.INHERENT_WEIGHT) + (control_gap * self.CONTROL_WEIGHT)
        
        # Determine risk level
        if residual_score >= self.HIGH_THRESHOLD:
            risk_level = RiskLevel.HIGH
        elif residual_score >= self.MEDIUM_THRESHOLD:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            inherent_factors, control_factors, risk_level
        )
        
        return RiskAssessmentResult(
            name=input.name,
            area=input.area,
            description=input.description,
            inherent_score=round(inherent_score * 100, 1),
            control_score=round(control_score * 100, 1),
            residual_score=round(residual_score * 100, 1),
            risk_level=risk_level,
            inherent_factors=inherent_factors,
            control_factors=control_factors,
            recommendations=recommendations
        )
    
    def _generate_recommendations(
        self,
        inherent: Dict[str, int],
        control: Dict[str, int],
        risk_level: RiskLevel
    ) -> List[str]:
        """Generate risk-based recommendations"""
        recommendations = []
        
        # High inherent factors
        if inherent.get("complexity", 0) >= 4:
            recommendations.append("Consider specialized audit expertise for complex areas")
        
        if inherent.get("regulatory_scrutiny", 0) >= 4:
            recommendations.append("Include regulatory compliance testing in audit scope")
        
        if inherent.get("issue_history", 0) >= 4:
            recommendations.append("Review root causes of historical issues")
        
        # Weak controls
        if control.get("control_design", 0) <= 2:
            recommendations.append("Evaluate control design adequacy")
        
        if control.get("operating_effectiveness", 0) <= 2:
            recommendations.append("Increase sample size for control testing")
        
        if control.get("management_oversight", 0) <= 2:
            recommendations.append("Assess management monitoring activities")
        
        if control.get("segregation_of_duties", 0) <= 2:
            recommendations.append("Review segregation of duties matrix")
        
        # Risk level specific
        if risk_level == RiskLevel.HIGH:
            recommendations.append("Prioritize for immediate audit coverage")
            recommendations.append("Consider continuous monitoring implementation")
        
        return recommendations


class ProcedureGenerator:
    """
    Generate audit procedures based on audit area and risk
    """
    
    # Standard procedure templates by category
    PROCEDURE_TEMPLATES = {
        "document_review": [
            "Obtain and review relevant policies, procedures, and guidelines",
            "Verify documentation is current and approved",
            "Compare documentation against regulatory requirements"
        ],
        "walkthrough": [
            "Conduct walkthrough with process owner",
            "Document key process steps and controls",
            "Identify control points and potential gaps"
        ],
        "control_testing": [
            "Select sample based on risk assessment",
            "Test design effectiveness of key controls",
            "Test operating effectiveness through reperformance",
            "Document test results and exceptions"
        ],
        "analytics": [
            "Define population and obtain complete data extract",
            "Perform data quality validation",
            "Execute analytical procedures (trend, ratio, comparison)",
            "Investigate anomalies and outliers"
        ],
        "compliance": [
            "Identify applicable regulatory requirements",
            "Map requirements to current practices",
            "Test compliance with key requirements",
            "Document compliance gaps"
        ]
    }
    
    def generate(
        self,
        audit_area: str,
        risk_level: RiskLevel,
        include_analytics: bool = True,
        include_it_controls: bool = False,
        regulations: List[str] = None
    ) -> List[AuditProcedure]:
        """Generate audit procedures for specified area"""
        procedures = []
        step = 1
        
        # Planning procedures
        procedures.append(AuditProcedure(
            step=step,
            description=f"Review prior audit reports and findings for {audit_area}",
            nature="Document Review",
            sample_size="N/A",
            timing="Planning"
        ))
        step += 1
        
        # Document review
        for template in self.PROCEDURE_TEMPLATES["document_review"]:
            procedures.append(AuditProcedure(
                step=step,
                description=f"{template} for {audit_area}",
                nature="Document Review",
                sample_size="All relevant",
                timing="Fieldwork"
            ))
            step += 1
        
        # Walkthrough
        procedures.append(AuditProcedure(
            step=step,
            description=f"Perform walkthrough of {audit_area} process with key stakeholders",
            nature="Inquiry/Observation",
            sample_size="1 end-to-end",
            timing="Fieldwork"
        ))
        step += 1
        
        # Control testing - sample size based on risk
        sample_size = self._get_sample_size(risk_level)
        for template in self.PROCEDURE_TEMPLATES["control_testing"]:
            procedures.append(AuditProcedure(
                step=step,
                description=f"{template} for {audit_area}",
                nature="Testing/Reperformance",
                sample_size=sample_size,
                timing="Fieldwork"
            ))
            step += 1
        
        # Analytics procedures
        if include_analytics:
            for template in self.PROCEDURE_TEMPLATES["analytics"]:
                procedures.append(AuditProcedure(
                    step=step,
                    description=f"{template} for {audit_area}",
                    nature="Analytics",
                    sample_size="100% of population",
                    timing="Fieldwork"
                ))
                step += 1
        
        # Compliance procedures
        if regulations:
            for reg in regulations:
                procedures.append(AuditProcedure(
                    step=step,
                    description=f"Test compliance with {reg} requirements",
                    nature="Compliance Testing",
                    sample_size=sample_size,
                    timing="Fieldwork"
                ))
                step += 1
        
        # IT control procedures
        if include_it_controls:
            it_procedures = [
                "Review user access rights and authorization matrix",
                "Test segregation of duties in system",
                "Review change management logs",
                "Verify data integrity controls"
            ]
            for proc in it_procedures:
                procedures.append(AuditProcedure(
                    step=step,
                    description=f"{proc} for {audit_area}",
                    nature="IT Control Testing",
                    sample_size=sample_size,
                    timing="Fieldwork"
                ))
                step += 1
        
        # Conclusion
        procedures.append(AuditProcedure(
            step=step,
            description="Summarize findings and develop recommendations",
            nature="Analysis",
            sample_size="N/A",
            timing="Reporting"
        ))
        
        return procedures
    
    def _get_sample_size(self, risk_level: RiskLevel) -> str:
        """Determine sample size based on risk level"""
        sample_sizes = {
            RiskLevel.LOW: "15 items",
            RiskLevel.MEDIUM: "25 items",
            RiskLevel.HIGH: "40 items",
            RiskLevel.CRITICAL: "60 items or 100%"
        }
        return sample_sizes.get(risk_level, "25 items")


class FindingDocumentor:
    """
    Document audit findings using 5Cs methodology
    """
    
    FINDING_CATEGORIES = [
        "Control Deficiency",
        "Compliance Issue", 
        "Process Inefficiency",
        "System Weakness",
        "Documentation Gap",
        "Segregation of Duties",
        "Policy Violation",
        "Fraud Risk"
    ]
    
    def create_finding(
        self,
        title: str,
        audit_area: str,
        condition: str,
        criteria: str,
        cause: str,
        effect: str,
        recommendation: str,
        risk_rating: RiskLevel = RiskLevel.MEDIUM,
        category: str = "Control Deficiency",
        owner: str = "",
        due_date: Optional[date] = None
    ) -> Finding:
        """Create a new finding"""
        finding_id = self._generate_finding_id()
        
        return Finding(
            id=finding_id,
            title=title,
            audit_area=audit_area,
            risk_rating=risk_rating,
            category=category,
            condition=condition,
            criteria=criteria,
            cause=cause,
            effect=effect,
            recommendation=recommendation,
            owner=owner,
            due_date=due_date
        )
    
    def _generate_finding_id(self) -> str:
        """Generate unique finding ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"F{timestamp}"
    
    def update_status(
        self, 
        finding: Finding, 
        new_status: FindingStatus,
        management_response: str = None
    ) -> Finding:
        """Update finding status"""
        finding.status = new_status
        
        if management_response:
            finding.management_response = management_response
        
        if new_status == FindingStatus.CLOSED:
            finding.closed_at = datetime.now()
        
        return finding
    
    def format_finding_report(self, finding: Finding) -> str:
        """Format finding for report output"""
        return f"""
## Finding: {finding.id}
### {finding.title}

**Risk Rating:** {finding.risk_rating.value}
**Category:** {finding.category}
**Audit Area:** {finding.audit_area}
**Status:** {finding.status.value}

#### Condition (What was found)
{finding.condition}

#### Criteria (What should be)
{finding.criteria}

#### Cause (Why it happened)
{finding.cause}

#### Effect (Impact)
{finding.effect}

#### Recommendation
{finding.recommendation}

---
**Owner:** {finding.owner}
**Due Date:** {finding.due_date}
**Created:** {finding.created_at.strftime('%Y-%m-%d')}
"""


class AuditService:
    """
    Main audit service orchestrating all audit operations
    """
    
    def __init__(self):
        self.risk_calculator = RiskCalculator()
        self.procedure_generator = ProcedureGenerator()
        self.finding_documentor = FindingDocumentor()
        
        # In-memory storage (replace with repository in production)
        self._risk_assessments: Dict[str, RiskAssessmentResult] = {}
        self._findings: Dict[str, Finding] = {}
        self._working_papers: Dict[str, WorkingPaper] = {}
    
    # Risk Assessment
    def assess_risk(self, input: RiskAssessmentInput) -> RiskAssessmentResult:
        """Perform risk assessment"""
        result = self.risk_calculator.calculate(input)
        self._risk_assessments[result.name] = result
        logger.info(f"Risk assessment completed for {result.name}: {result.risk_level.value}")
        return result
    
    def get_risk_assessment(self, name: str) -> Optional[RiskAssessmentResult]:
        """Get risk assessment by name"""
        return self._risk_assessments.get(name)
    
    def list_risk_assessments(self) -> List[RiskAssessmentResult]:
        """List all risk assessments"""
        return list(self._risk_assessments.values())
    
    # Audit Procedures
    def generate_procedures(
        self,
        audit_area: str,
        risk_level: RiskLevel = RiskLevel.MEDIUM,
        include_analytics: bool = True,
        include_it_controls: bool = False,
        regulations: List[str] = None
    ) -> List[AuditProcedure]:
        """Generate audit procedures"""
        return self.procedure_generator.generate(
            audit_area=audit_area,
            risk_level=risk_level,
            include_analytics=include_analytics,
            include_it_controls=include_it_controls,
            regulations=regulations
        )
    
    # Findings
    def create_finding(self, **kwargs) -> Finding:
        """Create a new finding"""
        finding = self.finding_documentor.create_finding(**kwargs)
        self._findings[finding.id] = finding
        logger.info(f"Finding created: {finding.id} - {finding.title}")
        return finding
    
    def update_finding_status(
        self, 
        finding_id: str, 
        new_status: FindingStatus,
        management_response: str = None
    ) -> Optional[Finding]:
        """Update finding status"""
        finding = self._findings.get(finding_id)
        if finding:
            finding = self.finding_documentor.update_status(
                finding, new_status, management_response
            )
            logger.info(f"Finding {finding_id} updated to {new_status.value}")
        return finding
    
    def get_finding(self, finding_id: str) -> Optional[Finding]:
        """Get finding by ID"""
        return self._findings.get(finding_id)
    
    def list_findings(
        self,
        status: Optional[FindingStatus] = None,
        risk_rating: Optional[RiskLevel] = None,
        audit_area: Optional[str] = None
    ) -> List[Finding]:
        """List findings with optional filters"""
        findings = list(self._findings.values())
        
        if status:
            findings = [f for f in findings if f.status == status]
        if risk_rating:
            findings = [f for f in findings if f.risk_rating == risk_rating]
        if audit_area:
            findings = [f for f in findings if f.audit_area == audit_area]
        
        return findings
    
    def get_overdue_findings(self) -> List[Finding]:
        """Get all overdue findings"""
        return [f for f in self._findings.values() if f.is_overdue]
    
    # Working Papers
    def create_working_paper(
        self,
        reference: str,
        template_type: str,
        audit_area: str,
        objective: str,
        preparer: str,
        reviewer: str,
        sections: Dict[str, str]
    ) -> WorkingPaper:
        """Create a working paper"""
        wp = WorkingPaper(
            reference=reference,
            template_type=template_type,
            audit_area=audit_area,
            objective=objective,
            preparer=preparer,
            reviewer=reviewer,
            sections=sections
        )
        self._working_papers[reference] = wp
        logger.info(f"Working paper created: {reference}")
        return wp
    
    def get_working_paper(self, reference: str) -> Optional[WorkingPaper]:
        """Get working paper by reference"""
        return self._working_papers.get(reference)
    
    def list_working_papers(self) -> List[WorkingPaper]:
        """List all working papers"""
        return list(self._working_papers.values())
    
    # Statistics
    def get_statistics(self) -> Dict[str, Any]:
        """Get audit statistics"""
        findings = list(self._findings.values())
        
        return {
            "total_findings": len(findings),
            "open_findings": len([f for f in findings if f.status == FindingStatus.OPEN]),
            "in_progress_findings": len([f for f in findings if f.status == FindingStatus.IN_PROGRESS]),
            "closed_findings": len([f for f in findings if f.status == FindingStatus.CLOSED]),
            "overdue_findings": len([f for f in findings if f.is_overdue]),
            "high_risk_findings": len([f for f in findings if f.risk_rating == RiskLevel.HIGH]),
            "total_risk_assessments": len(self._risk_assessments),
            "total_working_papers": len(self._working_papers),
            "findings_by_area": self._count_by_field(findings, "audit_area"),
            "findings_by_rating": self._count_by_field(findings, "risk_rating")
        }
    
    def _count_by_field(self, items: List, field: str) -> Dict[str, int]:
        """Count items by field value"""
        counts: Dict[str, int] = {}
        for item in items:
            value = getattr(item, field, None)
            if hasattr(value, 'value'):
                value = value.value
            value = str(value) if value else "Unknown"
            counts[value] = counts.get(value, 0) + 1
        return counts


# Create singleton instance
_audit_service: Optional[AuditService] = None

def get_audit_service() -> AuditService:
    """Get or create audit service singleton"""
    global _audit_service
    if _audit_service is None:
        _audit_service = AuditService()
    return _audit_service


__all__ = [
    'RiskLevel',
    'FindingStatus',
    'ControlEffectiveness',
    'RiskAssessmentInput',
    'RiskAssessmentResult',
    'Finding',
    'AuditProcedure',
    'WorkingPaper',
    'RiskCalculator',
    'ProcedureGenerator',
    'FindingDocumentor',
    'AuditService',
    'get_audit_service'
]
