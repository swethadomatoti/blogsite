#!/usr/bin/env python
"""
Check and display Google OAuth setup instructions
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')
django.setup()

from allauth.socialaccount.models import SocialApp

print("=" * 60)
print("Google OAuth Configuration Status")
print("=" * 60)

try:
    google_app = SocialApp.objects.get(provider='google')
    print("\n✓ Google OAuth IS configured!")
    print(f"  Provider: {google_app.provider}")
    print(f"  Name: {google_app.name}")
    print(f"  Client ID: {google_app.client_id[:20]}...")
    print(f"  Status: READY TO USE")
    print("\nYou can now use 'Sign in with Google' buttons!")
except SocialApp.DoesNotExist:
    print("\n✗ Google OAuth NOT configured yet")
    print("\nOptions to configure:")
    print("\nOPTION 1: Via Django Admin (Recommended for first time)")
    print("  1. Go to http://127.0.0.1:8000/admin")
    print("  2. Login: admin / admin123")
    print("  3. Navigate to 'Social Applications'")
    print("  4. Click 'Add Social Application'")
    print("  5. Fill in:")
    print("     - Provider: Google")
    print("     - Name: Google OAuth")
    print("     - Client ID: [your-google-client-id]")
    print("     - Secret key: [your-google-secret]")
    print("  6. Add the current site to 'Available sites'")
    print("  7. Save")
    
    print("\nOPTION 2: Via Script (if credentials in .env)")
    print("  1. Add to .env:")
    print("     SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-client-id")
    print("     SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-secret")
    print("  2. Run: python setup_google_oauth.py")
    
    print("\nGetting Google Credentials:")
    print("  1. Go to https://console.cloud.google.com/apis/credentials")
    print("  2. Create OAuth 2.0 Client ID (Web application)")
    print("  3. Add Authorized Redirect URIs:")
    print("     - http://127.0.0.1:8000/accounts/google/login/callback/")
    print("     - http://localhost:8000/accounts/google/login/callback/")
    print("  4. Copy Client ID and Secret")
    print("  5. Use in Django admin or .env file")

except Exception as e:
    print(f"\n✗ Error: {str(e)}")

print("\n" + "=" * 60)
