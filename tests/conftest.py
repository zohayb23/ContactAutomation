"""
Pytest configuration and shared fixtures
"""
import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def test_data_dir():
    """Return path to test data directory"""
    return Path(__file__).parent / "data"


@pytest.fixture
def mock_config():
    """Mock configuration"""
    return {
        "drive": {
            "vault_folder_id": "test_folder_id",
            "scopes": ["https://www.googleapis.com/auth/drive.readonly"]
        },
        "gmail": {
            "scopes": ["https://www.googleapis.com/auth/gmail.send"],
            "rate_limit_delay": 1
        },
        "database": {
            "path": ":memory:"  # Use in-memory database for tests
        }
    }
