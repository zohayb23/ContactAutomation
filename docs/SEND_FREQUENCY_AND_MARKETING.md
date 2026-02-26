# Send Frequency, Beat Formatting, and Marketing Copy

## How often to send packs

**Recommendation: every 4–6 weeks (about once a month).**

- **30-day rule**: The app won’t send the same beat to the same artist within 30 days. Sending at least every 4–6 weeks gives enough time for variety and avoids feeling spammy.
- **Inbox placement**: Sending too often (e.g. weekly) can hurt deliverability and push you toward spam/promotions.
- **Value**: Monthly “Exclusive Beat pack #2, #3…” feels like a consistent drop, not noise.
- **Practical**: Run `python main.py send-beats` once a month (e.g. first Friday after new uploads). With 143 beats and 38 artists, you have plenty of variety for Pack #2 and beyond.

**Suggested schedule:**
First Friday of the month (or the Friday after you upload new beats), run send-beats. Optional: add a calendar reminder.

---

## Beats that need formatting

**Required format:**
`@zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3`

**Order:** Beat Name → **BPM (number)** → Key → Style.

Run this anytime to see which files need renaming:

```bash
python main.py check-beats
```


**Rule:** The **number (BPM)** must come right after the beat name, then Key, then Style. Fix those 8 and all 143 will match.

---

## LinkedIn post draft (project demo)

**Draft 1 (technical / builder-focused):**

---

I built an automation tool that takes my beat vault on Google Drive and sends personalized beat packs to artists via email—each with 3–5 random MP3s and a usage agreement, no manual copying.

Tech: Python, Google Drive & Gmail APIs, SQLite, OAuth. Features: 30-day duplicate prevention, per-artist pack numbers, rate limiting, and a CLI (list artists, send packs, view history). All behavior is test-covered and documented.

[Screenshot: terminal output]
[Screenshot: sample email with beats attached]

If you’re a producer or dev looking to automate outreach or practice system design, I’m happy to share the approach or the repo.

#Python #Automation #Producer #SoftwareEngineering #SideProject

---

**Draft 2 (shorter / story-focused):**

---

As a producer I was manually sending beats to artists one by one. So I built a CLI that:

• Pulls artists from a shared Drive folder
• Picks 3–5 random beats per person
• Sends personalized emails with attachments and a usage agreement
• Tracks everything (who got what, pack #, 30-day no-repeat)

[Screenshots: terminal + email]

Built with Python, Google APIs, and SQLite. One command and everyone gets their pack.

#Producer #Automation #Python #SideProject

---

**What to show in the post (you already have):**

- Terminal: `python main.py send-beats` (or list-artists / show-history).
- Email: subject “Exclusive Beat pack #1”, body with name + beat list, attachments (agreement + MP3s).

**Optional extras that strengthen the post:**

- Short clip of running `python main.py check-beats` (shows you care about data quality).
- One slide or screenshot: “What it does” (e.g. Drive → parse → select → email → log).
- One line on why: “So I can focus on making beats and stay consistent with artists.”
- If you’re open to it: “Repo / design doc available on request” or link to a public repo.

---

## Discord message (invite people to DM you for vault access)

**130+ beats** in the vault — trap, plugg, rnb, drill, boom bap, you name it. I send **exclusive packs** (3–5 beats + terms) straight to your inbox. No spam, no paywall. **DM me your email** and I’ll add you to the list.

---

## Quick reference

- **Send frequency:** Every 4–6 weeks (e.g. first Friday of the month).
- **Check formatting:** `python main.py check-beats`
- **Required format:** `@zobi - [Beat Name] - [BPM] - [Key] - [Style].mp3`
- **8 files** to rename in Drive (see table above); after that you have **143 beats** ready for Pack #2 and beyond.
