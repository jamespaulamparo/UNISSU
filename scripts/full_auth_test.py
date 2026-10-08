import requests
import time
import re

base = 'http://127.0.0.1:8000'
s = requests.Session()

print('=== COMPREHENSIVE AUTH FLOW TEST ===\n')

# 1. GET login page
print('1. GET login page')
r = s.get(base + '/users/login-register/')
print(f'   Status: {r.status_code}')
csrf = s.cookies.get('csrftoken', '')
print(f'   CSRF token obtained: {len(csrf) > 0}\n')

# 2. Register new user with email
print('2. POST register with email')
headers = {'X-CSRFToken': csrf}
user_data = {
    'username': 'testuser_full',
    'email': 'testuser@example.com',
    'full_name': 'Test User Full',
    'password1': 'SecurePass123!',
    'password2': 'SecurePass123!',
}
r = s.post(base + '/users/register/', data=user_data, headers=headers)
print(f'   Status: {r.status_code}')
print(f'   Registered: testuser_full\n')

# 3. Try to login (should work even if email not verified for now)
print('3. POST login')
csrf = s.cookies.get('csrftoken', '')
headers = {'X-CSRFToken': csrf}
login_data = {
    'username': 'testuser_full',
    'password': 'SecurePass123!',
}
r = s.post(base + '/users/login/', data=login_data, headers=headers, allow_redirects=True)
print(f'   Status: {r.status_code}')
print(f'   Redirect to: {r.url}\n')

# 4. GET profile
print('4. GET profile (authenticated)')
r = s.get(base + '/users/profile/')
print(f'   Status: {r.status_code}')
print(f'   Profile page contains email: {"Email" in r.text}\n')

# 4a. POST updated profile data
print('4a. POST update profile info')
csrf = s.cookies.get('csrftoken', '')
headers = {'X-CSRFToken': csrf}
profile_data = {
    'full_name': 'Updated Name',
    'phone_number': '1234567890',
    'address': '123 Main St',
}
r = s.post(base + '/users/profile/', data=profile_data, headers=headers, allow_redirects=True)
print(f'   Status: {r.status_code}, redirected to {r.url}')
print(f'   New name shown: {"Updated Name" in r.text}\n')
print(f'   Phone number shown: {"1234567890" in r.text}')
print(f'   Address shown: {"123 Main St" in r.text}\n')

# 5. GET change password form
print('5. GET change password form')
r = s.get(base + '/users/change-password/')
print(f'   Status: {r.status_code}\n')

# 6. POST change password
print('6. POST change password')
csrf = s.cookies.get('csrftoken', '')
headers = {'X-CSRFToken': csrf}
pwd_data = {
    'old_password': 'SecurePass123!',
    'new_password1': 'NewSecurePass123!',
    'new_password2': 'NewSecurePass123!',
}
r = s.post(base + '/users/change-password/', data=pwd_data, headers=headers, allow_redirects=True)
print(f'   Status: {r.status_code}')
print(f'   Changed successfully (redirected): {r.url}\n')

# 7. Logout
print('7. POST logout')
r = s.post(base + '/users/logout/', allow_redirects=True)
print(f'   Status: {r.status_code}\n')

# 8. Test rate limiting on login attempts
print('8. TEST RATE LIMITING (10+ login attempts)')
s2 = requests.Session()
for i in range(12):
    r = s2.get(base + '/users/login-register/')
    csrf = s2.cookies.get('csrftoken', '')
    headers = {'X-CSRFToken': csrf}
    r = s2.post(base + '/users/login/', data={'username': 'wrong', 'password': 'wrong'}, headers=headers)
    if i >= 9:
        print(f'   Attempt {i+1}: Status {r.status_code}, Limited: {"Too many" in r.text}')

print('\n=== ALL TESTS COMPLETED ===')

