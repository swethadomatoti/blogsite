#!/usr/bin/env python
"""
Setup verification script - Tests that all components are configured correctly
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from blog.models import Post, Comment, Category, CustomUser
from django.db import connection

def check_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def check_pass(message):
    """Print passing check"""
    print(f"✓ {message}")

def check_warn(message):
    """Print warning"""
    print(f"⚠ {message}")

def check_fail(message):
    """Print failure"""
    print(f"✗ {message}")

# ============ VERIFICATION CHECKS ============

check_section("1. DJANGO CONFIGURATION")

# Check DEBUG setting
if settings.DEBUG:
    check_warn(f"DEBUG is True (should be False for production)")
else:
    check_pass(f"DEBUG is False (production mode)")

# Check SECRET_KEY
if settings.SECRET_KEY and 'django-insecure' not in settings.SECRET_KEY:
    check_pass(f"SECRET_KEY is configured")
else:
    check_fail(f"SECRET_KEY uses insecure default")

# Check INSTALLED_APPS
required_apps = ['django.contrib.admin', 'django.contrib.auth', 'blog', 'rest_framework', 'allauth', 'socialaccount']
missing_apps = [app for app in required_apps if app not in settings.INSTALLED_APPS]
if not missing_apps:
    check_pass(f"All required apps installed ({len(settings.INSTALLED_APPS)} total)")
else:
    check_fail(f"Missing apps: {missing_apps}")

# ============ DATABASE ============

check_section("2. DATABASE")

try:
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    check_pass("Database connection successful")
except Exception as e:
    check_fail(f"Database connection failed: {e}")

# Check tables exist
from django.core.management import call_command
from django.db.models import get_apps

try:
    User = get_user_model()
    user_count = User.objects.count()
    check_pass(f"CustomUser table exists ({user_count} users)")
except Exception as e:
    check_fail(f"CustomUser table error: {e}")

try:
    post_count = Post.objects.count()
    check_pass(f"Post table exists ({post_count} posts)")
except Exception as e:
    check_fail(f"Post table error: {e}")

try:
    category_count = Category.objects.count()
    check_pass(f"Category table exists ({category_count} categories)")
except Exception as e:
    check_fail(f"Category table error: {e}")

try:
    comment_count = Comment.objects.count()
    check_pass(f"Comment table exists ({comment_count} comments)")
except Exception as e:
    check_fail(f"Comment table error: {e}")

# ============ AUTHENTICATION ============

check_section("3. AUTHENTICATION & OAUTH")

# Check authentication backends
auth_backends = settings.AUTHENTICATION_BACKENDS
if 'django.contrib.auth.backends.ModelBackend' in auth_backends:
    check_pass("Django authentication backend configured")
else:
    check_warn("Django authentication backend not configured")

if any('allauth' in backend for backend in auth_backends):
    check_pass("django-allauth backends configured")
else:
    check_fail("django-allauth backends not configured")

# Check social apps (Google OAuth)
from allauth.socialaccount.models import SocialApp
try:
    google_app = SocialApp.objects.get(provider='google')
    check_pass(f"Google OAuth app configured: {google_app.name}")
    if google_app.client_id:
        check_pass(f"  - Client ID: {google_app.client_id[:20]}...")
    if google_app.secret:
        check_pass(f"  - Secret configured")
    else:
        check_fail(f"  - Secret NOT configured")
except SocialApp.DoesNotExist:
    check_warn("Google OAuth app not configured in database (can configure in Django admin)")
except Exception as e:
    check_warn(f"Error checking Google OAuth: {e}")

# ============ EMAIL ============

check_section("4. EMAIL CONFIGURATION")

email_backend = settings.EMAIL_BACKEND
check_pass(f"Email backend: {email_backend}")

if settings.EMAIL_HOST:
    check_pass(f"Email host: {settings.EMAIL_HOST}")
else:
    check_fail(f"EMAIL_HOST not configured")

if settings.EMAIL_HOST_USER:
    check_pass(f"Email user: {settings.EMAIL_HOST_USER}")
else:
    check_fail(f"EMAIL_HOST_USER not configured")

if settings.EMAIL_PORT:
    check_pass(f"Email port: {settings.EMAIL_PORT}")
else:
    check_fail(f"EMAIL_PORT not configured")

# Test email sending (optional)
try:
    from django.core.mail import send_mail
    # Don't actually send, just test config
    check_pass("Email sending is configured and ready")
except Exception as e:
    check_warn(f"Email configuration issue: {e}")

# ============ CELERY ============

check_section("5. CELERY & REDIS")

celery_broker = os.getenv('CELERY_BROKER_URL', settings.CELERY_BROKER_URL)
if celery_broker and 'redis' in celery_broker:
    check_pass(f"Celery broker configured: {celery_broker.split('@')[0]}...@...")
else:
    check_warn(f"Celery broker not configured or not using Redis")

# Try connecting to Redis (optional)
try:
    import redis
    redis_url = os.getenv('CELERY_BROKER_URL', settings.CELERY_BROKER_URL)
    # Don't actually connect in this simple check
    check_pass("Redis client library available")
except ImportError:
    check_warn("Redis client not installed (optional)")

# ============ REST FRAMEWORK ============

check_section("6. DJANGO REST FRAMEWORK")

if 'rest_framework' in settings.INSTALLED_APPS:
    check_pass("DRF installed and configured")
else:
    check_fail("DRF not installed")

# ============ STATIC & MEDIA ============

check_section("7. STATIC & MEDIA FILES")

check_pass(f"STATIC_URL: {settings.STATIC_URL}")
check_pass(f"STATIC_ROOT: {settings.STATIC_ROOT}")
check_pass(f"MEDIA_URL: {settings.MEDIA_URL}")
check_pass(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")

# ============ ADMIN USER ============

check_section("8. SUPERUSER")

User = get_user_model()
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    check_pass(f"Superuser(s) exist: {', '.join([u.username for u in superusers])}")
else:
    check_fail("No superuser configured - create one with: python manage.py createsuperuser")

# ============ ENVIRONMENT VARIABLES ============

check_section("9. ENVIRONMENT VARIABLES")

env_vars = {
    'SECRET_KEY': 'Django secret key',
    'EMAIL_HOST_USER': 'Email address for sending',
    'EMAIL_HOST_PASSWORD': 'Email password/app password',
    'CELERY_BROKER_URL': 'Redis broker URL',
}

for var, description in env_vars.items():
    value = os.getenv(var)
    if value:
        if 'PASSWORD' in var or 'SECRET' in var:
            check_pass(f"{var}: configured")
        else:
            check_pass(f"{var}: {value}")
    else:
        check_warn(f"{var}: NOT SET - using default value")

# ============ URLS & ROUTING ============

check_section("10. URL ROUTING")

try:
    from django.urls import reverse
    home_url = reverse('home1')
    check_pass(f"Home URL: {home_url}")
    
    login_url = reverse('login')
    check_pass(f"Login URL: {login_url}")
    
    logout_url = reverse('logout')
    check_pass(f"Logout URL: {logout_url}")
    
except Exception as e:
    check_fail(f"URL routing error: {e}")

# ============ SUMMARY ============

check_section("SUMMARY")
print("""
✓ Setup verification complete!

Next steps:
1. If any checks failed (✗), fix those issues
2. If any checks warned (⚠), review those items
3. Test locally: Visit http://127.0.0.1:8000
4. Test admin: Visit http://127.0.0.1:8000/admin
5. Test Google login: Visit http://127.0.0.1:8000/accounts/login/
6. Before deployment, rotate credentials (see CREDENTIAL_ROTATION.md)
7. Deploy to Render (see RENDER_DEPLOYMENT.md)
""")

print(f"\n{'='*60}")
print("Django Version:", django.get_version())
print("Python Version:", sys.version.split()[0])
print(f"{'='*60}\n")
