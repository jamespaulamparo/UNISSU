import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isyswear.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth.models import User

c = Client()

print('GET /')
r = c.get('/')
print('status', r.status_code)

print('GET /users/login-register/')
r = c.get('/users/login-register/')
print('status', r.status_code)

# Register a test user
username = 'testuser1'
password = 'TestPass123!'

# Ensure user doesn't already exist
User.objects.filter(username=username).delete()
print('POST register')
r = c.post('/users/register/', {'username': username, 'full_name': 'Test User', 'password1': password, 'password2': password})
print('register status', r.status_code)

print('POST login')
r = c.post('/users/login/', {'username': username, 'password': password}, follow=True)
print('login status', r.status_code)
print('redirect chain:', r.redirect_chain)
print('logged in user:', r.wsgi_request.user.username if r.wsgi_request.user.is_authenticated else 'anonymous')

print('GET /users/profile/')
r = c.get('/users/profile/')
print('profile status', r.status_code)
print('profile content length', len(r.content))
