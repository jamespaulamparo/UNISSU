from django.db import connection

with connection.cursor() as c:
    c.execute('DELETE FROM users_emailverification')
    print('emailverification rows deleted')
