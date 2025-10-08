# Collapp Backend - Módulo de Autenticação

Backend completo em Python (FastAPI) para o módulo de autenticação do projeto Collapp.

## Funcionalidades

### Autenticação
- ✅ Cadastro de usuário com validação de email e senha
- ✅ Login com JWT (access_token e refresh_token)
- ✅ Endpoints protegidos por Bearer Token
- ✅ Criptografia de senha com bcrypt

### Módulos de IA
- ✅ **Cálculo de Match**: IA que analisa compatibilidade entre creators (0-100%)
- ✅ **Sugestão de Collab**: Geração automática de ideias de colaboração
- ✅ **Media Kit**: Criação automática de media kits profissionais
- ✅ Integração com OpenAI GPT-3.5-turbo
- ✅ Templates personalizáveis para prompts

### Infraestrutura
- ✅ Banco PostgreSQL com SQLAlchemy + Alembic
- ✅ Testes unitários com pytest
- ✅ Docker Compose para desenvolvimento

## Estrutura do Projeto

```
collapp-backend/
├── app/
│   ├── auth/           # Módulo de autenticação
│   ├── ai/             # Módulos de IA (Match, Collab, Media Kit)
│   │   └── templates/  # Templates de prompts para IA
│   ├── core/           # Configurações e segurança
│   ├── db/             # Banco de dados e modelos
│   └── main.py         # Aplicação FastAPI
├── tests/              # Testes unitários
├── examples/           # Exemplos de uso da API
├── alembic/            # Migrações do banco
├── docker-compose.yml  # Configuração Docker
└── requirements.txt    # Dependências
```

## Como Executar

### 1. Com Docker Compose (Recomendado)

```bash
cd collapp-backend
docker-compose up --build
```

### 2. Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env

# Executar migrações
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

## Endpoints da API

### Autenticação

- `POST /auth/register` - Cadastro de usuário
- `POST /auth/login` - Login (retorna tokens JWT)
- `GET /auth/me` - Dados do usuário autenticado (protegido)

### IA para Creators

- `POST /ai/match` - Calcula compatibilidade entre dois creators (0-100%)
- `POST /ai/collab-suggestion` - Gera sugestão de colaboração criativa
- `POST /ai/media-kit` - Cria media kit profissional automaticamente

### Saúde da API

- `GET /` - Status da API
- `GET /health` - Health check

## Executar Testes

```bash
pytest
```

## Testar Módulos de IA

```bash
# Executar exemplo de uso
python examples/ai_usage.py
```

## Variáveis de Ambiente

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
OPENAI_API_KEY=your-openai-api-key
```

## Segurança Implementada

- Senhas criptografadas com bcrypt
- JWT com expiração configurável
- Validação de entrada com Pydantic
- Proteção contra SQL injection (SQLAlchemy ORM)
- Logging de eventos de segurança
- CORS configurado

A API estará disponível em `http://localhost:8000` com documentação automática em `/docs`.