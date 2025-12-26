import os
import logging
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
from dotenv import load_dotenv
from config.settings import CONTAINER_NAME

load_dotenv()

logger = logging.getLogger(__name__)

blob_service = BlobServiceClient.from_connection_string(
    os.getenv("AZURE_STORAGE_CONNECTION_STRING")
)

def list_files():
    """
    List ONLY root-level files (ignore already categorized files)
    """
    try:
        logger.info(f"Listing root-level files from container: {CONTAINER_NAME}")
        container = blob_service.get_container_client(CONTAINER_NAME)

        files = []
        for blob in container.list_blobs():
            if "/" not in blob.name:   # root-level only
                files.append(blob.name)

        logger.info(f"Found {len(files)} uncategorized files")
        return files
    except AzureError as e:
        logger.error(f"Azure error listing files: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return []


def move_file(filename: str, category: str):
    """
    Move file to a virtual folder inside SAME container
    """
    try:
        logger.info(f"Moving file: {filename} to category: {category}")
        container = blob_service.get_container_client(CONTAINER_NAME)

        source_blob = container.get_blob_client(filename)
        destination_blob_name = f"{category}/{filename}"
        destination_blob = container.get_blob_client(destination_blob_name)

        # Copy
        logger.debug(f"Copying {filename} to {destination_blob_name}")
        destination_blob.start_copy_from_url(source_blob.url)

        # Delete original
        logger.debug(f"Deleting original file: {filename}")
        source_blob.delete_blob()

        logger.info(f"Successfully moved {filename} → {destination_blob_name}")
    except AzureError as e:
        logger.error(f"Azure error moving file {filename}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error moving file {filename}: {str(e)}")
        raise
