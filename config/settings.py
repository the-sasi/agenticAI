import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Directory configuration
SOURCE_DIR = os.getenv("SOURCE_DIR", "./input_files")
DEST_DIR = os.getenv("DEST_DIR", "./output_files")

# File categories
CATEGORIES = {
    "Images": ["png", "jpg", "jpeg", "gif", "bmp", "svg"],
    "Documents": ["pdf", "docx", "txt", "doc", "xlsx", "pptx"],
    "Code": ["py", "js", "ts", "java", "cpp", "c", "go", "rs"],
    "Others": []
}

# Agent configuration
MAX_STEPS = 20

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
LLM_MODEL = os.getenv("LLM_MODEL")  # None = use provider default
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))

# Provider-specific API key mapping
PROVIDER_API_KEYS = {
    "openai": "OPENAI_API_KEY",
    "groq": "GROQ_API_KEY",
}


def get_required_api_key(provider: str) -> str:
    """Get the required API key env var name for a provider"""
    return PROVIDER_API_KEYS.get(provider.lower(), f"{provider.upper()}_API_KEY")


def validate_env():
    """
    Validate that all required environment variables are set
    """
    missing = []

    # Validate API key for the configured provider
    api_key_var = get_required_api_key(LLM_PROVIDER)
    if not os.getenv(api_key_var):
        missing.append(api_key_var)

    if missing:
        error_msg = f"Missing required environment variables: {', '.join(missing)}"
        logger.error(error_msg)
        raise EnvironmentError(error_msg)

    # Validate directories
    if not os.path.exists(SOURCE_DIR):
        logger.warning(f"Source directory does not exist, creating: {SOURCE_DIR}")
        os.makedirs(SOURCE_DIR, exist_ok=True)

    if not os.path.exists(DEST_DIR):
        logger.info(f"Destination directory does not exist, creating: {DEST_DIR}")
        os.makedirs(DEST_DIR, exist_ok=True)

    logger.info(f"Environment validated. LLM Provider: {LLM_PROVIDER}")
    return True
