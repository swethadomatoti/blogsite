# Django Blog Application

A modern Django blog platform with Google OAuth authentication, RESTful API, and Celery task queue support.

## Features

- **User Authentication**
  - Traditional login/registration with email verification
  - Google OAuth 2.0 integration for seamless sign-in
  - Password reset functionality with OTP verification
  - Custom user model with UUID primary keys

- **Blog Functionality**
  - Create, read, update, delete blog posts
  - Organize posts by categories
  - Comment system with nested replies
  - Image upload support for posts
  - Lazy-loaded comments for better performance

- **REST API**
  - Full REST API for posts, comments, and categories
  - DRF permissions and authentication
  - Serializers for complex data structures

- **Background Tasks**
  - Celery task queue with Redis broker
  - Automated email sending for welcome and password resets
  - Asynchronous operations support

- **Admin Interface**
  - Django admin panel for content management
  - User and content moderation tools
  - Email log tracking

## Tech Stack

- **Backend:** Django 5.2.8, Django REST Framework 3.14.0
- **Authentication:** django-allauth 0.61.1 (OAuth support)
- **Database:** SQLite3 (dev), PostgreSQL (production)
- **Cache/Queue:** Redis 5.0.1, Celery 5.6.2
- **Server:** Gunicorn 22.0.0 (ASGI/WSGI)
- **Frontend:** Bootstrap 5.3.2, Axios, Intersection Observer API
- **Email:** Gmail SMTP (TLS)

## Local Development

### Prerequisites

- Python 3.10+
- Redis server running locally
- Virtual environment

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/swethadomatoti/blogsite.git
   cd blogsite
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** (copy from `.env.example`)
   ```bash
   cp .env.example .env
   ```
   
   Fill in your credentials:
   ```
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   CELERY_BROKER_URL=redis://127.0.0.1:6379/0
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-client-id
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-secret
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

   Visit: http://127.0.0.1:8000

8. **Start Celery (in another terminal)**
   ```bash
   celery -A blogsite worker -l info
   ```

## Running Locally

### Access Points

- **Home Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin
- **Login:** http://127.0.0.1:8000/login/
- **Register:** http://127.0.0.1:8000/register/
- **API Posts:** http://127.0.0.1:8000/api/posts/
- **API Categories:** http://127.0.0.1:8000/api/categories/

### Testing Features

1. **Traditional Login**
   - Register with email/password
   - Login with credentials

2. **Google OAuth**
   - Click "Sign in with Google" on login page
   - Authorize application
   - Auto-redirect to home page

3. **Create Blog Post**
   - Click "Create New Post" on home page
   - Fill title, content, select category
   - Upload image (optional)
   - Click "Publish Post"

4. **Comment on Posts**
   - Click "Comments" button on any post
   - Type comment and click "Comment"
   - Lazy-loads only when expanded

5. **Admin Features**
   - Login to /admin with superuser
   - Manage posts, categories, comments
   - View user accounts
   - Configure OAuth apps

## Verification

Run setup verification:
```bash
python verify_setup.py
```

This checks:
- Django configuration
- Database connectivity
- OAuth setup
- Email configuration
- Celery/Redis
- Static/Media files
- Superuser exists
- URL routing

## Credential Rotation

⚠️ **Important:** If credentials were exposed, rotate them immediately.

See `CREDENTIAL_ROTATION.md` for step-by-step instructions:
1. Create new Google OAuth credentials
2. Generate new Gmail app password
3. Update Django admin
4. Delete old credentials

## Deployment to Render

See `RENDER_DEPLOYMENT.md` for complete deployment guide.

Quick steps:
1. Create Render Web Service connected to GitHub
2. Set environment variables
3. Configure PostgreSQL database
4. Set up Redis
5. Deploy!

### Environment Variables for Production

```
DEBUG=False
ALLOWED_HOSTS=yourblogsite.onrender.com
SECRET_KEY=your-production-secret
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=production-client-id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=production-secret
```

## Project Structure

```
blogsite/
├── blog/                          # Main blog app
│   ├── migrations/               # Database migrations
│   ├── templates/                # HTML templates
│   │   ├── home1.html           # Main blog page
│   │   ├── login.html           # Login form
│   │   ├── register.html        # Registration form
│   │   └── ...
│   ├── models.py                # Data models
│   ├── views.py                 # View handlers & API
│   ├── serializers.py           # REST serializers
│   ├── adapters.py              # OAuth adapters
│   ├── urls.py                  # URL routing
│   ├── forms.py                 # Django forms
│   └── task.py                  # Celery tasks
├── blogsite/                     # Project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Root URL routing
│   ├── asgi.py                  # ASGI config
│   ├── wsgi.py                  # WSGI config
│   └── celery.py                # Celery config
├── manage.py                     # Django CLI
├── requirements.txt              # Python dependencies
├── .env                          # Local secrets (not in Git)
├── .env.example                  # Template for .env
├── .gitignore                    # Git ignore rules
├── CREDENTIAL_ROTATION.md        # Security guide
├── RENDER_DEPLOYMENT.md          # Deployment guide
└── verify_setup.py              # Setup verification script
```

## API Endpoints

### Posts
- `GET /posts/` - List all posts
- `POST /posts/` - Create new post (auth required)
- `GET /posts/<id>/` - Get post details
- `PUT /posts/<id>/` - Update post (author only)
- `DELETE /posts/<id>/` - Delete post (author only)

### Comments
- `GET /comments/` - List comments (supports `?post_id=<id>`)
- `POST /comments/` - Create comment (auth required)
- `DELETE /comments/<id>/` - Delete comment (author only)

### Categories
- `GET /categories/` - List all categories

### Authentication
- `POST /login/` - Login with email/password
- `GET /accounts/google/login/callback/` - Google OAuth callback
- `POST /logout/` - Logout

## Security Features

- ✓ CSRF protection enabled
- ✓ SQL injection prevention (ORM)
- ✓ XSS protection
- ✓ CORS configured
- ✓ Secrets in environment variables (not in code)
- ✓ Django security middleware
- ✓ Password hashing with PBKDF2
- ✓ OAuth 2.0 for third-party auth
- ✓ Email verification for password reset

## Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
- Activate virtual environment: `venv\Scripts\activate`
- Install requirements: `pip install -r requirements.txt`

### "Connection refused" when accessing localhost:8000
- Django server not running: `python manage.py runserver`
- Check port 8000 is not in use

### Google OAuth not working
- Verify OAuth credentials in Django admin: /admin/socialaccount/socialapp/
- Check redirect URI matches your domain
- Test locally: http://127.0.0.1:8000/accounts/login/

### Email not sending
- Verify Gmail app password (not account password)
- Enable 2-factor authentication on Gmail
- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env
- Test in Django shell: `python manage.py shell`

### Celery tasks not running
- Start Celery worker: `celery -A blogsite worker -l info`
- Verify Redis is running: `redis-cli ping`
- Check Celery settings in settings.py

## Contributing

1. Create a branch for your feature
2. Make your changes
3. Test locally
4. Commit with clear messages
5. Push and create pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check this README
2. Review `CREDENTIAL_ROTATION.md` for security issues
3. Review `RENDER_DEPLOYMENT.md` for deployment help
4. Check Django docs: https://docs.djangoproject.com/
5. Check allauth docs: https://django-allauth.readthedocs.io/

## Author

Swetha Domatoti

---

**Last Updated:** January 27, 2026
**Django Version:** 5.2.8
**Python Version:** 3.10+
