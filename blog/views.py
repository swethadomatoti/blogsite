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
from .form import CustomUserCreationForm, PostForm, CommentForm
from .permissions import IsAuthorOrReadOnly
import random
import string


# Helper function to generate OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


# Auth views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home1')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home1')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['user_id'] = str(user.id)
            # In production, send OTP via email
            print(f"OTP for {email}: {otp}")
            messages.info(request, f'OTP sent to {email}')
            return redirect('verify_otp')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email not found')
    return render(request, 'forgot_password.html')


def verify_otp_view(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if otp_input == request.session.get('otp'):
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'verify_otp.html')


def reset_password_view(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
        else:
            user_id = request.session.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully!')
            # Clear session
            del request.session['otp']
            del request.session['email']
            del request.session['user_id']
            del request.session['otp_verified']
            return redirect('login')
    
    return render(request, 'reset_password.html')


# Main blog view
@login_required(login_url='login')
def home(request):
    categories = Category.objects.all()
    posts = Post.objects.all()
    return render(request, 'home1.html', {
        'categories': categories,
        'posts': posts,
    })


# API Views
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]





