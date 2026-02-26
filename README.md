# Contact Automation System

Automated email distribution system for sending personalized beat packs to artists via Gmail.

## 🎯 Project Status

**Current Phase**: Complete
**Completion**: 100%

### ✅ Completed
- Project structure and configuration
- Google Cloud OAuth authentication
- Database service (SQLite, 4 tables, full CRUD)
- Google Drive service (artists, beats, download)
- Beat parser (filename metadata extraction)
- Beat selection service (random + 30-day duplicate prevention)
- Email template service (personalization)
- Gmail service (send with attachments, rate limiting)
- Full CLI: `configure`, `list-artists`, `send-beats`, `show-history`
- 33 unit tests passing

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
│   ├── config.example.yaml  # Copy to config.yaml (gitignored)
│   └── credentials.json     # OAuth tokens (gitignored)
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
7. Copy `config/config.example.yaml` to `config/config.yaml`
8. Get your vault folder ID from Google Drive URL and set it in `config/config.yaml`

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

### 4. First Run

```bash
# List artists in your vault folder
python main.py list-artists

# Send beats (dry run first - no emails sent)
python main.py send-beats --dry-run

# Send beats to all artists
python main.py send-beats

# View sending history
python main.py show-history
```

### 5. Scheduling (optional)

To send packs automatically (e.g. monthly), use **Windows Task Scheduler** with the provided script:

- **Script:** `scripts/send_beats_scheduled.bat`
- **Full guide:** [docs/SCHEDULING.md](docs/SCHEDULING.md)

Example: run the task on the first Friday of every month at 10:00 AM.

## Usage

### Available Commands

```bash
# Configure Google API authentication
python main.py configure

# List all artists
python main.py list-artists

# Send beats to all artists
python main.py send-beats

# View sending history
python main.py show-history
```

### Current Status

- ✅ `configure` - Set up OAuth authentication
- ✅ `list-artists` - List artists from vault folder (syncs to DB)
- ✅ `send-beats` - Send personalized beat packs to all artists (`--dry-run` to test)
- ✅ `show-history` - Display email sending history table
- ✅ `check-beats` - List beats in vault and flag any that need filename formatting

### What else you can do

- **Schedule sends** – Use [Windows Task Scheduler](docs/SCHEDULING.md) to run packs on the 14th and 28th (or your preferred dates).
- **Check vault health** – Run `python main.py check-beats` after adding or renaming beats.
- **Share the project** – Push to GitHub (see below); use the LinkedIn/Discord copy in [docs/SEND_FREQUENCY_AND_MARKETING.md](docs/SEND_FREQUENCY_AND_MARKETING.md) to promote it.
- **Extend the app** – Add new CLI commands, support more email templates, or integrate with other tools (e.g. analytics, CRM).

## Requirements

- Python 3.8+
- Google Cloud Project with APIs enabled
- OAuth 2.0 credentials
- Access to Google Drive "vault" folder
- Gmail account

## Documentation

| Doc | Description |
|-----|-------------|
| [Google Cloud Setup](docs/GOOGLE_CLOUD_SETUP.md) | OAuth and API setup |
| [OAuth Troubleshooting](docs/OAUTH_FIX.md) | Fix common auth issues |
| [Scheduling](docs/SCHEDULING.md) | Windows Task Scheduler |
| [Send frequency & marketing](docs/SEND_FREQUENCY_AND_MARKETING.md) | Cadence and Discord/LinkedIn copy |
| [System Design](SYSTEM_DESIGN.md) | Architecture |
| [Changelog](CHANGELOG.md) | Version history |

## Development

- **Tests:** `pytest`
- **Code quality:** Black, Flake8, MyPy (see [CONTRIBUTING.md](CONTRIBUTING.md))

```
ContactAutomation/
├── config/           # config.example.yaml → config.yaml (add vault ID)
├── services/         # Core logic (auth, drive, gmail, beats, email, db)
├── templates/        # Email body + beat usage agreement
├── scripts/          # send_beats_scheduled.bat, send_beats_test.bat
├── docs/             # Setup and scheduling guides
├── main.py           # CLI entry point
└── requirements.txt
```

### Tech stack

- **Python 3.8+**
- **Google Drive API** - Access vault folder
- **Gmail API** - Send emails
- **SQLite** - History tracking
- **OAuth 2.0** - Authentication

## License

Private project - All rights reserved
