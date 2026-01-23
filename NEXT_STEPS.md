# Next Steps - Contact Automation System

**Last Updated**: After initial setup and OAuth authentication completion
**Current Status**: ~30% Complete - Ready to build core services

---

## 🎯 Where We Are

### ✅ Completed
- [x] Project structure and configuration
- [x] Google Cloud OAuth authentication (`python main.py configure` works!)
- [x] CLI framework with command structure
- [x] All dependencies installed
- [x] Documentation and setup guides
- [x] Code pushed to GitHub

### 🚧 Next Phase: Core Services Development

---

## 📋 Immediate Next Steps (In Order)

### Step 1: Database Service (Priority 1)

**File**: `services/database_service.py`

**What to build**:
1. SQLite database initialization
2. Create 4 tables:
   - `artists` (id, name, email, added_date, last_pack_number)
   - `beats` (id, filename, beat_name, bpm, key, style_category, file_type, file_size, added_date)
   - `email_history` (id, artist_id, timestamp, pack_number, beats_sent, status, error_message)
   - `artist_beat_history` (id, artist_id, beat_id, sent_date) - for duplicate prevention
3. CRUD operations for all tables
4. Database connection management

**Reference**: See `SYSTEM_DESIGN.md` section 5.5 for schema details

**Test**: Create a simple test script to verify tables are created correctly

---

### Step 2: Google Drive Service (Priority 2)

**File**: `services/google_drive_service.py`

**What to build**:
1. Function: `get_folder_permissions()` - Extract artist list (names & emails)
   - Use `drive.permissions().list()` API
   - Filter for user emails (not service accounts)
   - Return list of {name, email} dictionaries
2. Function: `list_beat_files()` - Get all MP3 files from vault folder
   - Use `drive.files().list()` with query: `mimeType='audio/mpeg'` and `parents in 'FOLDER_ID'`
   - Return list of file metadata
3. Function: `download_file(file_id)` - Download beat files for attachments
   - Use `drive.files().get_media()` API
   - Save to temp directory or return bytes

**Reference**:
- Vault folder ID: `1D6pBAI4IDpicvLzLo9_R0qknn4y8DjCb` (in config.yaml)
- Use `services/auth_service.py` as reference for authentication

**Test**: Create `list-artists` command to test fetching artists

---

### Step 3: Beat Parser Service (Priority 3)

**File**: `services/beat_parser_service.py`

**What to build**:
1. Function: `parse_filename(filename)` - Extract metadata
   - Pattern: `@zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3`
   - Example: `@zobi - tundra - 136 - Cmin - travis.mp3`
   - Return: `{beat_name, bpm, key, style_category}`
2. Handle edge cases (malformed filenames)
3. Store parsed data in database (beats table)

**Test**: Parse a few sample filenames to verify extraction

---

### Step 4: Beat Selection Service (Priority 4)

**File**: `services/beat_selection_service.py`

**What to build**:
1. Function: `select_beats_for_artist(artist_id, count=3-5)` - Random selection
   - Query database for artist's last send date
   - If < 30 days, exclude previously sent beats (from `artist_beat_history`)
   - Random shuffle remaining beats
   - Select 3-5 unique beats
   - Return list of beat IDs
2. Track selections to avoid duplicates in same batch

**Test**: Test with a sample artist to verify selection logic

---

### Step 5: Email Template Service (Priority 5)

**File**: `services/email_template_service.py`

**What to build**:
1. Function: `load_template()` - Load from `templates/email_template.txt`
2. Function: `generate_email(artist_name, beat_list)` - Replace placeholders
   - Replace `{artist_name}` with actual name
   - Replace `{beat_list}` with formatted beat names (e.g., "tundra, hope, splash")
3. Return formatted email body

**Test**: Generate a sample email to verify formatting

---

### Step 6: Gmail Service (Priority 6)

**File**: `services/gmail_service.py`

**What to build**:
1. Function: `create_message(to, subject, body, attachments)` - Compose email
   - Use Gmail API message format
   - Handle attachments (MP3 files + Beat Agreement)
2. Function: `send_email(message)` - Send via Gmail API
   - Use `gmail.users().messages().send()`
   - Handle errors (invalid email, quota exceeded)
3. Rate limiting: 1-2 second delays between emails
4. Convert Beat Agreement text to attachment (PDF or text file)

**Test**: Send a test email to yourself first!

---

### Step 7: CLI Commands (Priority 7)

**File**: `main.py`

**What to build**:
1. `list-artists` command:
   - Fetch artists from Google Drive
   - Display in a nice table
   - Store in database
2. `send-beats` command:
   - Orchestrate full workflow:
     - Fetch artists
     - Fetch beats
     - Parse beat metadata
     - For each artist:
       - Get pack number (increment)
       - Select random beats
       - Generate email
       - Send email
       - Log to database
   - Add `--dry-run` flag for testing
3. `show-history` command:
   - Query database
   - Display table with: artist, email, timestamp, pack_number, beats, status

---

## 🧪 Testing Strategy

### Phase 1: Unit Tests
- Test each service independently
- Mock API calls where possible

### Phase 2: Integration Tests
- Test with 1-2 artists first
- Send test emails to yourself
- Verify database entries

### Phase 3: Full Test
- Test with all ~40 artists
- Monitor for errors
- Check email delivery

---

## 📝 Important Notes

### Security
- ✅ `credentials.json` and `token.json` are gitignored
- ✅ Never commit sensitive data
- ✅ Vault folder ID in config.yaml is OK (not sensitive)

### Configuration
- Vault folder ID: `1D6pBAI4IDpicvLzLo9_R0qknn4y8DjCb` (already in config.yaml)
- Beat Agreement: `templates/beat_usage_agreement.txt`
- Email Template: `templates/email_template.txt`

### Dependencies
All dependencies are in `requirements.txt` and should be installed:
```bash
pip install -r requirements.txt
```

### Authentication
- Token is saved in `config/token.json`
- Run `python main.py configure` if token expires
- Test user: zobeats23@gmail.com (already added in Google Cloud)

---

## 🐛 Common Issues & Solutions

### Issue: Token expired
**Solution**: Run `python main.py configure` again

### Issue: Can't find vault folder
**Solution**: Verify folder ID in `config/config.yaml` matches your Google Drive folder

### Issue: Gmail API errors
**Solution**: Check OAuth scopes include `gmail.send`

### Issue: Database errors
**Solution**: Make sure `database/` directory exists and is writable

---

## 📚 Reference Documents

- **System Design**: `SYSTEM_DESIGN.md` - Complete architecture
- **Implementation Plan**: `IMPLEMENTATION_PLAN.md` - Detailed steps
- **Google Cloud Setup**: `docs/GOOGLE_CLOUD_SETUP.md` - OAuth setup
- **OAuth Troubleshooting**: `docs/OAUTH_FIX.md` - Common OAuth issues

---

## 🎯 Success Criteria

You'll know you're done when:
- [ ] Can list all artists from vault folder
- [ ] Can parse beat filenames and extract metadata
- [ ] Can randomly select 3-5 beats per artist
- [ ] Can send personalized emails with attachments
- [ ] Can track history in database
- [ ] Can prevent duplicates (30-day rule)
- [ ] Pack numbers increment correctly per artist

---

## 🚀 Quick Start When Returning

1. **Activate environment** (if using venv):
   ```bash
   cd C:\Users\zohay\ContactAutomation
   # venv\Scripts\activate  # if using virtual environment
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install  # Set up pre-commit hooks
   ```

3. **Verify authentication**:
   ```bash
   python main.py configure
   ```
   (Should work without re-authenticating if token is still valid)

4. **Create feature branch**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/database-service
   ```

5. **Start with Database Service**:
   - Open `services/database_service.py`
   - Implement SQLite schema
   - Write tests in `tests/unit/test_database_service.py`
   - Run: `pytest tests/unit/test_database_service.py`
   - Commit: `git commit -m "feat(database): Add SQLite schema"`

6. **Then Google Drive Service**:
   - Open `services/google_drive_service.py`
   - Use `auth_service.py` as reference for authentication
   - Write tests
   - Test fetching artists

7. **Continue in order** through the priority list above

8. **Before committing**:
   ```bash
   # Format code
   black .
   isort .
   
   # Run tests
   pytest
   
   # Check linting
   flake8 .
   ```

9. **Create Pull Request**:
   - Push branch: `git push origin feature/database-service`
   - Create PR on GitHub
   - Fill out PR template
   - Request review

---

## 💡 Tips

- **Start small**: Test each service individually before integrating
- **Use logging**: Check `logs/app.log` for debugging
- **Test emails**: Always test with your own email first
- **Dry run**: Use `--dry-run` flag when testing `send-beats`
- **Database**: Use SQLite browser tool to inspect database if needed

---

## 📞 Need Help?

- Check `SYSTEM_DESIGN.md` for architecture details
- Review `services/auth_service.py` as reference for API usage
- See `docs/` folder for setup guides
- Google API documentation:
  - [Drive API](https://developers.google.com/drive/api/v3/about-sdk)
  - [Gmail API](https://developers.google.com/gmail/api/guides)

---

**Good luck! You've got a solid foundation - now it's time to build the core functionality! 🎵**
