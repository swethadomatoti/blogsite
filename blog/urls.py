from django.urls import path
from . import views

urlpatterns = [
    # Auth endpoints
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    
    # Home/Blog views
    path('', views.home, name='home1'),
    
    # API endpoints
    path('api/posts/', views.PostListCreateAPIView.as_view(), name='post_list_create'),
    path('api/posts/<uuid:pk>/', views.PostDetailAPIView.as_view(), name='post_detail'),
    path('api/categories/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('api/comments/', views.CommentListCreateAPIView.as_view(), name='comment_list_create'),
    path('api/comments/<uuid:pk>/', views.CommentDetailAPIView.as_view(), name='comment_detail'),
]
