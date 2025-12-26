import os
import shutil
import logging
from config.settings import SOURCE_DIR, DEST_DIR

logger = logging.getLogger(__name__)


def list_files():
    """
    List files from the source directory (ignore subdirectories)
    """
    try:
        logger.info(f"Listing files from: {SOURCE_DIR}")

        if not os.path.exists(SOURCE_DIR):
            logger.error(f"Source directory does not exist: {SOURCE_DIR}")
            return []

        files = []
        for item in os.listdir(SOURCE_DIR):
            item_path = os.path.join(SOURCE_DIR, item)
            if os.path.isfile(item_path):
                files.append(item)

        logger.info(f"Found {len(files)} files to process")
        return files
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return []


def move_file(filename: str, category: str):
    """
    Move file to a category folder inside the destination directory
    """
    try:
        source_path = os.path.join(SOURCE_DIR, filename)
        category_dir = os.path.join(DEST_DIR, category)
        dest_path = os.path.join(category_dir, filename)

        logger.info(f"Moving file: {filename} to category: {category}")

        # Create category directory if it doesn't exist
        os.makedirs(category_dir, exist_ok=True)

        # Move the file
        shutil.move(source_path, dest_path)

        logger.info(f"Successfully moved {filename} -> {dest_path}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {filename}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error moving file {filename}: {str(e)}")
        raise
