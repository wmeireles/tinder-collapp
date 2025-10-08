import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="collapp_db", 
    user="collapp_user",
    password="collapp_pass"
)

cur = conn.cursor()

# Verificar se tabela wanted_posts existe
cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'wanted_posts')")
exists = cur.fetchone()[0]
print(f"Tabela wanted_posts existe: {exists}")

if exists:
    # Verificar estrutura
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'wanted_posts'")
    columns = cur.fetchall()
    print("Colunas da tabela wanted_posts:")
    for col in columns:
        print(f"  {col[0]}: {col[1]}")

cur.close()
conn.close()