import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="collapp_db",
    user="collapp_user", 
    password="collapp_pass"
)

cur = conn.cursor()

# Criar tabela wanted_posts
cur.execute("""
CREATE TABLE IF NOT EXISTS wanted_posts (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::text,
    author_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    collaboration_type VARCHAR NOT NULL,
    requirements TEXT,
    deadline TIMESTAMP,
    status VARCHAR DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
""")

# Criar tabela wanted_applications
cur.execute("""
CREATE TABLE IF NOT EXISTS wanted_applications (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::text,
    wanted_post_id VARCHAR NOT NULL REFERENCES wanted_posts(id),
    applicant_id UUID NOT NULL REFERENCES users(id),
    message TEXT,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
""")

conn.commit()
cur.close()
conn.close()

print("Tabelas wanted_posts e wanted_applications criadas!")