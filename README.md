# Contact Automation System

Automated email distribution system for sending personalized beat packs to artists via Gmail.

## 🎯 Project Status

**Current Phase**: Core Services Development  
**Completion**: ~30% (Setup & Authentication Complete)

### ✅ Completed
- Project structure and configuration
- Google Cloud OAuth authentication
- CLI framework with `configure` command
- Documentation and setup guides

### 🚧 In Progress
- Database service (SQLite schema)
- Google Drive service (fetch artists & beats)
- Beat parser and selection logic
- Email sending functionality

## Features

- 🎵 Extract artist list from Google Drive shared folder
- 🎲 Randomly select 3-5 beats per artist
- 📧 Send personalized emails via Gmail with attachments
- 📊 Track sending history with SQLite database
- 🔄 Duplicate prevention (30-day rule)
- 📦 Incremental pack numbers per artist

## Project Structure

```
ContactAutomation/
├── config/              # Configuration files
│   ├── config.yaml     # Application settings
│   └── credentials.json # OAuth tokens (gitignored)
├── services/           # Core service modules
├── templates/          # Email and agreement templates
├── database/           # SQLite database files
├── logs/              # Application logs
├── utils/             # Utility functions
├── main.py            # CLI entry point
└── requirements.txt   # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Cloud Setup

**Detailed guide**: See [docs/GOOGLE_CLOUD_SETUP.md](docs/GOOGLE_CLOUD_SETUP.md)

Quick steps:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable APIs:
   - Google Drive API
   - Gmail API
4. Configure OAuth consent screen (add yourself as test user)
5. Create OAuth 2.0 credentials (Desktop app)
6. Download credentials JSON → save as `config/credentials.json`
7. Get your vault folder ID from Google Drive URL
8. Update `config/config.yaml` with vault folder ID

### 3. Authentication

```bash
# Authenticate with Google (opens browser)
python main.py configure
```

This will:
- Open browser for Google sign-in
- Request Drive and Gmail permissions
- Save token to `config/token.json`

**Note**: Make sure you've added yourself as a test user in OAuth consent screen!

### 4. First Run (Coming Soon)

```bash
# List artists in vault (when implemented)
python main.py list-artists

# Send beats to all artists (when implemented)
python main.py send-beats
```

## Usage

### Available Commands

```bash
# Configure Google API authentication
python main.py configure

# List all artists (coming soon)
python main.py list-artists

# Send beats to all artists (coming soon)
python main.py send-beats

# View sending history (coming soon)
python main.py show-history
```

### Current Status

- ✅ `configure` - **Working** - Set up OAuth authentication
- 🚧 `list-artists` - **In Development** - List artists from vault folder
- 🚧 `send-beats` - **In Development** - Send beats to artists
- 🚧 `show-history` - **In Development** - Display email history

## Requirements

- Python 3.8+
- Google Cloud Project with APIs enabled
- OAuth 2.0 credentials
- Access to Google Drive "vault" folder
- Gmail account

## Documentation

- [System Design](SYSTEM_DESIGN.md) - Complete architecture and design
- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Step-by-step development plan
- [Google Cloud Setup Guide](docs/GOOGLE_CLOUD_SETUP.md) - Detailed OAuth setup
- [OAuth Troubleshooting](docs/OAUTH_FIX.md) - Fix common OAuth issues

## Development

### Project Structure

```
ContactAutomation/
├── config/              # Configuration files
│   ├── config.yaml     # Application settings
│   └── credentials.json # OAuth tokens (gitignored)
├── services/           # Core service modules
│   ├── auth_service.py # OAuth authentication ✅
│   ├── database_service.py # SQLite operations 🚧
│   ├── google_drive_service.py # Drive API 🚧
│   └── ...             # Other services
├── templates/          # Email templates
├── database/           # SQLite database files
├── logs/              # Application logs
├── docs/              # Documentation
└── main.py            # CLI entry point
```

### Tech Stack

- **Python 3.8+**
- **Google Drive API** - Access vault folder
- **Gmail API** - Send emails
- **SQLite** - History tracking
- **OAuth 2.0** - Authentication

## License

Private project - All rights reserved
