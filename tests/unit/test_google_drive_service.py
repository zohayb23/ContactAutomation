"""
Unit tests for Google Drive service.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from services.google_drive_service import GoogleDriveService


@pytest.fixture
def mock_credentials():
    """Mock Google credentials."""
    creds = Mock()
    creds.valid = True
    return creds


@pytest.fixture
def mock_drive_service():
    """Mock Google Drive service."""
    service = Mock()

    # Mock permissions list
    permissions_mock = Mock()
    permissions_mock.list.return_value.execute.return_value = {
        'permissions': [
            {
                'id': 'perm1',
                'emailAddress': 'artist1@example.com',
                'displayName': 'Artist One',
                'type': 'user'
            },
            {
                'id': 'perm2',
                'emailAddress': 'artist2@example.com',
                'displayName': 'Artist Two',
                'type': 'user'
            }
        ]
    }
    service.permissions.return_value = permissions_mock

    # Mock files list
    files_mock = Mock()
    files_mock.list.return_value.execute.return_value = {
        'files': [
            {
                'id': 'file1',
                'name': 'beat1.mp3',
                'size': '3000000',
                'mimeType': 'audio/mpeg',
                'modifiedTime': '2025-01-01T00:00:00Z'
            },
            {
                'id': 'file2',
                'name': 'beat2.mp3',
                'size': '2500000',
                'mimeType': 'audio/mpeg',
                'modifiedTime': '2025-01-02T00:00:00Z'
            }
        ]
    }
    service.files.return_value = files_mock

    return service


@patch('services.google_drive_service.get_credentials')
@patch('services.google_drive_service.build')
def test_get_folder_permissions(mock_build, mock_get_creds, mock_credentials, mock_drive_service):
    """Test getting folder permissions (artists)."""
    mock_get_creds.return_value = mock_credentials
    mock_build.return_value = mock_drive_service

    service = GoogleDriveService(vault_folder_id='test_folder_id')
    artists = service.get_folder_permissions()

    assert len(artists) == 2
    assert artists[0]['email'] == 'artist1@example.com'
    assert artists[0]['name'] == 'Artist One'
    assert artists[1]['email'] == 'artist2@example.com'
    assert artists[1]['name'] == 'Artist Two'


@patch('services.google_drive_service.get_credentials')
@patch('services.google_drive_service.build')
def test_list_beat_files(mock_build, mock_get_creds, mock_credentials, mock_drive_service):
    """Test listing beat files."""
    mock_get_creds.return_value = mock_credentials
    mock_build.return_value = mock_drive_service

    service = GoogleDriveService(vault_folder_id='test_folder_id')
    beats = service.list_beat_files()

    assert len(beats) == 2
    assert beats[0]['name'] == 'beat1.mp3'
    assert beats[0]['id'] == 'file1'
    assert beats[1]['name'] == 'beat2.mp3'


@patch('services.google_drive_service.get_credentials')
@patch('services.google_drive_service.build')
def test_verify_folder_access(mock_build, mock_get_creds, mock_credentials, mock_drive_service):
    """Test verifying folder access."""
    mock_get_creds.return_value = mock_credentials
    mock_build.return_value = mock_drive_service

    # Mock folder get
    folder_mock = Mock()
    folder_mock.get.return_value.execute.return_value = {
        'id': 'test_folder_id',
        'name': 'vault'
    }
    mock_drive_service.files.return_value = folder_mock

    service = GoogleDriveService(vault_folder_id='test_folder_id')
    result = service.verify_folder_access()

    assert result is True
