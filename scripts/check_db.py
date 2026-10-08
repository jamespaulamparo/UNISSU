import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isyswear.settings')
import django
django.setup()
from django.db import connection

print('DB vendor:', connection.vendor)
with connection.cursor() as cur:
    cur.execute('SELECT DATABASE()')
    print('Current database:', cur.fetchone()[0])
    try:
        cur.execute('SHOW TABLES')
        tables = [r[0] for r in cur.fetchall()]
        print('Tables ({}):'.format(len(tables)))
        for t in tables:
            print(' -', t)
    except Exception as e:
        print('Could not list tables:', e)
