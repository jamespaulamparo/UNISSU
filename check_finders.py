import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isyswear.settings')
django.setup()

from django.conf import settings
from django.contrib.staticfiles.finders import get_finders

print("STATICFILES_FINDERS:")
for finder in get_finders():
    print(f"  {finder.__class__.__name__}")

print("\nSearching for css/base.css:")
for finder in get_finders():
    for path, storage in finder.list('.'):
        if 'base' in path and 'css' in path:
            print(f"  Found: {path} in {storage.location if hasattr(storage, 'location') else storage}")
