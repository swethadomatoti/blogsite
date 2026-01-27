"""
Django template context processors for blog app
"""

def google_oauth_available(request):
    """Check if Google OAuth is configured and available"""
    try:
        from allauth.socialaccount.models import SocialApp
        SocialApp.objects.get(provider='google')
        return {'google_oauth_available': True}
    except Exception:
        return {'google_oauth_available': False}

