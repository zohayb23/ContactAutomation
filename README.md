# Contact Automation

Automated email distribution: sends personalized beat packs to artists via Gmail from a Google Drive vault. Each pack includes 3–5 random beats and a usage agreement. Duplicate prevention (30-day) and per-artist pack numbering are built in.

## Features

- Sync artist list from a shared Drive folder; parse and store beat metadata from filenames.
- Select 3–5 random beats per artist (no repeat within 30 days); send via Gmail with attachments.
- CLI: `configure`, `list-artists`, `send-beats`, `show-history`, `check-beats`.
- Optional scheduling via Windows Task Scheduler.

## Requirements

- Python 3.8+
- Google Cloud project with Drive API and Gmail API enabled; OAuth 2.0 desktop credentials.
- A Drive folder (vault) containing artist permissions and beat MP3s.

## Setup

1. **Install:** `python -m venv venv` then `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux). Run `pip install -r requirements.txt`.
2. **Google Cloud:** Create a project, enable Drive + Gmail APIs, configure OAuth consent, create OAuth desktop credentials. Save as `config/credentials.json`. See [docs/GOOGLE_CLOUD_SETUP.md](docs/GOOGLE_CLOUD_SETUP.md).
3. **Config:** Copy `config/config.example.yaml` to `config/config.yaml` and set your vault folder ID (from the Drive folder URL).
4. **Auth:** Run `python main.py configure` and complete the browser sign-in. Token is stored in `config/token.json`.

## Usage

| Command | Description |
|--------|-------------|
| `python main.py configure` | Authenticate with Google (Drive + Gmail). |
| `python main.py list-artists` | Sync and list artists from the vault folder. |
| `python main.py send-beats` | Send beat packs to all artists. Use `--dry-run` to preview. |
| `python main.py show-history` | Show email send history. |
| `python main.py check-beats` | List beats and flag filenames that need formatting. |

Beat filename format: `@zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3`.

**Scheduling:** Use `scripts/send_beats_scheduled.bat` with Windows Task Scheduler. See [docs/SCHEDULING.md](docs/SCHEDULING.md).

## Project structure

```
├── config/         config.example.yaml → config.yaml (vault ID); credentials + token (gitignored)
├── services/       Auth, Drive, Gmail, beat parser/selection, email template, database
├── templates/      Email body and beat usage agreement
├── scripts/        send_beats_scheduled.bat, send_beats_test.bat
├── docs/           Setup, OAuth, scheduling, marketing copy
├── main.py         CLI entry point
└── requirements.txt
```

## Documentation

| Doc | Description |
|-----|-------------|
| [GOOGLE_CLOUD_SETUP.md](docs/GOOGLE_CLOUD_SETUP.md) | OAuth and API setup |
| [OAUTH_FIX.md](docs/OAUTH_FIX.md) | Auth troubleshooting |
| [SCHEDULING.md](docs/SCHEDULING.md) | Task Scheduler setup |
| [SEND_FREQUENCY_AND_MARKETING.md](docs/SEND_FREQUENCY_AND_MARKETING.md) | Send cadence, Discord/LinkedIn copy |
| [SYSTEM_DESIGN.md](SYSTEM_DESIGN.md) | Architecture |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

## Development

Run tests: `pytest`. Code style: Black, Flake8, MyPy. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

License: Private. All rights reserved.
