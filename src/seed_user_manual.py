import pymysql
import bcrypt
import uuid

conn = pymysql.connect(host='mysql', port=3306, user='root', password='123456', database='db_condominiums')
cur = conn.cursor()

cur.execute("SELECT id FROM users WHERE email = 'admin@admin.com' AND deleted_at IS NULL LIMIT 1")
row = cur.fetchone()
if row:
    print(f'User exists (id={row[0]}), updating password...')
    pw = bcrypt.hashpw('12345678'.encode(), bcrypt.gensalt(10)).decode()
    cur.execute("UPDATE users SET password_hash = %s, status = 'active', token_version = 1 WHERE id = %s", (pw, row[0]))
else:
    pw = bcrypt.hashpw('12345678'.encode(), bcrypt.gensalt(10)).decode()
    uid = str(uuid.uuid4())
    cur.execute("INSERT INTO users (uuid, email, password_hash, status, token_version, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())",
                (uid, 'admin@admin.com', pw, 'active', 1))
    conn.commit()
    user_id = cur.lastrowid
    print(f'Created user id={user_id}')

    # Create profile
    cur.execute("INSERT INTO user_profiles (uuid, user_id, first_name, last_name) VALUES (%s, %s, %s, %s)",
               (str(uuid.uuid4()), user_id, 'Admin', 'User'))
    print('Created profile')

conn.commit()
conn.close()
print('Done!')
print('Credentials: admin@admin.com / 12345678')