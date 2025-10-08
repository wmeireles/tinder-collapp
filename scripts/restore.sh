#!/bin/bash
# Restore script para PostgreSQL

set -e

# Verificar se arquivo de backup foi fornecido
if [ -z "$1" ]; then
    echo "❌ Usage: $0 <backup_file.sql.gz>"
    echo "Available backups:"
    ls -la ./backups/*.sql.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE=$1
DB_NAME=${POSTGRES_DB:-collapp_db}
DB_USER=${POSTGRES_USER:-collapp_user}
DB_HOST=${POSTGRES_HOST:-localhost}
DB_PORT=${POSTGRES_PORT:-5432}

# Verificar se arquivo existe
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "🔄 Starting restore from: $BACKUP_FILE"

# Descomprimir se necessário
if [[ $BACKUP_FILE == *.gz ]]; then
    echo "📦 Decompressing backup..."
    gunzip -c $BACKUP_FILE > temp_restore.sql
    RESTORE_FILE="temp_restore.sql"
else
    RESTORE_FILE=$BACKUP_FILE
fi

# Confirmar restore
read -p "⚠️  This will overwrite database '$DB_NAME'. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Restore cancelled"
    [ -f "temp_restore.sql" ] && rm temp_restore.sql
    exit 1
fi

# Executar restore
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $RESTORE_FILE

# Limpar arquivo temporário
[ -f "temp_restore.sql" ] && rm temp_restore.sql

echo "✅ Database restored successfully!"

# Restore via Docker (alternativo)
# docker exec -i collapp_postgres psql -U $DB_USER -d $DB_NAME < $RESTORE_FILE