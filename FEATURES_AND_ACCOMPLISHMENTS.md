# Contact Automation System — Features & Accomplishments

This document summarizes everything the project does and what we built.

---

## CLI Commands (What You Can Run)

| Command | What It Does |
|--------|----------------|
| `python main.py configure` | Opens browser for Google sign-in; saves token for Drive + Gmail. Run once (or when token expires). |
| `python main.py list-artists` | Fetches everyone with access to your vault folder from Google Drive, shows a table (Name, Email), and syncs them to the local database. |
| `python main.py send-beats` | Sends personalized beat packs to all artists: random 3–5 MP3s + Beat Agreement per email, with rate limiting and history logging. |
| `python main.py send-beats --dry-run` | Same flow but **no emails sent** — use to verify artists, beat selection, and counts. |
| `python main.py show-history` | Displays email history table: artist, email, timestamp, pack #, beats sent, status. Use `-n 100` to show more rows. |

---

## Features Delivered

### 1. Google Drive Integration
- **Vault folder**: Uses your configured folder ID to read who has access.
- **Artists**: Reads folder permissions and extracts **name** and **email** for each user (no service accounts).
- **Beats**: Lists all **MP3** files in the vault (by MIME type).
- **Download**: Can download any file by ID (used to attach beats to emails).
- **Verification**: Optional check that the folder is accessible.

### 2. Database (SQLite)
- **4 tables**: `artists`, `beats`, `email_history`, `artist_beat_history`.
- **Artists**: Name, email (unique), added date, **last pack number** (increments per artist).
- **Beats**: Filename (unique), beat name, BPM, key, style, file type, size, added date.
- **Email history**: Who was sent what, when, pack number, list of beat IDs, status (sent/failed).
- **Artist–beat history**: Which beat was sent to which artist and when (for 30-day duplicate rule).
- **Indexes** on email, filename, artist IDs, and dates for fast queries.
- **Docs**: Full schema and examples in `docs/DATABASE_SCHEMA.md`.

### 3. Beat Filename Parser
- **Pattern**: `@zobi - [Beat Name] - [BPM] - [Key] - [Style].mp3`
- **Extracts**: producer, beat_name, bpm, key, style_category, file_type.
- **Edge cases**: Invalid/malformed filenames return `None`; fallback beat name from filename without extension.
- **Batch**: Can parse many filenames at once.
- **Case**: Matching is case-insensitive.

### 4. Beat Selection
- **Count**: Randomly picks **3–5** beats per artist (configurable min/max).
- **30-day rule**: Skips beats that were already sent to that artist in the last 30 days.
- **Fallback**: If everything was sent recently, still picks from all beats so each artist gets something.
- **Config**: Min/max beats and duplicate-prevention window come from `config.yaml`.

### 5. Email Personalization
- **Template**: `templates/email_template.txt` with `{artist_name}` and `{beat_list}`.
- **Replacement**: Artist name and comma-separated beat names inserted into body.
- **Subject**: `Exclusive Beat pack #1`, `#2`, … per artist (from config template).

### 6. Gmail Sending
- **Send**: Composes a MIME message (plain text + attachments) and sends via Gmail API.
- **Attachments**: Beat Usage Agreement (from `templates/beat_usage_agreement.txt`) + selected MP3 files.
- **Rate limiting**: Delay between each email + optional pause every N emails (to stay in primary inbox).
- **Errors**: Failed sends are logged in DB with status `failed`; success is `sent`.

### 7. Full Send Workflow (send-beats)
1. Fetch **artists** from Drive (permissions on vault folder).
2. Fetch **MP3 list** from Drive; parse filenames and **upsert beats** into DB.
3. Load **Beat Agreement** from templates.
4. For each artist:
   - Get/create artist in DB; compute **next pack number**.
   - **Select** 3–5 random beats (respecting 30-day rule).
   - **Generate** subject and body (personalized).
   - **Download** selected beats from Drive; attach agreement + MP3s.
   - **Send** email (or skip in dry run); **log** to `email_history` and `artist_beat_history`; update artist’s **last_pack_number**.
5. Apply **rate limiting** between sends.
6. Print a **summary** table (artist, email, status, detail).

### 8. Authentication
- **OAuth 2.0** for Google (Drive + Gmail).
- **Scopes**: Drive read-only, Gmail send.
- **Token**: Stored in `config/token.json`; refresh when expired.
- **Configure**: Single command to (re)authenticate and verify APIs.

### 9. Configuration
- **config/config.yaml**: Vault folder ID, rate limits, min/max beats, duplicate-prevention days, template paths, DB path, logging.
- **Templates**: Email body and Beat Agreement path in config; easy to edit without code changes.

### 10. Logging
- **File**: `logs/app.log` (with rotation).
- **Console**: INFO-level messages for key steps.
- **Logger**: Used across services for debugging and audit.

### 11. Testing
- **33 unit tests** across 5 test files.
- **Database**: Init, CRUD, duplicate prevention, pack numbers, context manager.
- **Google Drive**: Permissions, list beats, verify folder (mocked).
- **Beat parser**: Valid/invalid filenames, BPM, batch, case-insensitivity.
- **Beat selection**: Count 3–5, exclusion of recently sent, insufficient beats.
- **Email template**: Placeholder replacement and beat list formatting.
- **Run**: `pytest tests/unit/ -v` (coverage ~59% overall; high on core services).

### 12. Project & Dev Practices
- **SDLC**: Planning, design, implementation, testing, docs (see `docs/SDLC.md`).
- **Git**: Feature branches, conventional commits, PR template.
- **CI**: GitHub Actions for lint and test (when enabled).
- **Pre-commit**: Black, isort, flake8, mypy (config in repo).
- **Docs**: README, NEXT_STEPS, SYSTEM_DESIGN, GOOGLE_CLOUD_SETUP, OAUTH_FIX, DATABASE_SCHEMA, TEST_ENGINEER_PREP, CONTRIBUTING, CHANGELOG.

---

## What We Accomplished (Summary)

- **End-to-end automation**: From “vault folder + Gmail” to “every artist gets a personalized beat pack and we track it.”
- **Duplicate prevention**: Same beat not sent to the same artist within 30 days.
- **Pack tracking**: Each artist has a growing pack number (Exclusive Beat pack #1, #2, …).
- **Beat Agreement**: Attached to every email automatically.
- **CLI**: Four commands (configure, list-artists, send-beats, show-history) with clear output and dry run.
- **Database**: Full schema, indexes, and documentation.
- **Tests**: 33 passing unit tests and a clear place to add integration tests later.
- **Production-style setup**: Config, logging, error handling, rate limiting, and docs.

---

## Quick Reference — Run These

```bash
python main.py configure          # One-time (or when token expires)
python main.py list-artists      # See all 38 artists (or your current count)
python main.py show-history      # See sent emails (empty until first send)
python main.py send-beats --dry-run   # Test without sending
python main.py send-beats        # Send for real
python -m pytest tests/unit/ -v  # Run all 33 tests
```

---

## File Overview

| Area | Files |
|------|--------|
| **CLI** | `main.py` |
| **Services** | `auth_service`, `database_service`, `google_drive_service`, `beat_parser_service`, `beat_selection_service`, `email_template_service`, `gmail_service` |
| **Config** | `config/config.yaml`, `templates/email_template.txt`, `templates/beat_usage_agreement.txt` |
| **Tests** | `tests/unit/test_database_service.py`, `test_google_drive_service.py`, `test_beat_parser_service.py`, `test_beat_selection_service.py`, `test_email_template_service.py` |
| **Docs** | `README.md`, `SYSTEM_DESIGN.md`, `NEXT_STEPS.md`, `docs/DATABASE_SCHEMA.md`, `docs/GOOGLE_CLOUD_SETUP.md`, `docs/OAUTH_FIX.md`, `docs/SDLC.md`, `docs/GITHUB_BEST_PRACTICES.md`, `docs/TEST_ENGINEER_PREP.md`, `CONTRIBUTING.md`, `CHANGELOG.md` |

You now have a single place to see **all features and accomplishments**: this file.
