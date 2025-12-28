"""
Custom Exceptions for AURIX.
Provides specific exception types for better error handling and messaging.
"""

from typing import Optional, Dict, Any


class AurixException(Exception):
    """Base exception for AURIX application."""
    
    def __init__(
        self,
        message: str,
        code: str = "AURIX_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error": True,
            "code": self.code,
            "message": self.message,
            "details": self.details
        }


# ============================================
# Configuration Exceptions
# ============================================

class ConfigurationError(AurixException):
    """Raised when there's a configuration error."""
    
    def __init__(self, message: str, config_key: str = ""):
        super().__init__(
            message=message,
            code="CONFIG_ERROR",
            details={"config_key": config_key}
        )


class MissingAPIKeyError(ConfigurationError):
    """Raised when required API key is missing."""
    
    def __init__(self, provider: str):
        super().__init__(
            message=f"API key not configured for provider: {provider}",
            config_key=f"{provider.upper()}_API_KEY"
        )
        self.provider = provider


# ============================================
# Database Exceptions
# ============================================

class DatabaseError(AurixException):
    """Base exception for database errors."""
    
    def __init__(self, message: str, query: str = ""):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            details={"query": query[:200] if query else ""}  # Truncate for security
        )


class ConnectionError(DatabaseError):
    """Raised when database connection fails."""
    
    def __init__(self, message: str = "Failed to connect to database"):
        super().__init__(message=message)
        self.code = "DB_CONNECTION_ERROR"


class RecordNotFoundError(DatabaseError):
    """Raised when a requested record is not found."""
    
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(
            message=f"{entity_type} with ID '{entity_id}' not found"
        )
        self.code = "RECORD_NOT_FOUND"
        self.details = {"entity_type": entity_type, "entity_id": entity_id}


# ============================================
# LLM Exceptions
# ============================================

class LLMError(AurixException):
    """Base exception for LLM-related errors."""
    
    def __init__(self, message: str, provider: str = ""):
        super().__init__(
            message=message,
            code="LLM_ERROR",
            details={"provider": provider}
        )


class LLMProviderNotFoundError(LLMError):
    """Raised when specified LLM provider is not found."""
    
    def __init__(self, provider: str):
        super().__init__(
            message=f"LLM provider '{provider}' is not supported",
            provider=provider
        )
        self.code = "LLM_PROVIDER_NOT_FOUND"


class LLMRateLimitError(LLMError):
    """Raised when LLM rate limit is exceeded."""
    
    def __init__(self, provider: str, retry_after: int = 0):
        super().__init__(
            message=f"Rate limit exceeded for {provider}. Retry after {retry_after} seconds.",
            provider=provider
        )
        self.code = "LLM_RATE_LIMIT"
        self.retry_after = retry_after


class LLMResponseError(LLMError):
    """Raised when LLM returns an invalid response."""
    
    def __init__(self, provider: str, response: str = ""):
        super().__init__(
            message=f"Invalid response from {provider}",
            provider=provider
        )
        self.code = "LLM_RESPONSE_ERROR"
        self.details["response_preview"] = response[:500] if response else ""


# ============================================
# RAG Exceptions
# ============================================

class RAGError(AurixException):
    """Base exception for RAG-related errors."""
    
    def __init__(self, message: str):
        super().__init__(message=message, code="RAG_ERROR")


class DocumentProcessingError(RAGError):
    """Raised when document processing fails."""
    
    def __init__(self, filename: str, reason: str = ""):
        super().__init__(
            message=f"Failed to process document '{filename}': {reason}"
        )
        self.code = "DOCUMENT_PROCESSING_ERROR"
        self.details = {"filename": filename, "reason": reason}


class EmbeddingError(RAGError):
    """Raised when embedding generation fails."""
    
    def __init__(self, model: str, reason: str = ""):
        super().__init__(
            message=f"Failed to generate embeddings with model '{model}': {reason}"
        )
        self.code = "EMBEDDING_ERROR"


class RetrievalError(RAGError):
    """Raised when document retrieval fails."""
    
    def __init__(self, query: str, reason: str = ""):
        super().__init__(
            message=f"Failed to retrieve documents for query: {reason}"
        )
        self.code = "RETRIEVAL_ERROR"


# ============================================
# Audit Exceptions
# ============================================

class AuditError(AurixException):
    """Base exception for audit-related errors."""
    
    def __init__(self, message: str):
        super().__init__(message=message, code="AUDIT_ERROR")


class InvalidRiskFactorError(AuditError):
    """Raised when risk factor is invalid."""
    
    def __init__(self, factor_name: str, reason: str = ""):
        super().__init__(
            message=f"Invalid risk factor '{factor_name}': {reason}"
        )
        self.code = "INVALID_RISK_FACTOR"


class FindingValidationError(AuditError):
    """Raised when finding data fails validation."""
    
    def __init__(self, field: str, reason: str = ""):
        super().__init__(
            message=f"Finding validation error for field '{field}': {reason}"
        )
        self.code = "FINDING_VALIDATION_ERROR"


# ============================================
# Validation Exceptions
# ============================================

class ValidationError(AurixException):
    """Base exception for validation errors."""
    
    def __init__(self, message: str, field: str = "", value: Any = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"field": field, "value": str(value)[:100] if value else ""}
        )


class InvalidInputError(ValidationError):
    """Raised when input is invalid."""
    
    def __init__(self, field: str, expected: str, received: str = ""):
        super().__init__(
            message=f"Invalid input for '{field}'. Expected: {expected}. Received: {received}",
            field=field
        )
        self.code = "INVALID_INPUT"


class FileSizeExceededError(ValidationError):
    """Raised when file size exceeds limit."""
    
    def __init__(self, filename: str, size_mb: float, max_size_mb: float):
        super().__init__(
            message=f"File '{filename}' ({size_mb:.2f}MB) exceeds maximum size ({max_size_mb}MB)",
            field="file"
        )
        self.code = "FILE_SIZE_EXCEEDED"


class UnsupportedFileTypeError(ValidationError):
    """Raised when file type is not supported."""
    
    def __init__(self, filename: str, file_type: str, supported_types: list):
        super().__init__(
            message=f"File type '{file_type}' not supported. Supported: {', '.join(supported_types)}",
            field="file_type"
        )
        self.code = "UNSUPPORTED_FILE_TYPE"


# ============================================
# Authentication/Authorization Exceptions
# ============================================

class AuthenticationError(AurixException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, code="AUTH_ERROR")


class AuthorizationError(AurixException):
    """Raised when user is not authorized for an action."""
    
    def __init__(self, action: str, resource: str = ""):
        super().__init__(
            message=f"Not authorized to {action}" + (f" on {resource}" if resource else ""),
            code="AUTHORIZATION_ERROR",
            details={"action": action, "resource": resource}
        )


# ============================================
# Feature Exceptions
# ============================================

class FeatureDisabledError(AurixException):
    """Raised when a disabled feature is accessed."""
    
    def __init__(self, feature: str):
        super().__init__(
            message=f"Feature '{feature}' is currently disabled",
            code="FEATURE_DISABLED",
            details={"feature": feature}
        )


class ServiceUnavailableError(AurixException):
    """Raised when a service is temporarily unavailable."""
    
    def __init__(self, service: str, retry_after: int = 60):
        super().__init__(
            message=f"Service '{service}' is temporarily unavailable. Please try again later.",
            code="SERVICE_UNAVAILABLE",
            details={"service": service, "retry_after": retry_after}
        )
