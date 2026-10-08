import requests

base = 'http://127.0.0.1:8000'

s = requests.Session()

print('GET /')
r = s.get(base + '/')
print(r.status_code)

print('GET login page')
r = s.get(base + '/users/login-register/')
print(r.status_code)

# register
username = 'httptestuser'
password = 'HttpTest123!'
print('POST register')
# fetch CSRF token from the login page cookies
csrf = s.cookies.get('csrftoken', '')
headers = {'X-CSRFToken': csrf}

r = s.post(base + '/users/register/', data={
    'username': username,
    'full_name': 'HTTP Test',
    'password1': password,
    'password2': password,
 }, headers=headers)
print('status', r.status_code)

print('POST login')
csrf = s.cookies.get('csrftoken', '')
headers = {'X-CSRFToken': csrf}
r = s.post(base + '/users/login/', data={'username': username, 'password': password}, allow_redirects=True, headers=headers)
print('login status', r.status_code)
print('final url', r.url)

print('GET profile')
r = s.get(base + '/users/profile/')
print('profile status', r.status_code)
print('length', len(r.text))

