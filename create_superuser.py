from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')
django.setup()

User = get_user_model()

# Create superuser
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print(f"✓ Superuser 'admin' created successfully")
    print(f"  Username: admin")
    print(f"  Email: admin@example.com")
    print(f"  Password: admin123")
else:
    print("✓ Superuser 'admin' already exists")
