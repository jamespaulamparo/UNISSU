import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Delete all users
c.execute('DELETE FROM auth_user')
deleted_users = c.rowcount

# Optional: clear related sessions containing user IDs
c.execute("DELETE FROM django_session WHERE session_data LIKE '%\"auth_user_id%'")
deleted_sessions = c.rowcount

conn.commit()
conn.close()

print(f"✓ Deleted {deleted_users} user(s)")
print(f"✓ Deleted {deleted_sessions} session(s)")
print("Database reset. Refresh /panel/users/ to confirm.")
