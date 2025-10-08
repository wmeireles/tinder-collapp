import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="collapp_db",
    user="collapp_user",
    password="collapp_pass"
)

cur = conn.cursor()

# Ver todos os wanted posts
cur.execute("SELECT title, description, niches, platforms, sizes, budget, location, created_at FROM wanted_posts ORDER BY created_at DESC")
posts = cur.fetchall()

print("Anúncios salvos no backend:")
for i, post in enumerate(posts, 1):
    print(f"\n{i}. {post[0]}")
    print(f"   Descrição: {post[1]}")
    print(f"   Nichos: {post[2]}")
    print(f"   Plataformas: {post[3]}")
    print(f"   Tamanhos: {post[4]}")
    print(f"   Orçamento: {post[5]}")
    print(f"   Local: {post[6]}")
    print(f"   Criado: {post[7]}")

cur.close()
conn.close()