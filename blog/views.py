from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import Post, Comment, Category, CustomUser
from .serializers import PostSerializer, CommentSerializer, CategorySerializer
from .form import CustomUserCreationForm, PostForm, CommentForm, RegistrationForm
from .permissions import IsAuthorOrReadOnly
from .task import send_welcome_celeryemail, send_otp_email

def home(request):
    posts = Post.objects.all().order_by('-created_at') # latest first 
    return render(request, 'home1.html', {'posts': posts})

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)#creating an form
        if form.is_valid():#Validate the form data
            user = form.save()# Save the new user to the database
            # send mail using celery
            send_welcome_celeryemail.delay(user.email, user.username)
            messages.success(request, "Registration successful! Check your email for a welcome message.")
            return render(request,'login.html')
        else:
            print("Form invalid:", form.errors)
    else:
        form = RegistrationForm()
        print("Form invalid:", form.errors)
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home1')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

import random  
from django.utils import timezone
from datetime import timedelta

# Step 1: Show form to enter email
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')# Get email 
        try:
            user = CustomUser.objects.get(email=email)# Find user by email
            otp = str(random.randint(100000, 999999))# generate a 6-digit OTP
            user.otp_code = otp# Save OTP and expiry time to user record
            user.otp_expires_at = timezone.now() + timedelta(minutes=1)# setting 1 minute expiry
            user.save()           #current date and time + time duration          
            send_otp_email.delay(otp, user.email, user.username)
            messages.success(request, 'OTP has been sent to your email.')
            request.session['reset_email'] = user.email  # store temporarily for further verification
            return redirect('verify_otp')  # move to OTP verification page  
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email not found!')
    return render(request, 'forgot_password.html')

def verify_otp(request):
    email = request.session.get('reset_email')#This email identifies which user is trying to reset their password.
    if not email:
        messages.error(request, "Session expired. Please try again.")
        return redirect('forgot_password')
    user = CustomUser.objects.get(email=email) #verifying who the user is before checking the OTP.
    if request.method == 'POST':#if the form is submitted
        entered_otp = request.POST.get('otp')#Getting the entered otp
        if entered_otp == user.otp_code and not user.is_otp_expired():# it checks if the entered Otp is matched or not 
            request.session['otp_verified'] = True  
            return redirect('reset_password') 
        else:
            messages.error(request, "Invalid or expired OTP.")
    return render(request, 'verify_otp.html', {'email': email})

# Step 2: Reset password form
def reset_password(request):
    email = request.session.get('reset_email')
    otp_verified = request.session.get('otp_verified', False)
    if not email or not otp_verified:
        messages.error(request, "Unauthorized access.")
        return redirect('forgot_password')
    user = CustomUser.objects.get(email=email)
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user.set_password(password1)
            user.otp_code = ''
            user.otp_expires_at = None
            user.save()
            # clear session
            request.session.pop('reset_email', None)
            request.session.pop('otp_verified', None)
            messages.success(request, 'Password reset successfully! You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'reset_password.html', {'user': user})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return render(request, 'logout.html')


# API Views
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer
from .models import Post

 
class BlogView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get(self, request, pk=None):
        category_id = request.GET.get('category')
        if category_id is not None:
            posts = Post.objects.filter(category_id=category_id).order_by('-created_at')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # If 'pk' is provided, return one post (for API or edit)
        if pk:
            post = get_object_or_404(Post, pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Render the homepage template
            posts = Post.objects.all().order_by('-created_at')
            return render(request, 'home1.html', {'posts': posts})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response({'message': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------
class CommentView(APIView): 
    permission_classes = [IsAuthenticatedOrReadOnly] # GET comments for a post 
    def get(self, request, post_id): 
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all().order_by('-created_at') 
        serializer = CommentSerializer(comments, many=True) 
        return Response(serializer.data) # POST comment under a post 
    def post(self, request, post_id): 
        post = get_object_or_404(Post, id=post_id) 
        serializer = CommentSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save(user=request.user, post=post) 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
class CategoryView(APIView): 
    permission_classes = [IsAuthenticatedOrReadOnly] 
    def get(self, request): 
        categories = Category.objects.all() 
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    def post(self, request): 
        serializer = CategorySerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)