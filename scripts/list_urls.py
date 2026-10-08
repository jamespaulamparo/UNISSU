import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','isyswear.settings')
import django
django.setup()
from django.urls import get_resolver
r = get_resolver()
names = [n for n in r.reverse_dict.keys() if isinstance(n, str)]
print(sorted(names))
for n in sorted(names):
    print(n)
