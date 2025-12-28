"""
Centralized Configuration Management for AURIX.
Uses Pydantic for validation and type safety.
"""

import os
import streamlit as st
from typing import Optional, Dict, Any
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from enum import Enum


class Environment(str, Enum):
    """Application environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    GROQ = "groq"
    TOGETHER = "together"
    GOOGLE = "google"
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    MOCK = "mock"


class DatabaseSettings(BaseSettings):
    """Database configuration."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    host: str = Field(default="", validation_alias=AliasChoices("NEON_HOST", "neon_host"))
    database: str = Field(default="", validation_alias=AliasChoices("NEON_DATABASE", "neon_database"))
    user: str = Field(default="", validation_alias=AliasChoices("NEON_USER", "neon_user"))
    password: str = Field(default="", validation_alias=AliasChoices("NEON_PASSWORD", "neon_password"))
    port: int = Field(default=5432, validation_alias=AliasChoices("NEON_PORT", "neon_port"))
    pool_size: int = Field(default=10, validation_alias=AliasChoices("DATABASE_POOL_SIZE", "database_pool_size"))

    @property
    def connection_string(self) -> str:
        """Generate database connection string."""
        if not all([self.host, self.database, self.user, self.password]):
            return ""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def is_configured(self) -> bool:
        """Check if database is configured."""
        return bool(self.host and self.database and self.user and self.password)


class LLMSettings(BaseSettings):
    """LLM provider configuration."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    default_provider: LLMProvider = Field(default=LLMProvider.MOCK, validation_alias=AliasChoices("LLM_PROVIDER", "llm_provider"))
    temperature: float = Field(default=0.3, validation_alias=AliasChoices("LLM_TEMPERATURE", "llm_temperature"))
    max_tokens: int = Field(default=4096, validation_alias=AliasChoices("LLM_MAX_TOKENS", "llm_max_tokens"))

    # API Keys for various providers
    groq_api_key: str = Field(default="", validation_alias=AliasChoices("GROQ_API_KEY", "groq_api_key"))
    together_api_key: str = Field(default="", validation_alias=AliasChoices("TOGETHER_API_KEY", "together_api_key"))
    google_api_key: str = Field(default="", validation_alias=AliasChoices("GOOGLE_API_KEY", "google_api_key"))
    openrouter_api_key: str = Field(default="", validation_alias=AliasChoices("OPENROUTER_API_KEY", "openrouter_api_key"))
    anthropic_api_key: str = Field(default="", validation_alias=AliasChoices("ANTHROPIC_API_KEY", "anthropic_api_key"))
    openai_api_key: str = Field(default="", validation_alias=AliasChoices("OPENAI_API_KEY", "openai_api_key"))

    # Ollama specific
    ollama_base_url: str = Field(default="http://localhost:11434", validation_alias=AliasChoices("OLLAMA_BASE_URL", "ollama_base_url"))

    def get_api_key(self, provider: LLMProvider) -> str:
        """Get API key for specific provider."""
        key_map = {
            LLMProvider.GROQ: self.groq_api_key,
            LLMProvider.TOGETHER: self.together_api_key,
            LLMProvider.GOOGLE: self.google_api_key,
            LLMProvider.OPENROUTER: self.openrouter_api_key,
            LLMProvider.ANTHROPIC: self.anthropic_api_key,
            LLMProvider.OPENAI: self.openai_api_key,
        }
        return key_map.get(provider, "")


class RAGSettings(BaseSettings):
    """RAG engine configuration."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    chunk_size: int = Field(default=1000, validation_alias=AliasChoices("RAG_CHUNK_SIZE", "rag_chunk_size"))
    chunk_overlap: int = Field(default=200, validation_alias=AliasChoices("RAG_CHUNK_OVERLAP", "rag_chunk_overlap"))
    embedding_model: str = Field(default="all-MiniLM-L6-v2", validation_alias=AliasChoices("RAG_EMBEDDING_MODEL", "rag_embedding_model"))
    top_k_results: int = Field(default=5, validation_alias=AliasChoices("RAG_TOP_K", "rag_top_k"))
    similarity_threshold: float = Field(default=0.7, validation_alias=AliasChoices("RAG_SIMILARITY_THRESHOLD", "rag_similarity_threshold"))
    use_hybrid_search: bool = Field(default=True, validation_alias=AliasChoices("RAG_HYBRID_SEARCH", "rag_hybrid_search"))


class AuditSettings(BaseSettings):
    """Audit-specific configuration."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Risk scoring weights
    inherent_risk_weight: float = Field(default=0.6)
    control_effectiveness_weight: float = Field(default=0.4)

    # Risk thresholds
    high_risk_threshold: float = Field(default=0.7)
    medium_risk_threshold: float = Field(default=0.4)

    # Sampling
    default_sample_size: int = Field(default=25)
    min_sample_size: int = Field(default=10)
    max_sample_size: int = Field(default=100)


class AppSettings(BaseSettings):
    """Main application settings."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application
    app_name: str = Field(default="AURIX")
    app_version: str = Field(default="4.0.0")
    app_tagline: str = Field(default="Intelligent Audit. Elevated Assurance.")
    environment: Environment = Field(default=Environment.DEVELOPMENT, validation_alias=AliasChoices("APP_ENV", "app_env"))
    debug: bool = Field(default=False, validation_alias=AliasChoices("DEBUG", "debug"))

    # Logging
    log_level: str = Field(default="INFO", validation_alias=AliasChoices("LOG_LEVEL", "log_level"))
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Security
    secret_key: str = Field(default="change-me-in-production", validation_alias=AliasChoices("SECRET_KEY", "secret_key"))

    # Feature flags
    enable_visitor_tracking: bool = Field(default=True, validation_alias=AliasChoices("ENABLE_VISITOR_TRACKING", "enable_visitor_tracking"))
    enable_mock_data_fallback: bool = Field(default=True, validation_alias=AliasChoices("ENABLE_MOCK_DATA", "enable_mock_data"))

    # Sub-configurations
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    rag: RAGSettings = Field(default_factory=RAGSettings)
    audit: AuditSettings = Field(default_factory=AuditSettings)


@lru_cache()
def get_settings() -> AppSettings:
    """
    Get cached application settings.
    Uses lru_cache to ensure settings are only loaded once.
    """
    return AppSettings()


# Global settings instance
settings = get_settings()


def init_app():
    """
    Initialize application state and configurations.
    Called once at application startup.
    """
    # Initialize session state defaults
    defaults = {
        'theme': 'dark',
        'documents': [],
        'chat_history': [],
        'risk_assessments': {},
        'kri_data': {},
        'findings': [],
        'continuous_audit_rules': [],
        'working_papers': [],
        'visitor_id': None,
        'session_start': None,
        'page_views': 0,
        'visited_pages': [],
        'current_page': 'Dashboard',
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Initialize visitor tracking
    if st.session_state.visitor_id is None:
        import uuid
        from datetime import datetime
        st.session_state.visitor_id = str(uuid.uuid4())
        st.session_state.session_start = datetime.now()
    
    # Try to load secrets from Streamlit (for deployment)
    _load_streamlit_secrets()


def _load_streamlit_secrets():
    """Load secrets from Streamlit secrets management."""
    try:
        if "neon" in st.secrets:
            settings.database.host = st.secrets["neon"].get("host", "")
            settings.database.database = st.secrets["neon"].get("database", "")
            settings.database.user = st.secrets["neon"].get("user", "")
            settings.database.password = st.secrets["neon"].get("password", "")
            settings.database.port = int(st.secrets["neon"].get("port", 5432))
        
        if "llm" in st.secrets:
            settings.llm.groq_api_key = st.secrets["llm"].get("groq_api_key", "")
            settings.llm.google_api_key = st.secrets["llm"].get("google_api_key", "")
    except Exception:
        pass  # Secrets not available (local development)


def get_database_config() -> Dict[str, Any]:
    """Get database configuration dictionary."""
    return {
        'host': settings.database.host,
        'database': settings.database.database,
        'user': settings.database.user,
        'password': settings.database.password,
        'port': settings.database.port,
    }


def is_production() -> bool:
    """Check if running in production environment."""
    return settings.environment == Environment.PRODUCTION


def is_development() -> bool:
    """Check if running in development environment."""
    return settings.environment == Environment.DEVELOPMENT
