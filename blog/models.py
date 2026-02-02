from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.conf import settings
 

class CustomUser(AbstractUser):
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)  # new field
    otp_expires_at = models.DateTimeField(blank=True, null=True)   

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150,unique=True,validators=[username_validator],
                                error_messages={'unique': 'A user with that username already exists.'},
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                verbose_name='username')
    def is_otp_expired(self):
        if not self.otp_expires_at:
            return True
        return timezone.now() > self.otp_expires_at
    def __str__(self):
        return self.username

class Category(models.Model):
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

     


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Link comment to post
    content = models.TextField()                                # Comment text
    created_at = models.DateTimeField(auto_now_add=True)     # Auto timestamp

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'
#--------------------------------------------------------------------