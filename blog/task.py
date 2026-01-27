from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_celeryemail(recipient_email, user_name):
    """Send welcome email to new users."""
    subject = 'Welcome to Our Blog!'
    message = f'''
    Hi {user_name},
    
    Welcome to our blog platform! We're excited to have you join our community.
    
    You can now:
    - Create and publish blog posts
    - Comment on other posts
    - Explore different categories
    
    Happy blogging!
    
    Best regards,
    The Blog Team
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient_email],
            fail_silently=False,
        )
        return f"Email sent to {recipient_email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"


@shared_task
def send_password_reset_email(recipient_email, reset_token):
    """Send password reset email."""
    reset_url = f"http://yourdomain.com/reset-password/?token={reset_token}"
    subject = 'Password Reset Request'
    message = f'''
    Click the link below to reset your password:
    {reset_url}
    
    This link expires in 24 hours.
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient_email],
            fail_silently=False,
        )
        return f"Reset email sent to {recipient_email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"
