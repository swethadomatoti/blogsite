# Google OAuth Setup Guide

## Current Status

Your Django blog is running, but **Google OAuth is not yet configured**. The application now handles this gracefully:
- Login/Register pages show a message instead of errors
- Google button appears only after OAuth is configured
- Application continues to work with traditional email/password auth

## Fix the Error

The error you saw (`SocialApp.DoesNotExist`) is now **fixed**. Pages will display:
- "Google OAuth not configured. Configure in Django admin." (until you set it up)

## Quick Setup (2 options)

### OPTION 1: Django Admin (Recommended - 5 minutes)

**Easiest method for local development:**

1. **Go to Admin Panel**
   ```
   http://127.0.0.1:8000/admin
   Login: admin
   Password: admin123
   ```

2. **Add Social Application**
   - Left sidebar → "Social applications"
   - Click "Add Social Application"

3. **Fill the Form**
   - **Provider:** Google
   - **Name:** Google OAuth
   - **Client ID:** (leave blank for now)
   - **Secret key:** (leave blank for now)
   - **Sites:** Check the site that's listed
   - Click "Save"

4. **Get Google Credentials** (next section)

5. **Edit the saved entry**
   - Go back to Social Applications
   - Click on "Google OAuth"
   - Fill in Client ID and Secret
   - Save

### OPTION 2: Environment Variables + Script (5 minutes)

**If you have Google credentials ready:**

1. **Get Google Credentials**
   - See "Get Google Credentials" section below
   - Copy Client ID and Secret

2. **Update .env file**
   ```
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-client-id-here
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-secret-here
   ```

3. **Run setup script**
   ```bash
   python setup_google_oauth.py
   ```

4. **Restart Django server**
   ```bash
   # Stop the running server (Ctrl+C)
   # Then restart it
   python manage.py runserver
   ```

---

## Get Google Credentials

### Step 1: Create Google OAuth 2.0 Credential

1. Go to: https://console.cloud.google.com/apis/credentials
2. Sign in with your Google account
3. Select your project (or create one)
4. Click "Create Credentials"
5. Choose "OAuth client ID"
6. Select "Web application"
7. Give it a name (e.g., "blogsite-local")

### Step 2: Add Authorized Redirect URIs

In the "Authorized redirect URIs" section, add:
```
http://127.0.0.1:8000/accounts/google/login/callback/
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/
http://localhost:8000/accounts/google/login/
```

**For Render deployment, also add:**
```
https://yourblogsite.onrender.com/accounts/google/login/callback/
https://yourblogsite.onrender.com/accounts/google/login/
```

### Step 3: Copy Your Credentials

- Copy the **Client ID**
- Copy the **Client Secret**
- Keep these safe!

---

## Verify Setup

After configuring, run:
```bash
python check_google_oauth.py
```

You should see:
```
✓ Google OAuth IS configured!
  Status: READY TO USE
```

---

## Test Google Login

1. **Restart the server** (if not already restarted)

2. **Go to login page**
   ```
   http://127.0.0.1:8000/login/
   ```

3. **Click "Sign in with Google"**
   - Should redirect to Google consent screen
   - After consent, creates account and logs you in

4. **Go to register page**
   ```
   http://127.0.0.1:8000/register/
   ```

5. **Click "Sign up with Google"**
   - Same flow as login
   - Creates new account if first time

---

## Troubleshooting

### "Google OAuth not configured" message appears

**Solution:** You haven't set up OAuth yet. Follow steps in OPTION 1 or OPTION 2 above.

### "Invalid redirect_uri" error from Google

**Solution:** Check your redirect URIs in Google Cloud Console. They must exactly match.

For local development, use:
- `http://127.0.0.1:8000/accounts/google/login/callback/`

### "This app is not verified" warning

**Solution:** This is normal for development apps. Click "Continue" to proceed.

### Google button doesn't appear after setup

**Solution:**
1. Restart the Django server
2. Run: `python check_google_oauth.py`
3. Verify it shows "✓ Google OAuth IS configured!"

---

## Files Related to Google OAuth Setup

| File | Purpose |
|------|---------|
| `setup_google_oauth.py` | Automatic setup script (uses .env) |
| `check_google_oauth.py` | Check current configuration |
| `blog/context_processors.py` | Makes buttons conditional |
| `blog/templates/login.html` | Shows button only if OAuth configured |
| `blog/templates/register.html` | Shows button only if OAuth configured |
| `blogsite/settings.py` | Context processor configuration |

---

## What Happens After Setup

1. **Google Button Appears**
   - Replaces the "not configured" message
   - Users can click to sign in with Google

2. **New Users via Google**
   - Account created automatically
   - Email-based username generated
   - Welcome email sent (if Celery running)

3. **Existing Users via Google**
   - Matched by email
   - Logged in automatically
   - No new account created

---

## Next: Deploy to Production

After testing locally:

1. **Get your production domain**
2. **Add to Google OAuth redirect URIs:**
   ```
   https://yourblogsite.onrender.com/accounts/google/login/callback/
   ```
3. **Set environment variables on Render:**
   - `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-prod-client-id`
   - `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-prod-secret`
4. **Deploy**

See RENDER_DEPLOYMENT.md for full instructions.

---

## Summary

- ✓ Error fixed - pages now handle missing OAuth gracefully
- ✓ Google buttons appear only after OAuth is configured
- ✓ Two setup options available (admin or script)
- ✓ Verification script to check status
- ✓ Ready for local and production use

**Next Action:** Follow OPTION 1 or 2 above to set up Google OAuth in ~5 minutes.
