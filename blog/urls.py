from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home1/', views.home, name='home1'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('BlogView/', views.BlogView.as_view(), name='BlogView'),   # Create (POST)
    path('BlogView/<int:pk>/', views.BlogView.as_view(), name='BlogDetail'),  # Update/Delete
    path('posts/<int:post_id>/comments/', views.CommentView.as_view(), name='comments'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
]
