"""
Google Drive service for accessing vault folder.
Handles authentication, listing artists, and fetching beat files.
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io
import yaml
from services.auth_service import get_credentials
from utils.logger import setup_logger

logger = setup_logger(__name__)


class GoogleDriveService:
    """Service for interacting with Google Drive API."""

    def __init__(self, vault_folder_id: Optional[str] = None):
        """
        Initialize Google Drive service.

        Args:
            vault_folder_id: Google Drive folder ID. If None, loads from config.
        """
        creds = get_credentials()
        if not creds:
            raise ValueError("Authentication required. Run 'python main.py configure' first.")

        self.drive_service = build('drive', 'v3', credentials=creds)

        if vault_folder_id is None:
            config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            vault_folder_id = config['drive']['vault_folder_id']

        self.vault_folder_id = vault_folder_id
        logger.info(f"Google Drive service initialized for folder: {vault_folder_id}")

    def get_folder_permissions(self) -> List[Dict[str, str]]:
        """
        Get list of users with access to the vault folder (artists).

        Returns:
            List of dictionaries with 'name' and 'email' keys

        Raises:
            HttpError: If API call fails
        """
        try:
            artists = []
            page_token = None

            while True:
                # Get permissions for the folder
                results = self.drive_service.permissions().list(
                    fileId=self.vault_folder_id,
                    fields='nextPageToken, permissions(id, emailAddress, displayName, type)',
                    pageToken=page_token
                ).execute()

                permissions = results.get('permissions', [])

                for perm in permissions:
                    # Only include user permissions (not service accounts or domain-wide)
                    if perm.get('type') == 'user' and perm.get('emailAddress'):
                        artists.append({
                            'name': perm.get('displayName', perm.get('emailAddress', 'Unknown')),
                            'email': perm.get('emailAddress')
                        })

                page_token = results.get('nextPageToken')
                if not page_token:
                    break

            logger.info(f"Found {len(artists)} artists with access to vault folder")
            return artists

        except HttpError as error:
            logger.error(f"Error fetching folder permissions: {error}")
            raise

    def list_beat_files(self) -> List[Dict[str, Any]]:
        """
        List all MP3 files in the vault folder.

        Returns:
            List of dictionaries with file metadata:
            - id: Google Drive file ID
            - name: Filename
            - size: File size in bytes
            - mimeType: MIME type
            - modifiedTime: Last modified timestamp

        Raises:
            HttpError: If API call fails
        """
        try:
            beats = []
            page_token = None

            # Query for MP3 files in the vault folder
            query = f"'{self.vault_folder_id}' in parents and mimeType='audio/mpeg' and trashed=false"

            while True:
                results = self.drive_service.files().list(
                    q=query,
                    fields='nextPageToken, files(id, name, size, mimeType, modifiedTime)',
                    pageToken=page_token,
                    orderBy='name'
                ).execute()

                files = results.get('files', [])
                beats.extend(files)

                page_token = results.get('nextPageToken')
                if not page_token:
                    break

            logger.info(f"Found {len(beats)} MP3 files in vault folder")
            return beats

        except HttpError as error:
            logger.error(f"Error listing beat files: {error}")
            raise

    def download_file(self, file_id: str) -> bytes:
        """
        Download a file from Google Drive.

        Args:
            file_id: Google Drive file ID

        Returns:
            File contents as bytes

        Raises:
            HttpError: If API call fails
        """
        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug(f"Download progress: {int(status.progress() * 100)}%")

            file_content.seek(0)
            content = file_content.read()
            logger.info(f"Downloaded file {file_id} ({len(content)} bytes)")
            return content

        except HttpError as error:
            logger.error(f"Error downloading file {file_id}: {error}")
            raise

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific file.

        Args:
            file_id: Google Drive file ID

        Returns:
            Dictionary with file metadata

        Raises:
            HttpError: If API call fails
        """
        try:
            file_metadata = self.drive_service.files().get(
                fileId=file_id,
                fields='id, name, size, mimeType, modifiedTime, createdTime'
            ).execute()

            return file_metadata

        except HttpError as error:
            logger.error(f"Error getting file metadata for {file_id}: {error}")
            raise

    def verify_folder_access(self) -> bool:
        """
        Verify that we have access to the vault folder.

        Returns:
            True if accessible, False otherwise
        """
        try:
            folder_metadata = self.drive_service.files().get(
                fileId=self.vault_folder_id,
                fields='id, name'
            ).execute()

            logger.info(f"Verified access to folder: {folder_metadata.get('name')}")
            return True

        except HttpError as error:
            logger.error(f"Cannot access vault folder: {error}")
            return False
