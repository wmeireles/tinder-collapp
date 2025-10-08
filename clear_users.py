import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="collapp_db",
    user="collapp_user",
    password="collapp_pass"
)

cur = conn.cursor()

# Deletar todos os usuários (cuidado!)
cur.execute("DELETE FROM users")
conn.commit()

print("Todos os usuários foram removidos!")

cur.close()
conn.close()