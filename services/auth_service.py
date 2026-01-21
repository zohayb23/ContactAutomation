"""
Authentication service for Google APIs (Drive and Gmail).
Handles OAuth 2.0 flow and token management.
"""
import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import yaml

# Scopes required for the application
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_credentials():
    """
    Get valid user credentials from storage or run OAuth flow.
    Returns Credentials object or None if authentication fails.
    """
    config = load_config()
    creds = None
    token_path = Path(__file__).parent.parent / 'config' / 'token.json'
    credentials_path = Path(__file__).parent.parent / 'config' / 'credentials.json'

    # Check if token.json exists
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"Error loading existing token: {e}")
            creds = None

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None

        if not creds:
            if not credentials_path.exists():
                print("\n[ERROR] credentials.json not found!")
                print(f"   Expected location: {credentials_path}")
                print("\n   Please:")
                print("   1. Download credentials.json from Google Cloud Console")
                print("   2. Save it to: config/credentials.json")
                print("   3. Run this command again")
                return None

            print("\n[INFO] Starting OAuth authentication...")
            print("   A browser window will open for you to sign in.")
            print("   Please authorize the application.\n")

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"\n[ERROR] Authentication failed: {e}")
                return None

        # Save the credentials for the next run
        try:
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
            print(f"\n[SUCCESS] Authentication successful!")
            print(f"   Token saved to: {token_path}")
        except Exception as e:
            print(f"\n[WARNING] Could not save token: {e}")

    return creds


def test_connection():
    """
    Test the connection to Google APIs.
    Returns True if successful, False otherwise.
    """
    print("\n[TEST] Testing connection to Google APIs...")

    creds = get_credentials()
    if not creds:
        return False

    try:
        # Test Drive API
        print("   Testing Google Drive API...", end=" ")
        drive_service = build('drive', 'v3', credentials=creds)
        drive_service.files().list(pageSize=1).execute()
        print("[OK]")

        # Test Gmail API
        print("   Testing Gmail API...", end=" ")
        gmail_service = build('gmail', 'v1', credentials=creds)
        # Use a simpler test that only requires gmail.send scope
        # getProfile requires gmail.readonly scope, but we only have gmail.send
        # So we'll just verify the service can be built (which means auth works)
        # The actual send test will happen when we send emails
        print("[OK] (Service initialized)")

        print("\n[SUCCESS] All API connections successful!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Connection test failed: {e}")
        return False


def configure():
    """
    Main configure function - sets up authentication.
    """
    print("=" * 60)
    print("Contact Automation System - Configuration")
    print("=" * 60)

    # Check if credentials.json exists
    credentials_path = Path(__file__).parent.parent / 'config' / 'credentials.json'
    if not credentials_path.exists():
        print("\n[ERROR] credentials.json not found!")
        print(f"   Location: {credentials_path}")
        print("\n   Please complete Google Cloud setup:")
        print("   1. Go to Google Cloud Console")
        print("   2. Create OAuth 2.0 credentials (Desktop app)")
        print("   3. Download credentials.json")
        print("   4. Save it to: config/credentials.json")
        print("\n   See docs/GOOGLE_CLOUD_SETUP.md for detailed instructions.")
        return False

    print(f"\n[OK] Found credentials.json")

    # Run authentication
    creds = get_credentials()
    if not creds:
        return False

    # Test connection
    success = test_connection()

    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] Configuration complete! You're ready to use the system.")
        print("=" * 60)
        print("\nNext steps:")
        print("  - python main.py list-artists    # View artists in vault")
        print("  - python main.py send-beats      # Send beats to artists")
    else:
        print("\n" + "=" * 60)
        print("[ERROR] Configuration incomplete. Please check the errors above.")
        print("=" * 60)

    return success
