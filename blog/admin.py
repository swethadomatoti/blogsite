from django.contrib import admin
from .models import CustomUser, Post, Comment, Category


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_staff']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    list_filter = ['category', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    search_fields = ['content', 'user__username', 'post__title']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
