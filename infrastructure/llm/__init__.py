"""
LLM Infrastructure Layer
Strategy pattern implementation for multiple LLM providers
Supports: Groq, Together AI, OpenRouter, Google AI, Ollama, Anthropic, OpenAI
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Generator, Callable
from enum import Enum
import logging
import json
import os

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers"""
    GROQ = "groq"
    TOGETHER = "together"
    OPENROUTER = "openrouter"
    GOOGLE = "google"
    OLLAMA = "ollama"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    MOCK = "mock"


@dataclass
class LLMConfig:
    """Configuration for LLM provider"""
    provider: LLMProvider
    api_key: Optional[str] = None
    model: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 4096
    timeout: int = 60
    
    # Provider-specific defaults
    DEFAULT_MODELS: Dict[LLMProvider, str] = field(default_factory=lambda: {
        LLMProvider.GROQ: "llama-3.3-70b-versatile",
        LLMProvider.TOGETHER: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        LLMProvider.OPENROUTER: "google/gemma-2-9b-it:free",
        LLMProvider.GOOGLE: "gemini-2.0-flash-exp",
        LLMProvider.OLLAMA: "llama3.2",
        LLMProvider.ANTHROPIC: "claude-sonnet-4-20250514",
        LLMProvider.OPENAI: "gpt-4o",
        LLMProvider.MOCK: "mock-model"
    })
    
    def get_model(self) -> str:
        """Get model name, using default if not specified"""
        return self.model or self.DEFAULT_MODELS.get(self.provider, "")


@dataclass
class LLMResponse:
    """Standardized response from LLM"""
    content: str
    model: str
    provider: str
    tokens_used: int = 0
    finish_reason: str = "stop"
    latency_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return self.content


@dataclass
class Message:
    """Chat message structure"""
    role: str  # "system", "user", "assistant"
    content: str
    
    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class LLMStrategy(ABC):
    """
    Abstract strategy for LLM providers
    Implements Strategy Pattern for interchangeable LLM backends
    """
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Provider name for identification"""
        pass
    
    @property
    @abstractmethod
    def available_models(self) -> List[str]:
        """List of available models"""
        pass
    
    @abstractmethod
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> LLMResponse:
        """Generate response from messages"""
        pass
    
    def stream(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> Generator[str, None, None]:
        """Stream response (default implementation uses non-streaming)"""
        response = self.generate(messages, temperature, max_tokens, **kwargs)
        yield response.content
    
    def simple_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Simplified generation with prompt string"""
        messages = []
        if system_prompt:
            messages.append(Message("system", system_prompt))
        messages.append(Message("user", prompt))
        return self.generate(messages, **kwargs)


class GroqStrategy(LLMStrategy):
    """Groq LLM Strategy - FASTEST FREE API"""
    
    BASE_URL = "https://api.groq.com/openai/v1"
    
    MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
    
    @property
    def provider_name(self) -> str:
        return "Groq"
    
    @property
    def available_models(self) -> List[str]:
        return self.MODELS
    
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> LLMResponse:
        import requests
        import time
        
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [m.to_dict() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        latency = (time.time() - start_time) * 1000
        
        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            model=self.model,
            provider=self.provider_name,
            tokens_used=result.get("usage", {}).get("total_tokens", 0),
            finish_reason=result["choices"][0].get("finish_reason", "stop"),
            latency_ms=latency,
            metadata={"usage": result.get("usage", {})}
        )
    
    def stream(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> Generator[str, None, None]:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [m.to_dict() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            stream=True,
            timeout=60
        )
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: ') and line != 'data: [DONE]':
                    try:
                        chunk = json.loads(line[6:])
                        delta = chunk["choices"][0]["delta"]
                        if delta.get("content"):
                            yield delta["content"]
                    except:
                        pass


class TogetherStrategy(LLMStrategy):
    """Together AI Strategy - Free credits on signup"""
    
    BASE_URL = "https://api.together.xyz/v1"
    
    MODELS = [
        "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "Qwen/Qwen2.5-72B-Instruct-Turbo",
        "deepseek-ai/DeepSeek-V3"
    ]
    
    def __init__(self, api_key: str, model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"):
        self.api_key = api_key
        self.model = model
    
    @property
    def provider_name(self) -> str:
        return "Together AI"
    
    @property
    def available_models(self) -> List[str]:
        return self.MODELS
    
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> LLMResponse:
        import requests
        import time
        
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [m.to_dict() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        latency = (time.time() - start_time) * 1000
        
        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            model=self.model,
            provider=self.provider_name,
            tokens_used=result.get("usage", {}).get("total_tokens", 0),
            finish_reason=result["choices"][0].get("finish_reason", "stop"),
            latency_ms=latency
        )


class OpenRouterStrategy(LLMStrategy):
    """OpenRouter Strategy - Multi-model access"""
    
    BASE_URL = "https://openrouter.ai/api/v1"
    
    MODELS = [
        "google/gemma-2-9b-it:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "meta-llama/llama-3.1-70b-instruct"
    ]
    
    def __init__(self, api_key: str, model: str = "google/gemma-2-9b-it:free"):
        self.api_key = api_key
        self.model = model
    
    @property
    def provider_name(self) -> str:
        return "OpenRouter"
    
    @property
    def available_models(self) -> List[str]:
        return self.MODELS
    
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> LLMResponse:
        import requests
        import time
        
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://aurix-audit.app",
            "X-Title": "AURIX Audit Platform"
        }
        
        data = {
            "model": self.model,
            "messages": [m.to_dict() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        latency = (time.time() - start_time) * 1000
        
        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            model=self.model,
            provider=self.provider_name,
            tokens_used=result.get("usage", {}).get("total_tokens", 0),
            latency_ms=latency
        )


class GoogleStrategy(LLMStrategy):
    """Google AI Studio Strategy - Free Gemini"""
    
    MODELS = [
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash-exp"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    @property
    def provider_name(self) -> str:
        return "Google AI"
    
    @property
    def available_models(self) -> List[str]:
        return self.MODELS
    
    def _get_client(self):
        if self._client is None:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai.GenerativeModel(self.model)
        return self._client
    
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> LLMResponse:
        import time
        
        start_time = time.time()
        client = self._get_client()
        
        # Convert messages to Gemini format
        prompt_parts = []
        for msg in messages:
            if msg.role == "system":
                prompt_parts.insert(0, msg.content + "\n\n")
            else:
                prompt_parts.append(msg.content)
        
        full_prompt = "\n".join(prompt_parts)
        
        response = client.generate_content(
            full_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )
        
        latency = (time.time() - start_time) * 1000
        
        return LLMResponse(
            content=response.text,
            model=self.model,
            provider=self.provider_name,
            latency_ms=latency
        )


class OllamaStrategy(LLMStrategy):
    """Ollama Strategy - Local LLMs"""
    
    MODELS = [
        "llama3.2",
        "llama3.1",
        "mistral",
        "qwen2.5",
        "deepseek-r1",
        "gemma2"
    ]
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url
        self.model = model
    
    @property
    def provider_name(self) -> str:
        return "Ollama"
    
    @property
    def available_models(self) -> List[str]:
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.ok:
                models = response.json().get("models", [])
                return [m["name"] for m in models]
        except:
            pass
        return self.MODELS
    
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> LLMResponse:
        import requests
        import time
        
        start_time = time.time()
        
        # Extract system and user messages
        system = ""
        prompt = ""
        for msg in messages:
            if msg.role == "system":
                system = msg.content
            elif msg.role == "user":
                prompt = msg.content
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=data,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        
        latency = (time.time() - start_time) * 1000
        
        return LLMResponse(
            content=result.get("response", ""),
            model=self.model,
            provider=self.provider_name,
            tokens_used=result.get("eval_count", 0),
            latency_ms=latency
        )


class MockStrategy(LLMStrategy):
    """Mock Strategy for testing without API keys"""
    
    def __init__(self, model: str = "mock-model"):
        self.model = model
    
    @property
    def provider_name(self) -> str:
        return "Mock"
    
    @property
    def available_models(self) -> List[str]:
        return ["mock-model"]
    
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ) -> LLMResponse:
        # Get last user message for context
        user_msg = next((m.content for m in reversed(messages) if m.role == "user"), "")
        
        response_content = self._generate_mock_response(user_msg)
        
        return LLMResponse(
            content=response_content,
            model=self.model,
            provider=self.provider_name,
            tokens_used=len(user_msg.split()) + len(response_content.split()),
            metadata={"mock": True}
        )
    
    def _generate_mock_response(self, prompt: str) -> str:
        """Generate contextual mock response"""
        prompt_lower = prompt.lower()
        
        if "risk" in prompt_lower:
            return """## Risk Assessment Analysis

Based on the analysis, here are the identified risk areas:

### High Risk Areas:
1. **Credit Risk Management** - NPL monitoring needs improvement
2. **IT Security Controls** - User access management gaps
3. **AML/CFT Compliance** - Transaction monitoring effectiveness

### Recommendations:
- Strengthen credit monitoring procedures
- Implement automated access review
- Update transaction monitoring parameters

*Response generated by AURIX Mock LLM*"""

        elif "audit" in prompt_lower or "procedure" in prompt_lower:
            return """## Audit Procedures

| Step | Procedure | Nature | Sample |
|------|-----------|--------|--------|
| 1 | Review policy documentation | Document Review | All |
| 2 | Walkthrough with stakeholders | Inquiry | N/A |
| 3 | Test sample transactions | Testing | 25 |
| 4 | Verify segregation of duties | Observation | Key users |
| 5 | Analyze exception reports | Analytics | 100% |

*Response generated by AURIX Mock LLM*"""

        else:
            return """## Analysis Results

Based on the provided context:

### Key Findings:
1. Areas requiring attention identified
2. Current controls have strengths and gaps
3. Regulatory compliance generally maintained

### Next Steps:
1. Prioritize high-risk areas
2. Develop remediation plan
3. Schedule regular reviews

*Response generated by AURIX Mock LLM*"""


class LLMClient:
    """
    Main LLM Client using Strategy Pattern
    Provides unified interface to all LLM providers
    """
    
    STRATEGIES: Dict[LLMProvider, type] = {
        LLMProvider.GROQ: GroqStrategy,
        LLMProvider.TOGETHER: TogetherStrategy,
        LLMProvider.OPENROUTER: OpenRouterStrategy,
        LLMProvider.GOOGLE: GoogleStrategy,
        LLMProvider.OLLAMA: OllamaStrategy,
        LLMProvider.MOCK: MockStrategy
    }
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self._strategy = self._create_strategy()
    
    def _create_strategy(self) -> LLMStrategy:
        """Create appropriate strategy based on config"""
        strategy_class = self.STRATEGIES.get(self.config.provider)
        
        if not strategy_class:
            logger.warning(f"Unknown provider {self.config.provider}, using Mock")
            return MockStrategy()
        
        # Build kwargs for strategy
        kwargs = {"model": self.config.get_model()}
        
        if self.config.api_key:
            kwargs["api_key"] = self.config.api_key
        
        if self.config.provider == LLMProvider.OLLAMA and self.config.base_url:
            kwargs["base_url"] = self.config.base_url
        
        try:
            return strategy_class(**kwargs)
        except Exception as e:
            logger.error(f"Failed to create {self.config.provider} strategy: {e}")
            return MockStrategy()
    
    @property
    def provider_name(self) -> str:
        return self._strategy.provider_name
    
    @property
    def available_models(self) -> List[str]:
        return self._strategy.available_models
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate response from prompt"""
        messages = []
        if system_prompt:
            messages.append(Message("system", system_prompt))
        messages.append(Message("user", prompt))

        # Extract known params to avoid duplicate keyword arguments
        temperature = kwargs.pop("temperature", self.config.temperature)
        max_tokens = kwargs.pop("max_tokens", self.config.max_tokens)

        return self._strategy.generate(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    def chat(self, messages: List[Message], **kwargs) -> LLMResponse:
        """Chat with message history"""
        # Extract known params to avoid duplicate keyword arguments
        temperature = kwargs.pop("temperature", self.config.temperature)
        max_tokens = kwargs.pop("max_tokens", self.config.max_tokens)

        return self._strategy.generate(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        """Stream response"""
        messages = []
        if system_prompt:
            messages.append(Message("system", system_prompt))
        messages.append(Message("user", prompt))
        
        yield from self._strategy.stream(
            messages,
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
            **kwargs
        )


def create_llm_client(
    provider: str = "groq",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs
) -> LLMClient:
    """Factory function to create LLM client"""
    try:
        provider_enum = LLMProvider(provider.lower())
    except ValueError:
        logger.warning(f"Unknown provider '{provider}', using mock")
        provider_enum = LLMProvider.MOCK
    
    # Try to get API key from environment if not provided
    env_keys = {
        LLMProvider.GROQ: "GROQ_API_KEY",
        LLMProvider.TOGETHER: "TOGETHER_API_KEY",
        LLMProvider.OPENROUTER: "OPENROUTER_API_KEY",
        LLMProvider.GOOGLE: "GOOGLE_API_KEY",
        LLMProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
        LLMProvider.OPENAI: "OPENAI_API_KEY"
    }
    
    if not api_key and provider_enum in env_keys:
        api_key = os.getenv(env_keys[provider_enum])
    
    config = LLMConfig(
        provider=provider_enum,
        api_key=api_key,
        model=model,
        **kwargs
    )
    
    return LLMClient(config)


# Provider metadata for UI
LLM_PROVIDER_INFO = {
    "groq": {
        "name": "Groq",
        "description": "🚀 FASTEST FREE API - Llama 3.3, Mixtral",
        "free": True,
        "url": "https://console.groq.com/keys"
    },
    "together": {
        "name": "Together AI",
        "description": "🆓 Free credits - Llama, Qwen, DeepSeek",
        "free": True,
        "url": "https://api.together.xyz/"
    },
    "openrouter": {
        "name": "OpenRouter",
        "description": "🌐 Multi-model access - Free & Paid",
        "free": True,
        "url": "https://openrouter.ai/keys"
    },
    "google": {
        "name": "Google AI Studio",
        "description": "🆓 Free Gemini 2.0 Flash",
        "free": True,
        "url": "https://aistudio.google.com/app/apikey"
    },
    "ollama": {
        "name": "Ollama (Local)",
        "description": "💻 Run LLMs locally - FREE",
        "free": True,
        "url": "https://ollama.ai/"
    },
    "mock": {
        "name": "Mock (Demo)",
        "description": "🧪 Testing without API key",
        "free": True,
        "url": None
    }
}


__all__ = [
    'LLMProvider',
    'LLMConfig',
    'LLMResponse',
    'Message',
    'LLMStrategy',
    'LLMClient',
    'create_llm_client',
    'LLM_PROVIDER_INFO',
    'GroqStrategy',
    'TogetherStrategy',
    'OpenRouterStrategy',
    'GoogleStrategy',
    'OllamaStrategy',
    'MockStrategy'
]
