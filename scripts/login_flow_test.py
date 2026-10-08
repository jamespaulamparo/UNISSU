import requests

base = 'http://127.0.0.1:8000'
s = requests.Session()

print('=== LOGIN PAGE TEST ===\n')

# 1. Try to access home without auth - should redirect to login
print('1. GET / (unauthenticated) - should redirect to login')
r = s.get(base + '/', allow_redirects=False)
print(f'   Status: {r.status_code}')
print(f'   Redirected to: {r.headers.get("Location", "No redirect")}\n')

# 2. Access login page directly
print('2. GET /users/login-register/')
r = s.get(base + '/users/login-register/')
print(f'   Status: {r.status_code}')
print(f'   Has form: {"form-group" in r.text}')
print(f'   Has email field: {"email" in r.text.lower()}')
print(f'   Has username field: {"username" in r.text.lower()}')
print(f'   Has password fields: {"password" in r.text.lower()}\n')

# 3. Register new user
print('3. POST /users/register/ (new user)')
csrf = s.cookies.get('csrftoken', '')
headers = {'X-CSRFToken': csrf}
user_data = {
    'username': 'newuser123',
    'email': 'newuser@example.com',
    'full_name': 'New User',
    'password1': 'SecurePass123!',
    'password2': 'SecurePass123!',
}
r = s.post(base + '/users/register/', data=user_data, headers=headers)
print(f'   Status: {r.status_code}')
print(f'   Created successfully\n')

# 4. Login as new user
print('4. POST /users/login/')
csrf = s.cookies.get('csrftoken', '')
headers = {'X-CSRFToken': csrf}
login_data = {
    'username': 'newuser123',
    'password': 'SecurePass123!',
}
r = s.post(base + '/users/login/', data=login_data, headers=headers, allow_redirects=True)
print(f'   Status: {r.status_code}')
print(f'   Final URL: {r.url}\n')

# 5. Now access home - should work (authenticated)
print('5. GET / (authenticated)')
r = s.get(base + '/')
print(f'   Status: {r.status_code}')
print(f'   Has navbar: {"navbar" in r.text}')
print(f'   Has home content: {"Welcome to iSysWear" in r.text or "Featured" in r.text}\n')

# verify uniforms names are present
for name in ['Classic White Shirt','Navy Polo','Pink Blouse','Gray Trousers','Black Cap']:
    print(name, 'on homepage:', name in r.text)


print('=== TEST COMPLETED ===')

