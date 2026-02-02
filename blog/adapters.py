from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from .task import send_welcome_celeryemail


class CustomAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        """Generate username from email or full name instead of random string."""
        if user.email:
            # Use email prefix as username
            username = user.email.split('@')[0]
        elif user.first_name and user.last_name:
            # Use first name + last name
            username = f"{user.first_name}{user.last_name}".lower()
        elif user.first_name:
            # Use first name only
            username = user.first_name.lower()
        else:
            # Fallback to default
            username = f"user_{user.id}"

        # Ensure uniqueness
        from django.contrib.auth import get_user_model
        User = get_user_model()
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        user.username = username
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin,form=None):
        """Save user and send welcome email for new social signups."""
        user = sociallogin.user
        # Check if this is a new user
        is_new = not user.pk
        user = super().save_user(request, sociallogin)
        
        if is_new:
            # Send welcome email for new Google sign-ups
            send_welcome_celeryemail.delay(user.email, user.first_name or user.username)
        
        return user

    def pre_social_login(self, request, sociallogin):
        """Auto-connect social account if user with same email exists."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not sociallogin.is_existing:
            try:
                user = User.objects.get(email=sociallogin.account.extra_data.get('email'))
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass


