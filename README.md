# Contact Automation System

Automated email distribution system for sending personalized beat packs to artists via Gmail.

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

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable APIs:
   - Google Drive API
   - Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials JSON
6. Place in `config/credentials.json`

### 3. Configuration

1. Copy `.env.example` to `.env`
2. Fill in your Google Cloud credentials
3. Set your vault folder ID
4. Update `config/config.yaml` if needed

### 4. First Run

```bash
# Authenticate with Google
python main.py configure

# Test with dry run
python main.py send-beats --dry-run

# Send to all artists
python main.py send-beats
```

## Usage

```bash
# Send beats to all artists
python main.py send-beats

# View sending history
python main.py show-history

# List all artists
python main.py list-artists

# Configure credentials
python main.py configure
```

## Requirements

- Python 3.8+
- Google Cloud Project with APIs enabled
- OAuth 2.0 credentials
- Access to Google Drive "vault" folder
- Gmail account

## License

Private project - All rights reserved





