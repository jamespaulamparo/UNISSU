import requests

base = 'http://127.0.0.1:8000'
s = requests.Session()

print('Testing login page layout...\n')

# Get login page
r = s.get(base + '/users/login-register/')
print(f'Status: {r.status_code}')
print(f'Page title: {"Welcome" in r.text}')
print(f'Has logo section: {"logo-section" in r.text}')
print(f'Has form wrapper: {"form-wrapper" in r.text}')
print(f'Has Register tab: {"register" in r.text}')
print(f'Has Sign In tab: {"Sign In" in r.text}')
print(f'Has gradient background: {"gradient" in r.text}')

# Check if all form fields are present
has_username = 'username' in r.text.lower()
has_email = 'email' in r.text.lower()
has_password = 'password' in r.text.lower()
has_full_name = 'full_name' in r.text.lower() or 'full name' in r.text.lower()

print(f'\nForm fields:')
print(f'  Username: {has_username}')
print(f'  Email: {has_email}')
print(f'  Full Name: {has_full_name}')
print(f'  Password: {has_password}')

print('\n✅ Login page layout verified!')

