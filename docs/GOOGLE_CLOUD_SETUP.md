# Google Cloud Project Setup Guide

This guide will walk you through setting up Google Cloud Project with the necessary APIs and credentials.

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account (use the same account that has access to your vault folder)
3. Click on the project dropdown at the top (next to "Google Cloud")
4. Click **"NEW PROJECT"**
5. Enter project details:
   - **Project name**: `ContactAutomation` (or any name you prefer)
   - **Organization**: Leave as default (No organization)
6. Click **"CREATE"**
7. Wait for the project to be created (takes a few seconds)
8. Make sure your new project is selected in the dropdown

---

## Step 2: Enable Google Drive API

1. In the Google Cloud Console, make sure your project is selected
2. Go to **"APIs & Services"** → **"Library"** (left sidebar)
   - Or use this direct link: https://console.cloud.google.com/apis/library
3. Search for **"Google Drive API"**
4. Click on **"Google Drive API"**
5. Click **"ENABLE"** button
6. Wait for it to enable (takes a few seconds)

---

## Step 3: Enable Gmail API

1. Still in **"APIs & Services"** → **"Library"**
2. Search for **"Gmail API"**
3. Click on **"Gmail API"**
4. Click **"ENABLE"** button
5. Wait for it to enable

---

## Step 4: Configure OAuth Consent Screen

Before creating credentials, you need to configure the OAuth consent screen.

1. Go to **"APIs & Services"** → **"OAuth consent screen"** (left sidebar)
2. Select **"External"** (unless you have a Google Workspace account)
3. Click **"CREATE"**
4. Fill in the required fields:
   - **App name**: `Contact Automation System`
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
5. Leave other fields as default
6. Click **"SAVE AND CONTINUE"**
7. On the **"Scopes"** page, click **"SAVE AND CONTINUE"** (we'll add scopes via code)
8. On the **"Test users"** page:
   - Click **"+ ADD USERS"**
   - Enter your email address (the one you'll use for sending emails)
   - Click **"ADD"**
9. Click **"SAVE AND CONTINUE"**
10. Review the summary and click **"BACK TO DASHBOARD"**

---

## Step 5: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** → **"Credentials"** (left sidebar)
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**
4. If prompted to configure consent screen, you've already done it in Step 4
5. Configure the OAuth client:
   - **Application type**: Select **"Desktop app"**
   - **Name**: `Contact Automation Desktop Client`
6. Click **"CREATE"**
7. A dialog will appear with your credentials:
   - **Client ID**: (long string)
   - **Client Secret**: (shorter string)
8. Click **"DOWNLOAD JSON"** button
9. Save the file (it will be named something like `client_secret_xxxxx.json`)

---

## Step 6: Set Up Credentials in Project

1. Rename the downloaded file to `credentials.json`
2. Move it to your project's `config/` folder:
   ```
   ContactAutomation/config/credentials.json
   ```
3. **IMPORTANT**: This file is gitignored and should NEVER be committed to version control

---

## Step 7: Get Your Vault Folder ID

You need the ID of your Google Drive "vault" folder.

1. Open Google Drive in your browser
2. Navigate to your "vault" folder
3. Look at the URL in your browser's address bar:
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HERE
   ```
4. Copy the `FOLDER_ID_HERE` part (long string of letters and numbers)
5. Save this for the next step
---

## Step 8: Update Configuration

1. Open `config/config.yaml` in your project
2. Find the line:
   ```yaml
   vault_folder_id: ""
   ```
3. Replace it with your folder ID:
   ```yaml
   vault_folder_id: "YOUR_FOLDER_ID_HERE"
   ```
4. Save the file

---

## Step 9: Verify Setup

Your `config/` folder should now contain:
```
config/
├── __init__.py
├── config.yaml          # Updated with vault_folder_id
└── credentials.json     # Downloaded from Google Cloud
```

---

## Step 10: Test Authentication (Next Step)

Once you've completed all the above steps, we'll test the authentication by running:

```bash
python main.py configure
```

This will:
1. Open a browser window
2. Ask you to sign in to Google
3. Request permissions for Drive and Gmail access
4. Save the authentication token

---

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Make sure you added your email as a test user in OAuth consent screen (Step 4)
- Make sure both APIs are enabled (Steps 2 & 3)

### "The OAuth client was not found"
- Make sure you downloaded the credentials JSON file
- Make sure it's named `credentials.json` and in the `config/` folder

### "Invalid grant" or "Token expired"
- Delete `config/token.json` if it exists
- Run the authentication again

---

## Security Notes

⚠️ **NEVER share or commit these files:**
- `config/credentials.json` - OAuth client credentials
- `config/token.json` - Authentication token (created after first auth)
- `.env` - Environment variables

✅ **These are already in `.gitignore`**

---

## What's Next?

After completing this setup:
1. Run `python main.py configure` to authenticate
2. Continue with database service implementation
3. Start building the core functionality

---

## Quick Checklist

- [ ] Created Google Cloud Project
- [ ] Enabled Google Drive API
- [ ] Enabled Gmail API
- [ ] Configured OAuth consent screen
- [ ] Added yourself as test user
- [ ] Created OAuth 2.0 credentials (Desktop app)
- [ ] Downloaded credentials JSON
- [ ] Renamed to `credentials.json`
- [ ] Moved to `config/` folder
- [ ] Got vault folder ID from Google Drive URL
- [ ] Updated `config/config.yaml` with folder ID
- [ ] Ready to test authentication

---

Once you've completed all steps, let me know and we'll proceed with testing the authentication!
