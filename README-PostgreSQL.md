# 🐘 PostgreSQL Setup - Collapp Backend

## 🚀 Quick Start

### Docker Compose (Recomendado)
```bash
# Iniciar PostgreSQL
docker-compose up -d postgres

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs postgres
```

### Docker Run (Alternativo)
```bash
# Executar PostgreSQL standalone
docker run -d \
  --name collapp_postgres \
  -e POSTGRES_DB=collapp_db \
  -e POSTGRES_USER=collapp_user \
  -e POSTGRES_PASSWORD=collapp_pass \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine

# Conectar ao banco
docker exec -it collapp_postgres psql -U collapp_user -d collapp_db
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
# Database
POSTGRES_DB=collapp_db
POSTGRES_USER=collapp_user
POSTGRES_PASSWORD=collapp_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Connection URLs
DATABASE_URL=postgresql://collapp_user:collapp_pass@localhost:5432/collapp_db?client_encoding=utf8
DATABASE_URL_ASYNC=postgresql+asyncpg://collapp_user:collapp_pass@localhost:5432/collapp_db
```

### Strings de Conexão
```python
# Sync (SQLAlchemy)
DATABASE_URL = "postgresql://user:pass@host:port/db"

# Async (AsyncPG)
DATABASE_URL_ASYNC = "postgresql+asyncpg://user:pass@host:port/db"

# Com SSL (Produção)
DATABASE_URL = "postgresql://user:pass@host:port/db?sslmode=require"
```

## 📊 Migrações com Alembic

### Comandos Básicos
```bash
# Inicializar Alembic (já feito)
alembic init alembic

# Criar nova migração
alembic revision --autogenerate -m "Add user profiles"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1

# Ver histórico
alembic history

# Ver migração atual
alembic current
```

### Configuração Multi-Ambiente
```bash
# Desenvolvimento
alembic -x environment=dev upgrade head

# Produção
alembic -x environment=prod upgrade head
```

## 🌱 Dados de Teste

### Executar Seed
```bash
# Criar dados de exemplo
python scripts/seed_data.py

# Via Docker
docker-compose exec api python scripts/seed_data.py
```

## 💾 Backup e Restore

### Backup
```bash
# Backup local
./scripts/backup.sh

# Backup via Docker
docker exec collapp_postgres pg_dump -U collapp_user collapp_db > backup.sql

# Backup comprimido
docker exec collapp_postgres pg_dump -U collapp_user collapp_db | gzip > backup.sql.gz
```

### Restore
```bash
# Restore local
./scripts/restore.sh backups/collapp_db_20241006_120000.sql.gz

# Restore via Docker
docker exec -i collapp_postgres psql -U collapp_user -d collapp_db < backup.sql
```

## 🏥 Health Checks

### Endpoints
```bash
# Health básico
curl http://localhost:8000/health/

# Health do banco
curl http://localhost:8000/health/db

# Health detalhado
curl http://localhost:8000/health/detailed
```

### Docker Health Check
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U collapp_user -d collapp_db"]
  interval: 10s
  timeout: 5s
  retries: 5
```

## ⚡ Performance e Otimização

### Índices Importantes
```sql
-- Busca por email (único)
CREATE INDEX idx_users_email ON users(email);

-- Filtros por nicho
CREATE INDEX idx_profiles_niches ON user_profiles USING gin(niches);

-- Busca textual
CREATE INDEX idx_users_name_trgm ON users USING gin(name gin_trgm_ops);

-- Plataformas sociais
CREATE INDEX idx_profiles_social_platforms ON user_profiles USING gin(social_platforms);
```

### Connection Pooling
```python
# Configuração otimizada
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # Conexões permanentes
    max_overflow=20,       # Conexões extras
    pool_recycle=3600,     # Reciclar após 1h
    pool_pre_ping=True     # Verificar conexão
)
```

## 🔒 Segurança

### Configurações Recomendadas
```bash
# Variáveis de ambiente seguras
export POSTGRES_PASSWORD=$(openssl rand -base64 32)

# SSL em produção
DATABASE_URL="postgresql://user:pass@host:port/db?sslmode=require"

# Backup criptografado
pg_dump collapp_db | gpg --cipher-algo AES256 --compress-algo 1 --symmetric > backup.sql.gpg
```

### Roles e Permissões
```sql
-- Role apenas para leitura
CREATE ROLE readonly_user WITH LOGIN PASSWORD 'readonly_pass';
GRANT CONNECT ON DATABASE collapp_db TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

-- Role para aplicação
CREATE ROLE app_user WITH LOGIN PASSWORD 'app_pass';
GRANT CONNECT ON DATABASE collapp_db TO app_user;
GRANT USAGE, CREATE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
```

## 🌍 Multi-Ambiente

### Desenvolvimento
```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql://collapp_user:collapp_pass@localhost:5432/collapp_db
```

### Staging
```env
ENVIRONMENT=staging
DEBUG=false
DATABASE_URL=postgresql://collapp_user:secure_pass@staging-db:5432/collapp_staging
```

### Produção
```env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://collapp_user:very_secure_pass@prod-db:5432/collapp_prod?sslmode=require
```

## 🔍 Monitoramento

### Queries Úteis
```sql
-- Conexões ativas
SELECT * FROM pg_stat_activity WHERE state = 'active';

-- Tamanho das tabelas
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Índices não utilizados
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats WHERE schemaname = 'public';
```

### Logs
```bash
# Ver logs do PostgreSQL
docker-compose logs -f postgres

# Logs com timestamp
docker-compose logs -f --timestamps postgres
```

## 🚨 Troubleshooting

### Problemas Comuns
```bash
# Erro de conexão
docker-compose restart postgres

# Limpar volumes (CUIDADO!)
docker-compose down -v

# Verificar portas
netstat -tulpn | grep 5432

# Resetar senha
docker exec -it collapp_postgres psql -U postgres -c "ALTER USER collapp_user PASSWORD 'new_password';"
```

### Performance Issues
```sql
-- Analisar queries lentas
SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

-- Recriar estatísticas
ANALYZE;

-- Vacuum completo
VACUUM FULL;
```