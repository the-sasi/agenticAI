import os
import logging
from typing import Optional, Callable, Dict, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Provider registry - easily extensible
PROVIDERS: Dict[str, Callable] = {}


def register_provider(name: str, factory_fn: Callable):
    """Register a new LLM provider"""
    PROVIDERS[name.lower()] = factory_fn
    logger.debug(f"Registered LLM provider: {name}")


def get_available_providers() -> list:
    """Get list of available provider names"""
    return list(PROVIDERS.keys())


def create_llm(
    provider: str,
    model: Optional[str] = None,
    temperature: float = 0,
    **kwargs
):
    """
    Create an LLM instance dynamically.

    Args:
        provider: Name of the provider (e.g., "openai", "groq")
        model: Model name (optional, uses provider default if not specified)
        temperature: Temperature for generation (default: 0)
        **kwargs: Additional provider-specific arguments

    Returns:
        LLM instance compatible with LangChain interface

    Raises:
        ValueError: If provider is not registered
    """
    provider = provider.lower()

    if provider not in PROVIDERS:
        available = get_available_providers()
        raise ValueError(
            f"Unknown provider: '{provider}'. Available providers: {available}"
        )

    logger.info(f"Creating LLM: provider={provider}, model={model}, temperature={temperature}")
    return PROVIDERS[provider](model=model, temperature=temperature, **kwargs)


# =============================================================================
# Provider Implementations
# =============================================================================

def _create_openai(
    model: Optional[str] = None,
    temperature: float = 0,
    **kwargs
):
    """Create OpenAI LLM instance"""
    from langchain_openai import ChatOpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    return ChatOpenAI(
        api_key=api_key,
        model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=temperature,
        **kwargs
    )


def _create_groq(
    model: Optional[str] = None,
    temperature: float = 0,
    **kwargs
):
    """Create Groq LLM instance"""
    from langchain_groq import ChatGroq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    return ChatGroq(
        api_key=api_key,
        model=model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=temperature,
        **kwargs
    )


# =============================================================================
# Register Default Providers
# =============================================================================

register_provider("openai", _create_openai)
register_provider("groq", _create_groq)
