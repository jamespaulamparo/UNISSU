import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isyswear.settings')
import django
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@example.com'
password = 'Admin123!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✓ Superuser created successfully!')
    print(f'  Username: {username}')
    print(f'  Email: {email}')
    print(f'  Password: {password}')
    print(f'\nAccess admin at: http://127.0.0.1:8000/admin/')
else:
    print(f'✗ User "{username}" already exists')
