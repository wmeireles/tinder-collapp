import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="collapp_db",
    user="collapp_user",
    password="collapp_pass"
)

cur = conn.cursor()

# Adicionar novas colunas à tabela wanted_posts
try:
    cur.execute("ALTER TABLE wanted_posts ADD COLUMN IF NOT EXISTS niches TEXT[]")
    cur.execute("ALTER TABLE wanted_posts ADD COLUMN IF NOT EXISTS platforms TEXT[]")
    cur.execute("ALTER TABLE wanted_posts ADD COLUMN IF NOT EXISTS sizes TEXT[]")
    cur.execute("ALTER TABLE wanted_posts ADD COLUMN IF NOT EXISTS budget VARCHAR")
    cur.execute("ALTER TABLE wanted_posts ADD COLUMN IF NOT EXISTS location VARCHAR")
    
    conn.commit()
    print("Colunas adicionadas com sucesso!")
    
except Exception as e:
    print(f"Erro: {e}")
    conn.rollback()

cur.close()
conn.close()