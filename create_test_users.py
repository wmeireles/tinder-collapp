import psycopg2
import uuid
from datetime import datetime
import json

conn = psycopg2.connect(
    host="localhost",
    database="collapp_db", 
    user="collapp_user",
    password="collapp_pass"
)

cur = conn.cursor()

# Usuários de teste
test_users = [
    {
        "name": "Ana Silva",
        "email": "ana@test.com",
        "bio": "Influenciadora de lifestyle e moda. Amo criar conteúdo autêntico!",
        "niches": ["fashion", "lifestyle", "beauty"],
        "social_platforms": {"instagram": "ana_silva", "tiktok": "anasilva"},
        "follower_counts": {"instagram": 50000, "tiktok": 25000},
        "country": "BR",
        "city": "São Paulo"
    },
    {
        "name": "Carlos Santos",
        "email": "carlos@test.com", 
        "bio": "Creator de tech e gaming. Sempre testando os últimos gadgets!",
        "niches": ["technology", "gaming", "reviews"],
        "social_platforms": {"youtube": "carlos_tech", "instagram": "carlos_santos"},
        "follower_counts": {"youtube": 80000, "instagram": 30000},
        "country": "BR",
        "city": "Rio de Janeiro"
    },
    {
        "name": "Maria Costa",
        "email": "maria@test.com",
        "bio": "Foodie apaixonada! Compartilho receitas e dicas culinárias.",
        "niches": ["food", "cooking", "lifestyle"],
        "social_platforms": {"instagram": "maria_cozinha", "youtube": "maria_costa"},
        "follower_counts": {"instagram": 35000, "youtube": 15000},
        "country": "BR",
        "city": "Belo Horizonte"
    },
    {
        "name": "João Oliveira",
        "email": "joao@test.com",
        "bio": "Fitness coach e lifestyle. Motivando pessoas a viverem melhor!",
        "niches": ["fitness", "health", "lifestyle"],
        "social_platforms": {"instagram": "joao_fit", "tiktok": "joao_oliveira"},
        "follower_counts": {"instagram": 45000, "tiktok": 20000},
        "country": "BR",
        "city": "Porto Alegre"
    }
]

for user_data in test_users:
    user_id = str(uuid.uuid4())
    
    # Inserir usuário
    cur.execute("""
        INSERT INTO users (id, email, password_hash, name, bio, onboarding_completed, is_active, email_verified, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (email) DO UPDATE SET
        name = EXCLUDED.name,
        bio = EXCLUDED.bio,
        onboarding_completed = EXCLUDED.onboarding_completed
        RETURNING id
    """, (
        user_id,
        user_data["email"],
        "$2b$12$dummy_hash_for_test_users",  # password_hash dummy
        user_data["name"], 
        user_data["bio"],
        True,  # onboarding_completed
        True,  # is_active
        True,  # email_verified
        datetime.now(),
        datetime.now()
    ))
    
    result = cur.fetchone()
    if result:
        user_id = result[0]
    
    # Inserir perfil
    cur.execute("""
        INSERT INTO user_profiles (user_id, niches, social_platforms, follower_counts, country, city, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
        niches = EXCLUDED.niches,
        social_platforms = EXCLUDED.social_platforms,
        follower_counts = EXCLUDED.follower_counts,
        country = EXCLUDED.country,
        city = EXCLUDED.city
    """, (
        user_id,
        user_data["niches"],  # PostgreSQL array
        json.dumps(user_data["social_platforms"]),
        json.dumps(user_data["follower_counts"]),
        user_data["country"],
        user_data["city"],
        datetime.now(),
        datetime.now()
    ))

conn.commit()
cur.close()
conn.close()

print("Usuarios de teste criados com sucesso!")