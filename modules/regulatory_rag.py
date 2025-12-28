"""
Regulatory RAG Module for AURIX 2026.
RAG-based compliance validation against Indonesian regulations (OJK, BI, BPKH).

Features:
- Regulatory knowledge base with OJK, BI, BPKH regulations
- Compliance validation with scoring
- ESG taxonomy classification (POJK 6/2022)
- Sharia compliance checks (BPKH)
"""

import streamlit as st
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    REQUIRES_REVIEW = "requires_review"
    UNKNOWN = "unknown"


class ESGCategory(str, Enum):
    GREEN = "green"
    TRANSITION = "transition"
    BROWN = "brown"
    NEUTRAL = "neutral"


@dataclass
class RegulatoryReference:
    """Reference to a specific regulation."""
    regulation_id: str
    title: str
    article: str
    excerpt: str
    issuer: str  # OJK, BI, BPKH
    year: int
    relevance_score: float


@dataclass
class ComplianceResult:
    """Result of compliance validation."""
    statement: str
    overall_status: ComplianceStatus
    compliance_score: float  # 0-100
    matched_regulations: List[RegulatoryReference]
    risk_factors: List[str]
    recommendations: List[str]
    esg_category: Optional[ESGCategory] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


# =============================================================================
# REGULATORY KNOWLEDGE BASE
# =============================================================================

REGULATORY_KNOWLEDGE_BASE = {
    # POJK 6/2022 - Taksonomi Berkelanjutan Indonesia (ESG Taxonomy)
    "POJK-6-2022": {
        "title": "Peraturan OJK tentang Taksonomi Keuangan Berkelanjutan Indonesia",
        "issuer": "OJK",
        "year": 2022,
        "articles": {
            "Article 4": {
                "excerpt": "Kegiatan usaha hijau meliputi energi terbarukan, efisiensi energi, pengelolaan air berkelanjutan, dan adaptasi perubahan iklim.",
                "keywords": ["renewable", "solar", "wind", "hydro", "energy efficiency", "sustainable", "green bond"]
            },
            "Article 5": {
                "excerpt": "Kegiatan usaha coklat (brown) yang dikecualikan meliputi pertambangan batubara, pembangkit listrik tenaga batubara, eksplorasi minyak dan gas hulu, dan deforestasi.",
                "keywords": ["coal", "batubara", "deforestation", "oil exploration", "fossil fuel"]
            },
            "Article 6": {
                "excerpt": "Kegiatan transisi mencakup usaha yang memiliki rencana dekarbonisasi yang kredibel menuju net-zero.",
                "keywords": ["transition", "decarbonization", "net-zero", "carbon reduction"]
            }
        }
    },
    
    # POJK 51/2017 - Keuangan Berkelanjutan
    "POJK-51-2017": {
        "title": "Peraturan OJK tentang Penerapan Keuangan Berkelanjutan",
        "issuer": "OJK",
        "year": 2017,
        "articles": {
            "Article 3": {
                "excerpt": "Lembaga Jasa Keuangan wajib menyusun Rencana Aksi Keuangan Berkelanjutan (RAKB).",
                "keywords": ["RAKB", "sustainability", "action plan", "sustainable finance"]
            },
            "Article 7": {
                "excerpt": "Bank kategori BUKU 3 dan BUKU 4 wajib memiliki portofolio hijau minimal 20% dari total kredit pada tahun 2025.",
                "keywords": ["green portfolio", "20%", "BUKU 3", "BUKU 4", "target"]
            },
            "Article 10": {
                "excerpt": "Lembaga Jasa Keuangan wajib menyusun Laporan Keberlanjutan (Sustainability Report) tahunan.",
                "keywords": ["sustainability report", "ESG disclosure", "annual report"]
            }
        }
    },
    
    # PBI 23/2021 - Manajemen Risiko
    "PBI-23-2021": {
        "title": "Peraturan Bank Indonesia tentang Manajemen Risiko Bank Umum",
        "issuer": "BI",
        "year": 2021,
        "articles": {
            "Article 15": {
                "excerpt": "Bank wajib mengintegrasikan risiko perubahan iklim dalam kerangka manajemen risiko, meliputi risiko fisik dan risiko transisi.",
                "keywords": ["climate risk", "physical risk", "transition risk", "stress testing"]
            },
            "Article 18": {
                "excerpt": "Bank wajib melakukan stress testing terhadap eksposur yang rentan terhadap risiko perubahan iklim.",
                "keywords": ["stress testing", "climate scenario", "exposure"]
            }
        }
    },
    
    # BPKH - Sharia Compliance
    "BPKH-2023": {
        "title": "Pedoman Investasi Dana Haji Sesuai Prinsip Syariah",
        "issuer": "BPKH",
        "year": 2023,
        "articles": {
            "Article 3": {
                "excerpt": "Investasi dana haji harus bebas dari unsur riba (bunga), gharar (ketidakpastian berlebihan), dan maysir (perjudian).",
                "keywords": ["riba", "gharar", "maysir", "sharia", "halal", "interest-free"]
            },
            "Article 5": {
                "excerpt": "Sektor usaha yang dilarang meliputi: alkohol, perjudian, produk babi, tembakau, senjata, dan hiburan yang tidak sesuai syariah.",
                "keywords": ["alcohol", "gambling", "pork", "tobacco", "weapons", "entertainment", "haram"]
            },
            "Article 8": {
                "excerpt": "Rasio hutang berbasis bunga tidak boleh melebihi 45% dari total aset.",
                "keywords": ["debt ratio", "interest-based debt", "45%", "leverage"]
            }
        }
    },
    
    # POJK 15/2022 - Bank Umum Syariah
    "POJK-15-2022": {
        "title": "Peraturan OJK tentang Bank Umum Syariah",
        "issuer": "OJK",
        "year": 2022,
        "articles": {
            "Article 20": {
                "excerpt": "Bank Syariah wajib memiliki Dewan Pengawas Syariah (DPS) yang bertugas mengawasi kepatuhan prinsip syariah.",
                "keywords": ["DPS", "sharia board", "sharia compliance", "supervision"]
            },
            "Article 35": {
                "excerpt": "Akad pembiayaan wajib sesuai dengan prinsip syariah yang diatur dalam fatwa DSN-MUI.",
                "keywords": ["akad", "fatwa", "DSN-MUI", "contract", "sharia principle"]
            }
        }
    }
}


# ESG Classification Keywords
ESG_KEYWORDS = {
    ESGCategory.GREEN: [
        "renewable energy", "solar", "wind", "hydro", "geothermal",
        "energy efficiency", "green building", "sustainable transport",
        "electric vehicle", "sustainable agriculture", "organic",
        "water treatment", "waste management", "recycling",
        "biodiversity", "conservation", "reforestation"
    ],
    ESGCategory.BROWN: [
        "coal", "batubara", "coal mining", "coal-fired power",
        "upstream oil", "oil exploration", "fossil fuel",
        "deforestation", "illegal logging", "peat destruction"
    ],
    ESGCategory.TRANSITION: [
        "natural gas", "LNG", "decarbonization", "carbon capture",
        "emission reduction", "energy transition", "phase-out plan",
        "climate commitment", "net-zero target"
    ]
}


# =============================================================================
# REGULATORY VALIDATOR CLASS
# =============================================================================

class RegulatoryValidator:
    """
    Validates statements against Indonesian regulatory requirements.
    Uses keyword-based matching (in production, would use vector embeddings).
    """
    
    def __init__(self):
        self.knowledge_base = REGULATORY_KNOWLEDGE_BASE
        self.esg_keywords = ESG_KEYWORDS
    
    def _search_regulations(self, query: str, top_k: int = 5) -> List[RegulatoryReference]:
        """Search regulations matching the query."""
        query_lower = query.lower()
        matches = []
        
        for reg_id, reg_data in self.knowledge_base.items():
            for article_name, article_data in reg_data["articles"].items():
                # Calculate relevance score based on keyword matches
                keywords = article_data.get("keywords", [])
                matched_keywords = sum(1 for kw in keywords if kw.lower() in query_lower)
                
                if matched_keywords > 0:
                    relevance = matched_keywords / len(keywords) if keywords else 0
                    
                    matches.append(RegulatoryReference(
                        regulation_id=reg_id,
                        title=reg_data["title"],
                        article=article_name,
                        excerpt=article_data["excerpt"],
                        issuer=reg_data["issuer"],
                        year=reg_data["year"],
                        relevance_score=round(relevance, 2)
                    ))
        
        # Sort by relevance and return top_k
        matches.sort(key=lambda x: -x.relevance_score)
        return matches[:top_k]
    
    def _classify_esg(self, statement: str) -> ESGCategory:
        """Classify statement into ESG category."""
        statement_lower = statement.lower()
        
        # Check for brown keywords first (exclusions)
        for keyword in self.esg_keywords[ESGCategory.BROWN]:
            if keyword.lower() in statement_lower:
                return ESGCategory.BROWN
        
        # Check for green keywords
        green_matches = sum(1 for kw in self.esg_keywords[ESGCategory.GREEN] 
                          if kw.lower() in statement_lower)
        
        # Check for transition keywords
        transition_matches = sum(1 for kw in self.esg_keywords[ESGCategory.TRANSITION] 
                                if kw.lower() in statement_lower)
        
        if green_matches > transition_matches:
            return ESGCategory.GREEN
        elif transition_matches > 0:
            return ESGCategory.TRANSITION
        
        return ESGCategory.NEUTRAL
    
    def _calculate_compliance_score(
        self,
        statement: str,
        regulations: List[RegulatoryReference],
        esg_category: ESGCategory
    ) -> Tuple[float, ComplianceStatus, List[str]]:
        """Calculate compliance score and determine status."""
        statement_lower = statement.lower()
        risks = []
        base_score = 70  # Start with base score
        
        # ESG-based scoring
        if esg_category == ESGCategory.BROWN:
            base_score = 20
            risks.append("Activity classified as BROWN under POJK 6/2022 ESG Taxonomy")
            risks.append("May be excluded from sustainable finance portfolios")
        elif esg_category == ESGCategory.GREEN:
            base_score = 95
        elif esg_category == ESGCategory.TRANSITION:
            base_score = 75
            risks.append("Activity requires credible decarbonization plan per POJK 6/2022")
        
        # Check for specific red flags
        red_flags = {
            "coal": ("High carbon intensity activity", -30),
            "gambling": ("Sharia-prohibited activity (maysir)", -40),
            "alcohol": ("Sharia-prohibited activity (haram)", -40),
            "interest": ("Potential riba concern for Islamic finance", -15),
            "deforestation": ("Environmental violation risk", -35),
            "tobacco": ("ESG exclusion list activity", -20),
        }
        
        for flag, (risk_msg, penalty) in red_flags.items():
            if flag in statement_lower:
                base_score += penalty
                if risk_msg not in risks:
                    risks.append(risk_msg)
        
        # Positive factors
        positive_factors = {
            "renewable": ("Aligned with green taxonomy", +10),
            "solar": ("Clean energy investment", +10),
            "sustainability": ("ESG-aligned activity", +5),
            "halal": ("Sharia-compliant", +5),
            "green bond": ("Sustainable finance instrument", +10),
        }
        
        for factor, (_, bonus) in positive_factors.items():
            if factor in statement_lower:
                base_score += bonus
        
        # Clamp score to 0-100
        final_score = max(0, min(100, base_score))
        
        # Determine status
        if final_score >= 80:
            status = ComplianceStatus.COMPLIANT
        elif final_score >= 50:
            status = ComplianceStatus.REQUIRES_REVIEW
        else:
            status = ComplianceStatus.NON_COMPLIANT
        
        return final_score, status, risks
    
    def _generate_recommendations(
        self,
        status: ComplianceStatus,
        esg_category: ESGCategory,
        risks: List[str]
    ) -> List[str]:
        """Generate recommendations based on compliance status."""
        recommendations = []
        
        if status == ComplianceStatus.NON_COMPLIANT:
            recommendations.append("Seek legal counsel for regulatory impact assessment")
            recommendations.append("Consider alternative business activities that align with regulations")
            
            if esg_category == ESGCategory.BROWN:
                recommendations.append("Develop transition plan with clear decarbonization timeline")
                recommendations.append("Assess stranded asset risk for current investments")
        
        elif status == ComplianceStatus.REQUIRES_REVIEW:
            recommendations.append("Document compliance rationale and supporting evidence")
            recommendations.append("Consult with Compliance team for formal assessment")
            
            if "sharia" in str(risks).lower():
                recommendations.append("Obtain fatwa from Dewan Syariah Nasional (DSN-MUI)")
        
        else:  # COMPLIANT
            recommendations.append("Maintain documentation for regulatory reporting")
            recommendations.append("Consider highlighting in Sustainability Report")
        
        return recommendations
    
    def validate(self, statement: str) -> ComplianceResult:
        """
        Validate a statement against Indonesian regulations.
        
        Args:
            statement: Business activity or policy statement to validate
        
        Returns:
            ComplianceResult with status, score, and recommendations
        """
        # Search for relevant regulations
        regulations = self._search_regulations(statement)
        
        # Classify ESG category
        esg_category = self._classify_esg(statement)
        
        # Calculate score and status
        score, status, risks = self._calculate_compliance_score(
            statement, regulations, esg_category
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(status, esg_category, risks)
        
        return ComplianceResult(
            statement=statement,
            overall_status=status,
            compliance_score=score,
            matched_regulations=regulations,
            risk_factors=risks,
            recommendations=recommendations,
            esg_category=esg_category
        )
    
    def get_regulation_summary(self, regulation_id: str) -> Optional[Dict]:
        """Get summary of a specific regulation."""
        return self.knowledge_base.get(regulation_id)
    
    def list_all_regulations(self) -> List[Dict]:
        """List all regulations in knowledge base."""
        result = []
        for reg_id, reg_data in self.knowledge_base.items():
            result.append({
                "id": reg_id,
                "title": reg_data["title"],
                "issuer": reg_data["issuer"],
                "year": reg_data["year"],
                "article_count": len(reg_data["articles"])
            })
        return result


# =============================================================================
# SAMPLE QUERIES FOR TESTING
# =============================================================================

SAMPLE_QUERIES = [
    {
        "query": "We plan to invest in a new coal mining project in Kalimantan",
        "expected_status": "non_compliant",
        "category": "brown"
    },
    {
        "query": "Our company is developing a solar panel manufacturing facility",
        "expected_status": "compliant",
        "category": "green"
    },
    {
        "query": "We are transitioning our fleet from diesel to LNG vehicles",
        "expected_status": "requires_review",
        "category": "transition"
    },
    {
        "query": "The investment portfolio includes alcohol distributors",
        "expected_status": "non_compliant",
        "category": "sharia_violation"
    },
    {
        "query": "We are issuing a green bond to fund sustainable water treatment plants",
        "expected_status": "compliant",
        "category": "green"
    },
    {
        "query": "Our palm oil plantation has RSPO certification",
        "expected_status": "requires_review",
        "category": "transition"
    }
]


# Export
__all__ = [
    "RegulatoryValidator",
    "ComplianceResult",
    "ComplianceStatus",
    "ESGCategory",
    "RegulatoryReference",
    "REGULATORY_KNOWLEDGE_BASE",
    "SAMPLE_QUERIES"
]
