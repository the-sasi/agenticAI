import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Container configuration
CONTAINER_NAME = "doclingdev"

# File categories
CATEGORIES = {
    "Images": ["png", "jpg", "jpeg"],
    "Documents": ["pdf", "docx", "txt"],
    "Others": []
}

# Agent configuration
MAX_STEPS = 20

# Required environment variables
REQUIRED_ENV_VARS = [
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_DEPLOYMENT_NAME",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_STORAGE_CONNECTION_STRING"
]


def validate_env():
    """
    Validate that all required environment variables are set
    """
    missing = []
    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if not value:
            missing.append(var)

    if missing:
        error_msg = f"Missing required environment variables: {', '.join(missing)}"
        logger.error(error_msg)
        raise EnvironmentError(error_msg)

    logger.info("All environment variables validated successfully")
    return True
