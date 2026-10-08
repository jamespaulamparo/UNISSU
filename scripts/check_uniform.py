import os
import sys
import django

# ensure project root on path
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isyswear.settings')
django.setup()

from django.test import Client

c = Client()
from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')

# log in so middleware lets us through
from django.contrib.auth.models import User
if not User.objects.filter(username='temp').exists():
    User.objects.create_user('temp','temp@example.com','pass')
c.login(username='temp', password='pass')

resp = c.get('/uniforms/1/')
print('status', resp.status_code)
html = resp.content.decode()
print('contains add_to_cart url?', '/cart/add/' in html)
print('contains /cart/add/1/', '/cart/add/1/' in html)
# optionally print around potential form
start = html.find('form')
if start != -1:
    print(html[start:start+500])
else:
    print('no form tag found')

