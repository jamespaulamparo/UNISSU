import requests

base='http://127.0.0.1:8000'
s = requests.Session()

# register/login quickly
user_data = {
    'username': 'layouttester',
    'email': 'layout@test.com',
    'full_name': 'Layout Tester',
    'password1': 'TestPass123!',
    'password2': 'TestPass123!',
}
# get csrf
r = s.get(base + '/users/login-register/')
csrftoken = s.cookies.get('csrftoken', '')
headers = {'X-CSRFToken': csrftoken}
# try to register (may fail if exists)
r = s.post(base + '/users/register/', data=user_data, headers=headers)
# login
login_data = {'username': 'layouttester', 'password': 'TestPass123!'}
r = s.post(base + '/users/login/', data=login_data, headers=headers)

# now fetch uniforms
res = s.get(base+'/uniforms/')
print('status', res.status_code)
print(res.text[:4000])

