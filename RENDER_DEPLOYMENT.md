# Render Deployment Guide

## Prerequisites

- Render account (https://render.com)
- GitHub repository with code (already pushed: https://github.com/swethadomatoti/blogsite.git)
- Rotated credentials (see CREDENTIAL_ROTATION.md)

## Step 1: Create Render Web Service

1. **Go to Render Dashboard**
   - https://dashboard.render.com

2. **Create New Web Service**
   - Click "New +" → Web Service
   - Select: "Build and deploy from a Git repository"
   - Paste GitHub repo URL: `https://github.com/swethadomatoti/blogsite.git`
   - Click "Connect"

3. **Configure Service**
   - **Name:** blogsite (or your preferred name)
   - **Environment:** Python 3
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```
     gunicorn blogsite.wsgi:application
     ```
   - **Plan:** Free tier (initially) or Starter ($12/month)

## Step 2: Set Environment Variables

1. **In Render Dashboard** → Your Web Service → Environment
2. **Add all these variables:**

```
DJANGO_SETTINGS_MODULE=blogsite.settings
SECRET_KEY=your-actual-secret-key-from-settings
DEBUG=False
ALLOWED_HOSTS=yourblogsite.onrender.com,www.yourblogsite.onrender.com
EMAIL_HOST_USER=swethadomatoti@gmail.com
EMAIL_HOST_PASSWORD=your-new-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
CELERY_BROKER_URL=redis://default:password@your-redis-url:6379/0
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-new-google-client-id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-new-google-secret
```

## Step 3: Set Up PostgreSQL Database (Optional)

For production, use PostgreSQL instead of SQLite:

1. **Create PostgreSQL Database**
   - In Render Dashboard → Databases
   - Click "New +" → PostgreSQL
   - Choose plan (Free tier available)
   - Save connection details

2. **Add Database URL to Environment**
   ```
   DATABASE_URL=postgresql://user:password@hostname:5432/dbname
   ```

3. **Update settings.py to use DATABASE_URL** (already supports it via `dj-database-url`)

## Step 4: Set Up Redis Cache (Optional but Recommended)

1. **Create Redis Instance**
   - Render Dashboard → Redis
   - Click "New +" → Redis
   - Copy Redis URL

2. **Add to Environment**
   ```
   REDIS_URL=redis://default:password@hostname:port
   CELERY_BROKER_URL=redis://default:password@hostname:port/0
   ```

## Step 5: Configure GitHub Integration

1. **In Render, your Web Service**
   - Render will automatically redeploy on GitHub pushes to `main` branch
   - To disable: uncheck "Auto-Deploy"

2. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Update for Render deployment"
   git push origin main
   ```

## Step 6: Deploy!

1. **Click "Deploy"** in Render Dashboard
2. **Monitor logs** for any errors
3. **Wait** for build to complete (~5-10 minutes first time)

## Step 7: Post-Deployment Tasks

### Create Django Admin Superuser (on Render)

```bash
# In Render Shell/Console:
python manage.py createsuperuser
```

Or create via script:
```bash
# Push this as a one-time script
python manage.py shell < create_admin.py
```

### Update Google OAuth Redirect URIs

1. Go to Google Cloud Console
2. Update OAuth credential redirect URIs:
   - Add: `https://yourblogsite.onrender.com/accounts/google/login/callback/`

### Test the Application

1. Visit: `https://yourblogsite.onrender.com`
2. Test login page
3. Test "Sign in with Google"
4. Create a test post
5. Test password reset (email)

## Troubleshooting

### Common Errors:

**"ModuleNotFoundError: No module named 'django'"**
- Build command didn't install dependencies
- Check: `pip install -r requirements.txt` in build command

**"DisallowedHost: Invalid HTTP_HOST"**
- Add your Render domain to ALLOWED_HOSTS environment variable
- Redeploy after updating

**"No such table: blog_post"**
- Migrations didn't run
- Add `python manage.py migrate` to build command

**"Google OAuth redirect_uri_mismatch"**
- Update Google OAuth credentials with new Render domain
- Update redirect URI to: `https://yourblogsite.onrender.com/accounts/google/login/callback/`

**"Celery tasks not running"**
- Need Redis or another broker configured
- Render provides Redis service
- Or disable Celery if not critical (set `CELERY_ALWAYS_EAGER=True` for testing)

## Production Checklist

- [ ] Environment variables set in Render
- [ ] Database configured (PostgreSQL or using SQLite)
- [ ] Redis configured for Celery
- [ ] Google OAuth credentials updated with Render domain
- [ ] Django admin accessible and superuser created
- [ ] Static files being served (collectstatic ran)
- [ ] Email sending working (test password reset)
- [ ] Google login working
- [ ] Blog posts can be created/viewed
- [ ] Comments working
- [ ] Categories accessible
- [ ] DEBUG=False verified
- [ ] ALLOWED_HOSTS includes Render domain

## Monitoring & Logs

**View Logs:**
- Render Dashboard → Your Service → Logs
- Shows real-time output from `gunicorn`

**Monitor Performance:**
- Render Dashboard → Your Service → Metrics
- CPU, Memory, Requests

**Set Up Alerts:**
- Render Dashboard → Settings → Notifications
- Get alerted on failures

## Scaling (Future)

- **Free Plan Limits:** Spins down after 15 mins of inactivity
- **Upgrade to Starter ($12/mo):** Always running, better performance
- **Add Worker Dyno:** For background Celery tasks

## Cost Estimate (Using Paid Plans)

- Web Service (Starter): $12/month
- PostgreSQL (Small): $12/month
- Redis (Small): $6/month
- **Total: ~$30/month**

Free tier is good for testing before committing to paid plans.
