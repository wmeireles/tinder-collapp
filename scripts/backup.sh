#!/bin/bash
# Backup script para PostgreSQL

set -e

# Configurações
DB_NAME=${POSTGRES_DB:-collapp_db}
DB_USER=${POSTGRES_USER:-collapp_user}
DB_HOST=${POSTGRES_HOST:-localhost}
DB_PORT=${POSTGRES_PORT:-5432}
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql"

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

echo "🗄️  Starting backup of database: $DB_NAME"

# Backup completo
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME \
    --verbose --clean --no-owner --no-privileges \
    --file=$BACKUP_FILE

# Comprimir backup
gzip $BACKUP_FILE

echo "✅ Backup completed: ${BACKUP_FILE}.gz"

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "${DB_NAME}_*.sql.gz" -mtime +7 -delete

echo "🧹 Old backups cleaned up"

# Backup via Docker (alternativo)
# docker exec collapp_postgres pg_dump -U $DB_USER -d $DB_NAME > $BACKUP_FILE