# Fix: OAuth Access Denied Error (403)

## Problem
You're seeing: "Access blocked: ArtistAutomation has not completed the Google verification process"
Error 403: access_denied

## Solution: Add Yourself as a Test User

Since your app is in "Testing" mode (which is correct for personal use), you need to add yourself as a test user.

### Step-by-Step Fix:

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Make sure your project is selected

2. **Navigate to OAuth Consent Screen**
   - Click "APIs & Services" in the left sidebar
   - Click "OAuth consent screen"

3. **Add Test Users**
   - Scroll down to the "Test users" section
   - Click the "+ ADD USERS" button
   - Enter your email address: **zobeats23@gmail.com**
   - Click "ADD"
   - You should see your email appear in the test users list

4. **Verify App Status**
   - At the top of the OAuth consent screen, you should see:
     - Publishing status: "Testing"
     - This is correct! You don't need to publish for personal use.

5. **Try Again**
   - Go back to your terminal
   - Run: `python main.py configure`
   - The browser should now allow you to sign in

## Important Notes:

- **Testing Mode**: Perfect for personal use. No verification needed.
- **Test Users**: Only users you add can use the app.
- **No Publishing Required**: For personal use, you can stay in Testing mode forever.

## If You Still Get Errors:

1. **Check the email matches exactly**
   - The email you add as test user must match the email you sign in with
   - Case-sensitive: zobeats23@gmail.com (not Zobeats23@gmail.com)

2. **Wait a few minutes**
   - Sometimes changes take a minute to propagate

3. **Clear browser cache**
   - Try in an incognito/private window

4. **Check OAuth Consent Screen Settings**
   - Make sure scopes are added (Drive and Gmail)
   - User type should be "External" (unless you have Workspace)

## Quick Checklist:

- [ ] OAuth consent screen is in "Testing" mode
- [ ] Your email (zobeats23@gmail.com) is in the "Test users" list
- [ ] You're signing in with the same email
- [ ] Both Drive and Gmail APIs are enabled
- [ ] OAuth credentials are created (Desktop app)

Once you've added yourself as a test user, try `python main.py configure` again!
