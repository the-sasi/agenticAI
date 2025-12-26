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

# Required environment variables
REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY"
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

    # Validate directories
    if not os.path.exists(SOURCE_DIR):
        logger.warning(f"Source directory does not exist, creating: {SOURCE_DIR}")
        os.makedirs(SOURCE_DIR, exist_ok=True)

    if not os.path.exists(DEST_DIR):
        logger.info(f"Destination directory does not exist, creating: {DEST_DIR}")
        os.makedirs(DEST_DIR, exist_ok=True)

    logger.info("All environment variables validated successfully")
    return True
