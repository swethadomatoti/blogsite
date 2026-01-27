#!/usr/bin/env python
"""
Setup Google OAuth credentials in Django admin
Run this to configure Google authentication without manual admin panel entry
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')
django.setup()

from allauth.socialaccount.models import SocialApp, SocialAccount
from django.contrib.sites.models import Site

def setup_google_oauth():
    """Setup Google OAuth in Django admin"""
    
    # Get Google credentials from environment
    google_client_id = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
    google_secret = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
    
    if not google_client_id or not google_secret:
        print("""
ERROR: Google OAuth credentials not found!

Please set these environment variables in .env file:
  SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-client-id
  SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-secret-key

Get credentials from: https://console.cloud.google.com/apis/credentials

Steps:
1. Create OAuth 2.0 Credential (Web application)
2. Add Authorized Redirect URIs:
   - http://127.0.0.1:8000/accounts/google/login/callback/
   - http://localhost:8000/accounts/google/login/callback/
3. Copy Client ID and Secret to .env
4. Run this script again
        """)
        return False
    
    try:
        # Check if Google OAuth app already exists
        google_app = SocialApp.objects.get(provider='google')
        print(f"[UPDATE] Google OAuth app already exists")
        
        # Update credentials if different
        if google_app.client_id != google_client_id or google_app.secret != google_secret:
            google_app.client_id = google_client_id
            google_app.secret = google_secret
            google_app.save()
            print(f"[UPDATED] Credentials updated")
        else:
            print(f"[OK] Credentials match current settings")
            
    except SocialApp.DoesNotExist:
        # Create new Google OAuth app
        print("[CREATE] Creating Google OAuth app...")
        
        # Get the current site
        site = Site.objects.get_current()
        
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=google_client_id,
            secret=google_secret,
        )
        
        # Add site to the app
        google_app.sites.add(site)
        google_app.save()
        
        print(f"[SUCCESS] Google OAuth app created!")
        print(f"  Provider: google")
        print(f"  Name: Google OAuth")
        print(f"  Client ID: {google_client_id[:20]}...")
        print(f"  Site: {site.domain}")
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False
    
    print("\n✓ Google OAuth is now configured!")
    print("  You can now use 'Sign in with Google' buttons")
    return True

if __name__ == '__main__':
    print("="*60)
    print("Django Google OAuth Setup")
    print("="*60)
    setup_google_oauth()
    print("="*60)
