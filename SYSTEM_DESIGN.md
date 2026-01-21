# Contact Automation System - System Design Document

## 1. Overview

**Problem Statement:**
Automate personalized email distribution to artists in a shared Google Drive folder, including randomly selected beats (3-5 per artist) as attachments or links.

**Scale:**

- Current: ~40 artists
- Expected growth: 100s of artists
- Frequency: Weekly (every Friday after beat upload)
- Beats: ~135 beats currently, growing collection (weekly uploads)
- File types: All MP3 files (~3 MB each) - conversion complete

---

## 2. Requirements

### Functional Requirements

1. **Extract artist information** from Google Drive shared folder
   - Names and emails of users with access to "vault" folder
2. **Select random beats** (3-5 per artist) from the folder
3. **Generate personalized emails** with:
   - Artist name
   - Beat titles with metadata (BPM, key, style)
   - Beat attachments (3-5 MP3 files per email)
   - Beat Usage Agreement document (attached to every email)
4. **Send emails via Gmail** to all artists
5. **Track sending history**:
   - Timestamp
   - Artist name & email
   - Beats sent
   - Status (sent/failed)

### Non-Functional Requirements

- **Reliability**: Handle invalid emails gracefully
- **Observability**: Logging and audit trails
- **Rate Limiting**: Avoid Gmail spam detection (stay in primary inbox)
- **Idempotency**: Track what was sent - prevent sending same beats to same artist within 30 days
- **Local Deployment**: CLI tool for single-user use
- **Beat Agreement**: Must attach Beat Usage Agreement document to every email

---

## 3. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Application (Python)                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Google     │  │    Gmail     │  │   Local      │     │
│  │   Drive      │  │     API      │  │   Database   │     │
│  │   Service    │  │   Service    │  │  (SQLite)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘           │
│                            │                                │
│                    ┌───────▼────────┐                      │
│                    │  Email Service │                      │
│                    │   (Orchestrator)│                     │
│                    └─────────────────┘                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. **Google Drive Service**

- **Purpose**: Extract artist list and beat files
- **Responsibilities**:
  - Authenticate with Google Drive API
  - List users with access to "vault" folder (permissions API)
  - Fetch file metadata (MP3 files only)
  - Download or generate shareable links for beats
- **API Endpoints Used**:
  - `drive.permissions().list()` - Get folder permissions (users)
  - `drive.files().list()` - List files in folder
  - `drive.files().get()` - Get file metadata

#### 2. **Beat Parser Service**

- **Purpose**: Extract metadata from beat filenames
- **Responsibilities**:
  - Parse filename pattern: `@zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3`
  - Extract: producer name, beat name, BPM, key, artist/style category
  - Store parsed metadata in database
- **Example Parsing**:
  - `@zobi - tundra - 136 - Cmin - travis.mp3` →
    - Beat Name: "tundra"
    - BPM: 136
    - Key: Cmin
    - Category: travis (style/artist reference)
  - `@zobi - splash - 116 - F#min - afrobeat.mp3` →
    - Beat Name: "splash"
    - BPM: 116
    - Key: F#min
    - Category: afrobeat (genre type)

#### 3. **Beat Selection Service**

- **Purpose**: Randomly select 3-5 beats per artist with duplicate prevention
- **Responsibilities**:
  - Filter audio files (MP3 only)
  - Random selection algorithm (ensure variety)
  - Check duplicate prevention: same beats to same artist only after 30 days
  - Track selections to avoid exact duplicates in same batch
- **Algorithm**:
  - Query database for last send date to artist
  - If < 30 days since last send, exclude previously sent beats
  - Shuffle all remaining beats (purely random, no style variety enforcement)
  - Select 3-5 unique beats per artist
  - Track selections to avoid exact duplicates in same batch

#### 4. **Email Template Service**

- **Purpose**: Generate personalized email content
- **Responsibilities**:
  - Load email template
  - Replace placeholders (artist name, beat titles with metadata)
  - Format beat list with details (name, BPM, key, style)
- **Template Variables**:
  - `{artist_name}`
  - `{beat_list}` (formatted list of beat names only, e.g., "tundra, hope, splash")
- **Default Template**:

  ```
  Hey {artist_name},

  I have some exclusive beats for you! Lmk if you want to use them, make sure you reach out to me so we have an agreement if you post them on publishing platforms.

  {beat_list}

  Best,
  zobi
  ```

#### 5. **Gmail Service**

- **Purpose**: Send emails with attachments
- **Responsibilities**:
  - Authenticate with Gmail API
  - Compose email (subject with pack number, body, attachments)
  - Set subject line: "Exclusive Beat pack #{pack_number}" (increments per artist)
  - Attach selected beats (3-5 MP3 files)
  - Attach Beat Usage Agreement document (from local template, required for every email)
  - Handle rate limiting (delays between sends)
  - Send email
  - Handle errors (invalid email, quota exceeded)
  - Update artist's last_pack_number in database after successful send
- **API Endpoints Used**:
  - `gmail.users().messages().send()` - Send email
- **Rate Limiting Strategy**:
  - Delay between emails (1-2 seconds)
  - Batch processing with delays
  - Respect Gmail quotas (500/day free, 2000/day Workspace)

#### 6. **History/Database Service**

- **Purpose**: Track email sending history
- **Responsibilities**:
  - Store artist information
  - Store beat metadata (parsed from filenames)
  - Log email sends (timestamp, status, beats)
  - Track artist-beat relationships for duplicate prevention
  - Query history for reporting
- **Schema**:

  ```sql
  artists (id, name, email, added_date, last_pack_number)

  beats (id, filename, beat_name, bpm, key, style_category, file_type, file_size, added_date)

  email_history (
    id, artist_id, timestamp,
    pack_number,
    beats_sent (JSON array of beat IDs),
    status, error_message
  )

  artist_beat_history (
    id, artist_id, beat_id, sent_date,
    UNIQUE(artist_id, beat_id, sent_date)
  )
  ```

#### 7. **CLI Interface**

- **Purpose**: User interaction
- **Responsibilities**:
  - Command-line interface
  - Display progress
  - Show history table
  - Configuration management
- **Commands**:
  - `send-beats` - Main command to send beats
  - `show-history` - Display sending history
  - `list-artists` - Show all artists
  - `configure` - Setup credentials

---

## 4. Data Flow

### Main Workflow: Send Beats to Artists

```
1. User runs CLI command: `python main.py send-beats`
   │
2. Initialize Services
   ├─> Load configuration (credentials, template)
   ├─> Connect to Google Drive API
   ├─> Connect to Gmail API
   └─> Initialize SQLite database
   │
3. Fetch Artist List
   ├─> Google Drive: Get folder permissions
   ├─> Extract user emails and names
   └─> Store/update in database
   │
4. Fetch Beat Files
   ├─> Google Drive: List MP3 files in folder
   ├─> Parse filenames (extract beat name, BPM, key, style)
   └─> Store beat information with metadata
   │
5. Load Beat Agreement Document
   ├─> Load from local template file (`templates/beat_usage_agreement.txt`)
   └─> Convert to PDF or prepare as attachment
   │
6. For Each Artist:
   │
   ├─> Check Duplicate Prevention
   │   └─> Query database: last send date to this artist
   │   └─> If < 30 days, exclude previously sent beats
   │
   ├─> Select Random Beats (3-5)
   │   └─> Beat Selection Service
   │
   ├─> Generate Email
   │   ├─> Load template
   │   ├─> Replace {artist_name}
   │   ├─> Replace {beat_list} (simple list of beat names)
   │   ├─> Get pack number for artist (increment from last send)
   │   └─> Prepare attachments
   │
   ├─> Send Email
   │   ├─> Gmail API: Compose message
   │   ├─> Set subject: "Exclusive Beat pack #{pack_number}" (increments per artist)
   │   ├─> Attach selected beats (3-5 MP3 files, ~9-15 MB total)
   │   ├─> Attach Beat Usage Agreement document (from local template)
   │   ├─> Apply rate limiting (delay)
   │   └─> Send via Gmail API
   │
   ├─> Log Result
   │   ├─> Record timestamp
   │   ├─> Store beats sent
   │   └─> Update status (sent/failed)
   │
   └─> Continue to next artist
   │
6. Display Summary
   └─> Show table: artist, email, timestamp, beats, status
```

---

## 5. Technical Decisions & Trade-offs

### 5.1 Email Attachments vs. Links

**Option A: Attach MP3 files directly**

- ✅ Artists receive files immediately
- ❌ Gmail 25MB limit per email (multiple beats may exceed)
- ❌ Slower sending (upload time)
- ❌ Higher bandwidth usage

**Option B: Generate shareable Google Drive links**

- ✅ No size limits
- ✅ Faster sending
- ✅ Lower bandwidth
- ❌ Artists need to click links (extra step)
- ❌ Link permissions need management

**Recommendation**: **MP3-Only Attachments**

- **File Size Analysis**:
  - All beats are MP3 files (~3 MB each) - conversion complete
  - 3-5 MP3s = 9-15 MB total (well under 25MB limit)
- **Strategy**:
  - All files are MP3 format
  - Attach MP3 files directly (3-5 beats per email)
  - All files stay under 25MB limit
  - Artists receive files immediately, no extra clicks needed

### 5.2 Rate Limiting Strategy

**Why Rate Limiting Matters:**

- Gmail may flag rapid-fire emails as spam
- Staying in primary inbox requires natural sending patterns
- Gmail quotas: 500 emails/day (free), 2000/day (Workspace)

**Strategy:**

- **Delay between emails**: 1-2 seconds (simulates human behavior)
- **Batch delays**: Pause every 10 emails (30 seconds)
- **Daily limit check**: Stop if approaching quota
- **Exponential backoff**: If errors occur, increase delays

### 5.3 Database Choice

**SQLite** (Recommended for local deployment)

- ✅ No server setup required
- ✅ File-based, easy backup
- ✅ Sufficient for 100s of records
- ✅ Built into Python

**Alternative: JSON file**

- Simpler but less queryable
- Not recommended for history tracking

### 5.4 Authentication

**OAuth 2.0 Flow** (Required for Google APIs)

- User grants permission once
- Refresh token stored securely
- Re-authenticate when token expires

**Service Account** (Alternative)

- Not suitable for accessing user's personal Drive/Gmail
- Would require sharing folder with service account

### 5.5 Filename Parsing Strategy

**Pattern**: `@zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3`

**Examples**:

- `@zobi - tundra - 136 - Cmin - travis.mp3`
- `@zobi - hope - 75 - Cmin - future.mp3`
- `@zobi - splash - 116 - F#min - afrobeat.mp3`

**Parsing Logic**:

1. Split by `-` (space-dash-space) delimiter
2. Extract components:
   - Producer: First part (after `@`)
   - Beat Name: Second part
   - BPM: Third part (convert to integer)
   - Key: Fourth part (musical key)
   - Style/Artist: Fifth part (before file extension)
   - File Type: Extension (.mp3)

**Benefits**:

- Rich metadata without ID3 tags
- Enables filtering by style (trap, drill, rnb, afro, etc.)
- Can personalize beat selection by artist preference
- Easy to query and organize

### 5.6 Beat Agreement Document

**Requirement**: Beat Usage Agreement must be attached to every email

**Implementation**:

- **Option 1 (Recommended)**: Use local template file (`templates/beat_usage_agreement.txt`)
  - Convert to PDF or attach as text file
  - No need to search Google Drive
  - More reliable and faster
- **Option 2**: Locate document in Google Drive (by filename or specific location)
  - Download document (PDF or DOCX)
  - Cache document locally to avoid repeated downloads
- Attach to every email alongside beat files
- **Content**: Full agreement text provided (credit requirements, pricing, contact info)

---

## 6. File Structure

```
ContactAutomation/
├── main.py                 # CLI entry point
├── config/
│   ├── config.yaml        # Configuration file
│   └── credentials.json    # OAuth tokens (gitignored)
├── services/
│   ├── __init__.py
│   ├── google_drive_service.py
│   ├── gmail_service.py
│   ├── beat_parser_service.py      # Parse filename metadata
│   ├── beat_selection_service.py
│   ├── email_template_service.py
│   └── database_service.py
├── templates/
│   └── email_template.txt  # Email template
├── assets/
│   └── beat_agreement.pdf  # Cached Beat Usage Agreement (optional)
├── database/
│   └── history.db          # SQLite database
├── logs/
│   └── app.log            # Application logs
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (gitignored)
├── .gitignore
└── README.md
```

---

## 7. API Requirements & Costs

### Google Drive API

- **Free tier**: 1,000 requests/day
- **Cost**: Free for this use case
- **Authentication**: OAuth 2.0

### Gmail API

- **Free tier**:
  - 500 emails/day (personal Gmail)
  - 2,000 emails/day (Google Workspace)
- **Cost**: Free for this use case
- **Authentication**: OAuth 2.0

### Storage

- **Local**: SQLite database (minimal)
- **Google Drive**: Using existing storage (no additional cost)

**Total Cost**: **$0** (within free tiers)

---

## 8. Error Handling & Edge Cases

### Invalid Emails

- Validate email format before sending
- Log invalid emails, continue with others
- Report in summary

### Missing Beats

- If folder has <3 beats: Send all available
- If no beats: Skip artist or send email without beats (configurable)

### API Quota Exceeded

- Check quota before starting
- Stop gracefully if limit reached
- Resume from last sent artist on next run

### Network Failures

- Retry with exponential backoff (3 attempts)
- Log failures
- Continue with next artist

### Duplicate Prevention

- **Rule**: Same beats to same artist only after 30 days
- Check database before sending: query last send date to artist
- Exclude beats sent to this artist in last 30 days from selection pool
- Different artists can receive same beats (no restriction)
- Track in `artist_beat_history` table for efficient queries

---

## 9. Security Considerations

1. **Credentials Storage**

   - OAuth tokens in `credentials.json` (gitignored)
   - Never commit sensitive data
   - Use environment variables for secrets

2. **Email Privacy**

   - BCC option (all artists in one email) vs. individual emails
   - Recommendation: Individual emails (more personal, better tracking)

3. **Google Drive Access**
   - Only read permissions needed
   - OAuth scope: `drive.readonly`, `gmail.send`

---

## 10. Future Enhancements (Backlog)

### Recruiter Automation

- Similar architecture, different data source (Excel)
- Share components: Gmail Service, Database Service
- Different email template

### Additional Features

- Web UI for easier management
- Scheduling (automated Friday sends)
- Analytics dashboard (open rates, click rates if using links)
- A/B testing different email templates

---

## 11. Implementation Phases

### Phase 1: Core Functionality (MVP)

1. Google Drive integration (list artists, list beats)
2. Beat selection algorithm
3. Gmail integration (send emails)
4. Basic CLI interface
5. Simple logging

### Phase 2: History & Tracking

1. SQLite database setup
2. History logging
3. History display command
4. Error handling improvements

### Phase 3: Polish & Reliability

1. Rate limiting
2. Comprehensive error handling
3. Configuration management
4. Better logging
5. Documentation

---

## 12. Resolved Questions ✅

1. **Email Template**: ✅ Provided - "Hey {artist_name}, I have some exclusive beats for you! Lmk if you want to use them, make sure you reach out to me so we have an agreement if you post them on publishing platforms"
2. **Beat Metadata**: ✅ Filename parsing - Pattern: `@zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3`
3. **Beat Categories**: ✅ Extracted from filename (last part: artist/style like "travis", "future", "afrobeat", "drill", "rnb")
4. **Attachment Size**: ✅ All beats are MP3 (~3 MB each) → Use MP3 attachments (3-5 beats = 9-15 MB total) - conversion complete
5. **Duplicate Prevention**: ✅ 30 days minimum between sending same beats to same artist
6. **Total Beats**: ✅ ~135 beats in vault folder
7. **Beat Agreement**: ✅ Must attach Beat Usage Agreement document to every email
8. **Beat Agreement Content**: ✅ Provided - Full text document created as template

## 12.1 Resolved Questions ✅

1. **Beat Agreement Location**: ✅ Use local template file (`templates/beat_usage_agreement.txt`) - ignore vault folder version

   - **Note**: User mentioned the agreement in vault is old - should we update the template? (Current template matches provided text)

2. **Beat List Formatting**: ✅ Simple format - Just beat names (e.g., "tundra, hope, splash")

   - No metadata in email body (BPM, key, style kept in database for tracking only)

3. **Email Subject Line**: ✅ "Exclusive Beat pack #{pack_number}"

   - Pack number increments per artist (artist's first email = pack #1, second = pack #2, etc.)
   - Tracked in database: `artists.last_pack_number` and `email_history.pack_number`

4. **Beat Selection Variety**: ✅ Purely random selection
   - No style variety enforcement
   - Simple random shuffle and select 3-5 beats

---

## 13. Next Steps

1. **Review this design** - Does this align with your vision?
2. **Answer open questions** - Help refine the design
3. **Set up Google Cloud Project** - Enable APIs, get credentials
4. **Create project structure** - Initialize repository
5. **Begin Phase 1 implementation**

---

## Summary

This system design provides:

- ✅ Scalable architecture (handles 100s of artists)
- ✅ Reliable email delivery with rate limiting
- ✅ Complete history tracking
- ✅ Error handling and logging
- ✅ Zero cost (within free API tiers)
- ✅ Extensible for future features (recruiters)

**Key Technologies:**

- Python (backend)
- Google Drive API (artist & beat data)
- Gmail API (email sending)
- SQLite (history tracking)
- OAuth 2.0 (authentication)
- Filename parsing (regex/string manipulation)

**Key Design Decisions:**

1. ✅ **MP3-only attachments** - Convert/use MP3s (3-5 beats = 9-15 MB, under 25MB limit)
2. ✅ **Filename parsing** - Extract rich metadata from structured filenames
3. ✅ **30-day duplicate prevention** - Same beats to same artist only after 30 days
4. ✅ **Rate limiting** - 1-2 second delays to stay in primary inbox
5. ✅ **Comprehensive tracking** - Full history with beat metadata and pack numbers
6. ✅ **Beat Agreement attachment** - Required document in every email (from local template)
7. ✅ **Pack number tracking** - Incremental pack numbers per artist ("Exclusive Beat pack #1", "#2", etc.)
8. ✅ **Simple beat list** - Just beat names in email body (metadata in database only)
9. ✅ **Random selection** - Purely random beat selection (no style variety enforcement)

**✅ All questions answered! Ready to proceed with implementation!**
