import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="collapp_db",
    user="collapp_user",
    password="collapp_pass"
)

cur = conn.cursor()

# Verificar tabelas de chat
tables = ['chats', 'messages', 'wanted_applications']

for table in tables:
    cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')")
    exists = cur.fetchone()[0]
    print(f"Tabela {table}: {'Existe' if exists else 'Nao existe'}")
    
    if exists:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"Registros: {count}")

cur.close()
conn.close()