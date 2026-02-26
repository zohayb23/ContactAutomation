# Scheduling Beat Packs (Windows Task Scheduler)

You can schedule packs to send automatically (e.g. **first Friday of every month**) using Windows Task Scheduler. Your PC must be on and logged in at the scheduled time.

---

## Option 1: Windows Task Scheduler (recommended)

### Step 1: Create the task

1. Press **Win + R**, type `taskschd.msc`, press Enter.
2. In Task Scheduler, click **Create Basic Task** (or **Create Task** for more options).
3. **Name:** `Contact Automation - Send Beat Packs`  
   **Description:** Sends beat packs to all artists in vault.
4. Click **Next**.

### Step 2: Trigger (when to run)

1. Choose **Monthly**.
2. Click **Next**.
3. Set the month (e.g. every 1 month), day (e.g. **First** and **Friday**), and a time (e.g. **10:00 AM**).
4. Click **Next**.

### Step 3: Action (what to run)

1. Choose **Start a program**.
2. **Program/script:**  
   `C:\Users\zohay\ContactAutomation\scripts\send_beats_scheduled.bat`  
   (Use your real project path if different.)
3. **Start in (optional):**  
   `C:\Users\zohay\ContactAutomation`
4. Click **Next**, then **Finish**.

### Step 4: Run only when logged on (important)

1. In Task Scheduler, find your task and double‑click it.
2. Open the **General** tab.
3. Select **Run only when user is logged on** (so the Google OAuth token can be used).
4. Check **Run with highest privileges** only if you need it; usually leave unchecked.
5. Click **OK**.

### Step 5: Test the task

1. Right‑click the task → **Run**.
2. Check that emails send (or check `logs\scheduled_send.log` and `python main.py show-history`).

---

## Option 2: Use the batch file path from your real project

If your project lives somewhere else, edit **`scripts/send_beats_scheduled.bat`** and leave it as-is (it already uses `%~dp0..` so the batch file’s folder’s parent = project root). In Task Scheduler, set:

- **Program/script:**  
  `C:\Users\zohay\ContactAutomation\scripts\send_beats_scheduled.bat`  
  (replace with your actual path to `send_beats_scheduled.bat`.)

- **Start in:**  
  Your project root, e.g. `C:\Users\zohay\ContactAutomation`.

---

## Option 3: Run with a virtual environment

If you use a venv, edit **`scripts/send_beats_scheduled.bat`** and replace the `python` line with your venv Python, e.g.:

```bat
"%PROJECT_DIR%\venv\Scripts\python.exe" main.py send-beats
```

Then schedule that same batch file as in Option 1.

---

## Notes

- **Token expiry:** Google tokens can expire. If a scheduled run fails with an auth error, run `python main.py configure` once (browser sign‑in), then the next scheduled run should work.
- **PC must be on:** The task runs only when the computer is on at the scheduled time. Sleep/hibernate can prevent it; adjust power settings if you want it to run overnight.
- **Log:** Each run appends to `logs\scheduled_send.log` (date, time, exit code). Check that file if something doesn’t send.
- **Dry run:** To test the script without sending, temporarily change the batch to run `python main.py send-beats --dry-run`.

---

## Quick reference

| What              | Where / How |
|-------------------|-------------|
| Run task manually | Task Scheduler → right‑click task → Run |
| View send history| `python main.py show-history` |
| Check next run    | Task Scheduler → task → **Next Run Time** |
| Edit schedule     | Task Scheduler → double‑click task → Triggers tab |

Your vault is ready: **132 beats**, all correctly formatted. After you set the task, Pack #2 (and beyond) will go out on the schedule you choose.
