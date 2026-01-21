# Implementation Plan - Contact Automation System

## High-Level Overview

Build a Python CLI tool that automates sending personalized beat packs to artists via Gmail, with full history tracking and duplicate prevention.

---

## Phase 1: Setup & Foundation (Week 1)

### Step 1: Project Setup
- [ ] Create project directory structure
- [ ] Initialize Python virtual environment
- [ ] Create `requirements.txt` with dependencies:
  - `google-api-python-client` (Drive & Gmail APIs)
  - `google-auth-httplib2`
  - `google-auth-oauthlib`
  - `sqlite3` (built-in)
  - `python-dotenv` (for config)
- [ ] Create `.gitignore` file
- [ ] Set up logging configuration

### Step 2: Google Cloud Setup
- [ ] Create Google Cloud Project
- [ ] Enable Google Drive API
- [ ] Enable Gmail API
- [ ] Create OAuth 2.0 credentials (Desktop app)
- [ ] Download credentials JSON file
- [ ] Set up OAuth consent screen
- [ ] Test authentication flow

### Step 3: Configuration System
- [ ] Create `config/` directory
- [ ] Create `config.yaml` for settings:
  - Vault folder ID
  - Email template path
  - Beat agreement path
  - Rate limiting settings
- [ ] Create `.env` file for sensitive data
- [ ] Create credential storage system

---

## Phase 2: Core Services (Week 1-2)

### Step 4: Database Service
- [ ] Create `services/database_service.py`
- [ ] Set up SQLite database schema:
  - `artists` table (id, name, email, added_date, last_pack_number)
  - `beats` table (id, filename, beat_name, bpm, key, style_category, etc.)
  - `email_history` table (id, artist_id, timestamp, pack_number, beats_sent, status)
  - `artist_beat_history` table (for duplicate prevention)
- [ ] Implement database initialization
- [ ] Create CRUD operations for all tables

### Step 5: Google Drive Service
- [ ] Create `services/google_drive_service.py`
- [ ] Implement OAuth authentication
- [ ] Function: `get_folder_permissions()` - Extract artist list (names & emails)
- [ ] Function: `list_beat_files()` - Get all MP3 files from vault folder
- [ ] Function: `download_file()` - Download beat files for attachments
- [ ] Test with your vault folder

### Step 6: Beat Parser Service
- [ ] Create `services/beat_parser_service.py`
- [ ] Implement filename parsing:
  - Pattern: `@zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3`
  - Extract: beat_name, bpm, key, style_category
- [ ] Store parsed metadata in database
- [ ] Handle edge cases (malformed filenames)

### Step 7: Beat Selection Service
- [ ] Create `services/beat_selection_service.py`
- [ ] Implement random selection algorithm:
  - Query database for artist's last send date
  - Exclude beats sent in last 30 days (duplicate prevention)
  - Random shuffle remaining beats
  - Select 3-5 unique beats
- [ ] Track selections to avoid duplicates in same batch

---

## Phase 3: Email Functionality (Week 2)

### Step 8: Email Template Service
- [ ] Create `services/email_template_service.py`
- [ ] Load email template from `templates/email_template.txt`
- [ ] Implement placeholder replacement:
  - `{artist_name}` → Artist's name
  - `{beat_list}` → Formatted list of beat names
- [ ] Format beat list (simple: "beat1, beat2, beat3")

### Step 9: Gmail Service
- [ ] Create `services/gmail_service.py`
- [ ] Implement OAuth authentication
- [ ] Function: `create_message()` - Compose email with:
  - Subject: "Exclusive Beat pack #{pack_number}"
  - Body: Personalized template
  - Attachments: 3-5 MP3 files + Beat Agreement PDF
- [ ] Function: `send_email()` - Send via Gmail API
- [ ] Implement rate limiting (1-2 second delays)
- [ ] Error handling (invalid emails, quota exceeded)

### Step 10: Beat Agreement Handler
- [ ] Create function to convert `templates/beat_usage_agreement.txt` to PDF
- [ ] Or attach as text file (simpler)
- [ ] Ensure it's attached to every email

---

## Phase 4: CLI Interface (Week 2-3)

### Step 11: Main CLI Application
- [ ] Create `main.py` as entry point
- [ ] Implement command structure:
  - `python main.py send-beats` - Main command
  - `python main.py show-history` - Display history
  - `python main.py list-artists` - Show all artists
  - `python main.py configure` - Setup credentials
- [ ] Use `argparse` or `click` library

### Step 12: Send Beats Command
- [ ] Orchestrate the full workflow:
  1. Initialize services (Drive, Gmail, Database)
  2. Fetch artist list from Google Drive
  3. Fetch beat files and parse metadata
  4. Load beat agreement
  5. For each artist:
     - Get pack number (increment from last)
     - Select random beats (3-5)
     - Generate email
     - Send email with attachments
     - Log to database
     - Apply rate limiting
  6. Display summary table
- [ ] Progress indicators
- [ ] Error handling and recovery

### Step 13: History Commands
- [ ] `show-history` - Display table:
  - Artist name, email, timestamp, pack number, beats sent, status
- [ ] `list-artists` - Show all artists with stats
- [ ] Format output nicely (use `tabulate` or similar)

---

## Phase 5: Testing & Polish (Week 3)

### Step 14: Error Handling
- [ ] Invalid email addresses
- [ ] API quota exceeded
- [ ] Network failures (retry logic)
- [ ] Missing beats (< 3 beats available)
- [ ] Malformed filenames
- [ ] Authentication failures

### Step 15: Logging & Monitoring
- [ ] Comprehensive logging to `logs/app.log`
- [ ] Log levels (INFO, WARNING, ERROR)
- [ ] Track all operations
- [ ] Log email send status

### Step 16: Configuration Management
- [ ] Make all settings configurable:
  - Rate limiting delays
  - Duplicate prevention days (30)
  - Number of beats per email (3-5)
  - Vault folder ID
- [ ] Environment variable support

### Step 17: Testing
- [ ] Test with 1-2 artists first (dry run mode)
- [ ] Test email sending (to your own email)
- [ ] Test duplicate prevention
- [ ] Test pack number incrementing
- [ ] Test error scenarios
- [ ] Full test with all artists

---

## Phase 6: Documentation & Deployment (Week 3)

### Step 18: Documentation
- [ ] Create `README.md` with:
  - Setup instructions
  - Google Cloud setup guide
  - Usage examples
  - Troubleshooting
- [ ] Document all configuration options
- [ ] Add code comments

### Step 19: Final Polish
- [ ] Code cleanup and refactoring
- [ ] Add type hints
- [ ] Optimize database queries
- [ ] Performance testing

### Step 20: Deployment
- [ ] Final testing
- [ ] Create backup of database
- [ ] Ready for production use!

---

## Quick Start Checklist (First Run)

1. ✅ Set up Google Cloud Project & APIs
2. ✅ Download OAuth credentials
3. ✅ Configure `config.yaml` with vault folder ID
4. ✅ Run `python main.py configure` to authenticate
5. ✅ Test with 1 artist: `python main.py send-beats --dry-run`
6. ✅ Send to test email first
7. ✅ Full run with all artists

---

## Estimated Timeline

- **Week 1**: Setup, Database, Google Drive integration
- **Week 2**: Beat parsing, selection, Gmail integration
- **Week 3**: CLI, testing, polish, documentation

**Total: ~3 weeks** (depending on availability and complexity)

---

## Key Dependencies

```python
google-api-python-client==2.100.0
google-auth-httplib2==0.1.1
google-auth-oauthlib==1.1.0
python-dotenv==1.0.0
pyyaml==6.0.1
tabulate==0.9.0  # For nice table formatting
```

---

## Success Criteria

✅ Can extract artist list from Google Drive vault folder
✅ Can parse beat filenames and extract metadata
✅ Can randomly select 3-5 beats per artist
✅ Can send personalized emails with attachments via Gmail
✅ Can track history in database
✅ Can prevent duplicates (30-day rule)
✅ Can increment pack numbers per artist
✅ CLI is user-friendly and provides good feedback

---

## Next Immediate Steps

1. **Start with Step 1**: Create project structure
2. **Then Step 2**: Set up Google Cloud Project (this might take some time)
3. **Then Step 4**: Build database service (foundation for everything)

Ready to begin? Let's start with Step 1!





