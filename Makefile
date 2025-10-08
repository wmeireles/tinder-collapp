# Makefile para Collapp Backend

.PHONY: help db-up db-down db-reset db-backup db-restore seed migrate health

# Variáveis
DOCKER_COMPOSE = docker-compose
PYTHON = python
ALEMBIC = alembic

help: ## Mostrar ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Database
db-up: ## Iniciar PostgreSQL
	$(DOCKER_COMPOSE) up -d postgres
	@echo "✅ PostgreSQL iniciado"

db-down: ## Parar PostgreSQL
	$(DOCKER_COMPOSE) down
	@echo "✅ PostgreSQL parado"

db-reset: ## Resetar banco (CUIDADO!)
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) up -d postgres
	sleep 10
	$(MAKE) migrate
	@echo "✅ Banco resetado"

db-logs: ## Ver logs do PostgreSQL
	$(DOCKER_COMPOSE) logs -f postgres

db-shell: ## Conectar ao PostgreSQL
	$(DOCKER_COMPOSE) exec postgres psql -U collapp_user -d collapp_db

# Migrações
migrate: ## Aplicar migrações
	$(ALEMBIC) upgrade head
	@echo "✅ Migrações aplicadas"

migrate-create: ## Criar nova migração
	@read -p "Nome da migração: " name; \
	$(ALEMBIC) revision --autogenerate -m "$$name"

migrate-history: ## Ver histórico de migrações
	$(ALEMBIC) history

migrate-current: ## Ver migração atual
	$(ALEMBIC) current

# Dados
seed: ## Executar seed de dados
	$(PYTHON) scripts/seed_data.py
	@echo "✅ Dados de teste criados"

# Backup/Restore
db-backup: ## Fazer backup
	./scripts/backup.sh
	@echo "✅ Backup realizado"

db-restore: ## Restaurar backup
	@echo "Uso: make db-restore FILE=backup.sql.gz"
	@if [ -n "$(FILE)" ]; then ./scripts/restore.sh $(FILE); fi

# Health
health: ## Verificar saúde da aplicação
	curl -s http://localhost:8000/health/ | jq .

health-db: ## Verificar saúde do banco
	curl -s http://localhost:8000/health/db | jq .

# Desenvolvimento
dev: ## Iniciar ambiente de desenvolvimento
	$(MAKE) db-up
	sleep 5
	$(MAKE) migrate
	$(MAKE) seed
	@echo "🚀 Ambiente de desenvolvimento pronto!"

install: ## Instalar dependências
	pip install -r requirements.txt
	@echo "✅ Dependências instaladas"

test: ## Executar testes
	pytest
	@echo "✅ Testes executados"

clean: ## Limpar arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "✅ Arquivos temporários removidos"