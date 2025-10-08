import psycopg2

# Conectar ao banco
conn = psycopg2.connect(
    host="localhost",
    database="collapp_db",
    user="collapp_user",
    password="collapp_pass"
)

cur = conn.cursor()

# Atualizar planos para maiúsculo
cur.execute("UPDATE users SET plan = 'FREE' WHERE plan = 'free'")
cur.execute("UPDATE users SET plan = 'PRO' WHERE plan = 'pro'")
cur.execute("UPDATE users SET plan = 'ENTERPRISE' WHERE plan = 'enterprise'")

conn.commit()
cur.close()
conn.close()

print("Planos atualizados com sucesso!")