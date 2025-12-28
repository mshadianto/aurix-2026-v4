"""
AURIX v4.0 Test Suite
Basic tests for module imports and functionality.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestImports:
    """Test that all modules can be imported."""
    
    def test_import_app_modules(self):
        """Test app module imports."""
        from app import config
        from app import constants
        from app import router
        assert config is not None
        assert constants is not None
        assert router is not None
    
    def test_import_data_modules(self):
        """Test data module imports."""
        from data.seeds import REGULATIONS, AUDIT_UNIVERSE, KRI_INDICATORS
        assert len(REGULATIONS) > 0
        assert len(AUDIT_UNIVERSE) > 0
        assert len(KRI_INDICATORS) > 0
    
    def test_import_utils(self):
        """Test utility imports."""
        from utils.logger import get_logger
        from utils.exceptions import AurixException
        assert get_logger is not None
        assert AurixException is not None


class TestSeedData:
    """Test seed data integrity."""
    
    def test_regulations_structure(self):
        """Test regulations data structure."""
        from data.seeds import REGULATIONS
        
        for category, regs in REGULATIONS.items():
            assert isinstance(category, str)
            assert isinstance(regs, list)
            for reg in regs:
                assert 'code' in reg
                assert 'title' in reg
                assert 'category' in reg
    
    def test_audit_universe_structure(self):
        """Test audit universe data structure."""
        from data.seeds import AUDIT_UNIVERSE
        
        for category, areas in AUDIT_UNIVERSE.items():
            assert isinstance(category, str)
            assert isinstance(areas, list)
            assert len(areas) > 0
    
    def test_kri_indicators_structure(self):
        """Test KRI indicators data structure."""
        from data.seeds import KRI_INDICATORS
        
        for category, indicators in KRI_INDICATORS.items():
            assert isinstance(category, str)
            assert isinstance(indicators, list)
            for ind in indicators:
                assert 'name' in ind
                assert 'threshold' in ind
                assert 'unit' in ind
                assert 'good_direction' in ind
    
    def test_fraud_red_flags_structure(self):
        """Test fraud red flags data structure."""
        from data.seeds import FRAUD_RED_FLAGS
        
        for category, flags in FRAUD_RED_FLAGS.items():
            assert isinstance(category, str)
            assert isinstance(flags, list)
            assert len(flags) > 0
    
    def test_continuous_audit_rules(self):
        """Test continuous audit rules structure."""
        from data.seeds import CONTINUOUS_AUDIT_RULES
        
        assert len(CONTINUOUS_AUDIT_RULES) > 0
        for rule in CONTINUOUS_AUDIT_RULES:
            assert 'id' in rule
            assert 'name' in rule
            assert 'description' in rule
            assert 'category' in rule


class TestConstants:
    """Test application constants."""
    
    def test_app_constants(self):
        """Test basic app constants."""
        from app.constants import APP_NAME, APP_VERSION
        
        assert APP_NAME == "AURIX"
        assert APP_VERSION is not None
    
    def test_llm_provider_info(self):
        """Test LLM provider information."""
        from app.constants import LLM_PROVIDER_INFO
        
        assert 'groq' in LLM_PROVIDER_INFO
        assert 'together' in LLM_PROVIDER_INFO
        assert 'google' in LLM_PROVIDER_INFO
    
    def test_finding_severity(self):
        """Test finding severity levels."""
        from app.constants import FINDING_SEVERITY
        
        assert 'CRITICAL' in FINDING_SEVERITY
        assert 'HIGH' in FINDING_SEVERITY
        assert 'MEDIUM' in FINDING_SEVERITY
        assert 'LOW' in FINDING_SEVERITY


class TestHelperFunctions:
    """Test helper functions in seed data."""
    
    def test_get_regulations_by_category(self):
        """Test getting regulations by category."""
        from data.seeds import get_regulations_by_category
        
        ojk_regs = get_regulations_by_category("OJK")
        assert len(ojk_regs) > 0
        
        invalid = get_regulations_by_category("INVALID")
        assert len(invalid) == 0
    
    def test_get_audit_areas_by_category(self):
        """Test getting audit areas by category."""
        from data.seeds import get_audit_areas_by_category
        
        risk_areas = get_audit_areas_by_category("Risk Management")
        assert len(risk_areas) > 0
    
    def test_get_all_audit_areas(self):
        """Test getting all audit areas."""
        from data.seeds import get_all_audit_areas
        
        all_areas = get_all_audit_areas()
        assert len(all_areas) > 10  # Should have many areas
    
    def test_get_system_prompt(self):
        """Test getting system prompts."""
        from data.seeds import get_system_prompt
        
        default = get_system_prompt("default")
        assert len(default) > 0
        
        risk = get_system_prompt("risk_assessment")
        assert len(risk) > 0
        
        # Should fallback to default
        fallback = get_system_prompt("nonexistent")
        assert fallback == get_system_prompt("default")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
