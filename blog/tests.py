from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment, Category

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass123')
        self.category = Category.objects.create(name='Tech')

    def test_create_post(self):
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category=self.category
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass123')
        self.category = Category.objects.create(name='Tech')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            category=self.category
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            content='Test comment',
            user=self.user,
            post=self.post
        )
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.post, self.post)
