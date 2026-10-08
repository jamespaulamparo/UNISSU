import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isyswear.settings')
django.setup()

from django.conf import settings
print(f"DEBUG: {settings.DEBUG}")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")

# Check if CSS file exists
css_path = os.path.join(settings.STATIC_ROOT, 'css', 'base.css')
print(f"\nCSS file exists at {css_path}: {os.path.exists(css_path)}")

# List files in static dir
import glob
print(f"\nFiles in static folder:")
for f in glob.glob(os.path.join(settings.STATIC_ROOT, '**', '*.*'), recursive=True):
    print(f"  {f}")
