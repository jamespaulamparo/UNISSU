import pymysql

host = '127.0.0.1'
user = 'root'
password = 'zxCvbn_m16**'
port = 3306
dbname = 'dbIsyswear'

print('connecting to MySQL...')
conn = pymysql.connect(host=host, user=user, password=password, port=port)
conn.autocommit(True)
with conn.cursor() as cur:
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
    print(f'Database `{dbname}` ensured')
conn.close()
