import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isyswear.settings')
import django
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
import getpass

print("=== Create New Admin Account ===")
print("Note: This creates a Django superuser (is_superuser=True) for admin panel access.")
print("Admin panel login: http://127.0.0.1:8000/panel/login/")
print()

# Interactive input
username = input("Enter username: ").strip()
if not username:
    print("Username required.")
    exit(1)

email = input("Enter email (optional): ").strip() or None

password = getpass.getpass("Enter password: ").strip()
if len(password) < 8:
    print("Password too short (min 8 chars).")
    exit(1)
password_confirm = getpass.getpass("Confirm password: ").strip()
if password != password_confirm:
    print("Passwords don't match.")
    exit(1)

if User.objects.filter(username=username).exists():
    print(f"✗ User '{username}' already exists.")
    exit(1)

# Create superuser
user = User.objects.create_superuser(username, email or '', password)
user.is_staff = True  # Ensure staff access
user.save()
print(f"✓ Superuser created successfully!")
print(f"  Username: {username}")
print(f"  Email: {email or 'Not set'}")
print(f"  Password: [hidden]")
print()

# Optional profile
create_profile = input("Create Profile? (y/N): ").strip().lower()
if create_profile == 'y':
    full_name = input("Full name: ").strip() or None
    phone = input("Phone number: ").strip() or None
    address = input("Address: ").strip() or None
    Profile.objects.create(
        user=user,
        full_name=full_name,
        phone_number=phone,
        address=address
    )
    print("✓ Profile created.")

print("\nNext steps:")
print("1. python manage.py runserver")
print("2. Visit http://127.0.0.1:8000/panel/login/")
print("3. Login with new admin credentials")
print("4. Access dashboard at /panel/")
