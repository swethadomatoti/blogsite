# Credential Rotation Guide

## Step 1: Rotate Google OAuth Credentials

### Why rotate?
Your Google OAuth Client Secret was previously exposed in GitHub history. You need to:
1. Create a new OAuth credential pair
2. Delete the old one
3. Update `.env` file locally

### How to Rotate:

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com
   - Sign in with your Google account
   - Select your project (likely "blogsite" or similar)

2. **Navigate to OAuth 2.0 Credentials**
   - Left sidebar → APIs & Services → Credentials
   - Look for "OAuth 2.0 Client IDs" section

3. **Create New Credential**
   - Click "Create Credentials" → OAuth client ID
   - Choose "Web application"
   - Set name: `blogsite-oauth-2` (or v2)
   - **Authorized JavaScript origins:**
     - http://localhost:8000
     - http://127.0.0.1:8000
     - https://yourblogsite.onrender.com (after deployment)
   - **Authorized redirect URIs:**
     - http://localhost:8000/accounts/google/login/callback/
     - http://127.0.0.1:8000/accounts/google/login/callback/
     - https://yourblogsite.onrender.com/accounts/google/login/callback/
   - Click "Create"

4. **Copy New Credentials**
   - Copy the new **Client ID** and **Client Secret**
   - Save them temporarily

5. **Update Django Admin**
   - Go to http://127.0.0.1:8000/admin
   - Login: admin / admin123
   - Navigate to: Sites Framework → Social applications
   - Edit the existing Google entry OR create new one:
     - Provider: Google
     - Name: Google OAuth
     - Client id: [paste new client ID]
     - Secret key: [paste new secret]
     - Sites: Select your site

6. **Update .env file locally**
   ```
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=YOUR_NEW_CLIENT_ID
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=YOUR_NEW_SECRET_KEY
   ```

7. **Delete Old Credential**
   - In Google Cloud Console, find the old credential (with exposed secret)
   - Delete it to prevent misuse

---

## Step 2: Rotate Gmail App Password

### Why rotate?
Your Gmail app password for email sending was exposed in GitHub. Create a new one.

### How to Rotate:

1. **Go to Google Account Security**
   - Visit: https://myaccount.google.com/security
   - Sign in with your Gmail account

2. **Enable 2-Step Verification (if not already)**
   - Left sidebar → Security
   - Look for "2-Step Verification"
   - Enable it if needed

3. **Create New App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select: Mail → Windows Computer (or your OS)
   - Google will generate a 16-character password
   - Copy it (without spaces)

4. **Update .env file**
   ```
   EMAIL_HOST_USER=swethadomatoti@gmail.com
   EMAIL_HOST_PASSWORD=YOUR_NEW_16_CHARACTER_PASSWORD
   ```

5. **Delete Old App Password**
   - In App passwords section, remove the old one to prevent misuse

---

## Step 3: Commit and Push Updated .env (Local Only!)

⚠️ **IMPORTANT: DO NOT COMMIT .env FILE TO GITHUB**

The `.env` file should stay local and in `.gitignore`. Only `.env.example` should be in Git.

Verify before pushing:
```bash
git status
```

Should NOT show `.env` in the list. It should only show:
- Changes to `.gitignore` (if modified)
- OR nothing if .env was never tracked

---

## Step 4: Add Credentials to Render Deployment

When deploying to Render, set environment variables:

1. Go to Render Dashboard
2. Select your service/app
3. Environment tab
4. Add these variables:
   ```
   SECRET_KEY=your-django-secret-key
   DEBUG=False
   EMAIL_HOST_USER=swethadomatoti@gmail.com
   EMAIL_HOST_PASSWORD=your-new-app-password
   CELERY_BROKER_URL=redis://your-redis-url:6379/0
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-new-client-id
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-new-secret
   ALLOWED_HOSTS=yourblogsite.onrender.com,www.yourblogsite.onrender.com
   ```

---

## Verification Checklist

- [ ] New Google OAuth credentials created
- [ ] Old Google credentials deleted
- [ ] Django admin social apps updated with new OAuth credentials
- [ ] New Gmail app password created
- [ ] Old Gmail app password deleted
- [ ] .env file updated locally (NOT committed to Git)
- [ ] .gitignore verified to include .env
- [ ] Tested Google login locally with new credentials
- [ ] Tested email sending locally with new password
- [ ] Ready for Render deployment with environment variables set

---

## Testing Locally

After updating credentials:

```bash
# Restart Django server
# Then test:
1. Go to http://127.0.0.1:8000/accounts/login/
2. Click "Sign in with Google"
3. Verify it redirects to new Google consent screen
4. Test password reset to verify email sending works
```

If any errors occur, check:
- Django admin panel logs
- `.env` file has correct values (no extra spaces)
- Google OAuth redirect URIs include localhost
