import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="collapp_db",
    user="collapp_user",
    password="collapp_pass"
)

cur = conn.cursor()

# Ver todos os emails no banco
cur.execute("SELECT email, created_at FROM users ORDER BY created_at DESC")
users = cur.fetchall()

print("Usuários no banco:")
for user in users:
    print(f"  {user[0]} - {user[1]}")

cur.close()
conn.close()