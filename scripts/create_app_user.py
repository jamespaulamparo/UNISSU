import pymysql

host = '127.0.0.1'
user = 'root'
password = 'zxCvbn_m16**'
port = 3306
dbname = 'dbIsyswear'

app_user = 'isyswear_user'
app_pass = 'isyswear_pass123'

print('Connecting to MySQL as root...')
conn = pymysql.connect(host=host, user=user, password=password, port=port)
conn.autocommit(True)
with conn.cursor() as cur:
    # Create user
    cur.execute(f"CREATE USER IF NOT EXISTS `{app_user}`@`%` IDENTIFIED BY '{app_pass}'")
    # Grant privileges on DB
    cur.execute(f"GRANT ALL PRIVILEGES ON `{dbname}`.* TO `{app_user}`@`%`")
    cur.execute("FLUSH PRIVILEGES")
    print(f"App user '{app_user}' created with full access to '{dbname}'")
    print(f"Username: {app_user}")
    print(f"Password: {app_pass}")
conn.close()
print("Done.")

