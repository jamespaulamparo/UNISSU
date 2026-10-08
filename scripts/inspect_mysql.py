import MySQLdb as Database
print('module_file:', getattr(Database, '__file__', None))
print('release.__version__:', getattr(Database.release, '__version__', None))
print('version_info:', getattr(Database, 'version_info', None))
try:
    print('get_client_info():', Database.get_client_info())
except Exception as e:
    print('get_client_info failed:', e)
print('attributes:', [a for a in dir(Database) if a.lower().find('version')!=-1])
