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

# List all artists (coming soon)
python main.py list-artists

# Send beats to all artists (coming soon)
python main.py send-beats

# View sending history (coming soon)
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

## Push to GitHub

Your repo is already linked to `origin`. To push your latest work:

```bash
git add .
git status   # Confirm config.yaml, credentials.json, token.json are NOT listed
git commit -m "feat: complete Contact Automation - send beat packs, scheduling, docs"
git push origin main
```

If you're on another branch (e.g. `feature/database-service`), merge into `main` first or push that branch and open a Pull Request. Your local `config/config.yaml`, `config/credentials.json`, and `config/token.json` are gitignored and will not be pushed.

## Requirements

- Python 3.8+
- Google Cloud Project with APIs enabled
- OAuth 2.0 credentials
- Access to Google Drive "vault" folder
- Gmail account

## Documentation

- **[Next Steps](NEXT_STEPS.md)** ⭐ - **Start here when returning to the project!**
- [Contributing Guidelines](CONTRIBUTING.md) - Development workflow and standards
- [SDLC Practices](docs/SDLC.md) - Software Development Life Cycle
- [GitHub Best Practices](docs/GITHUB_BEST_PRACTICES.md) - Git workflow and PR process
- [System Design](SYSTEM_DESIGN.md) - Complete architecture and design
- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Step-by-step development plan
- [Google Cloud Setup Guide](docs/GOOGLE_CLOUD_SETUP.md) - Detailed OAuth setup
- [OAuth Troubleshooting](docs/OAUTH_FIX.md) - Fix common OAuth issues
- [Scheduling Beat Packs](docs/SCHEDULING.md) - Windows Task Scheduler setup
- [Changelog](CHANGELOG.md) - Version history

## Development Standards

This project follows industry best practices:

- ✅ **SDLC**: Complete software development life cycle
- ✅ **Git Flow**: Feature branches, code reviews, PR process
- ✅ **Conventional Commits**: Standardized commit messages
- ✅ **Code Quality**: Black, Flake8, MyPy, Pytest
- ✅ **CI/CD**: GitHub Actions for automated testing
- ✅ **Pre-commit Hooks**: Code quality checks before commit
- ✅ **Documentation**: Comprehensive docs and docstrings
- ✅ **Testing**: Unit, integration, and E2E tests

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow.

### Project Structure

```
ContactAutomation/
├── config/              # Configuration files
│   ├── config.example.yaml  # Copy to config.yaml (gitignored)
│   └── credentials.json     # OAuth tokens (gitignored)
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
