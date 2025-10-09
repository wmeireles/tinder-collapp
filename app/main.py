from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.onboarding.router import router as onboarding_router
from app.matching.router import router as matching_router
from app.wanted.router import router as wanted_router
from app.chat.router import router as chat_router
from app.health.router import router as health_router
from app.ai.router import router as ai_router
from app.invitations.router import router as invitations_router
from app.linkinbio.router import router as linkinbio_router
from app.mediakit.router import router as mediakit_router
from app.notifications.router import router as notifications_router
from app.offers.router import router as offers_router
from app.subscriptions.router import router as subscriptions_router
from app.admin.router import router as admin_router
from app.reports.router import router as reports_router
from app.profile.router import router as profile_router
from app.core.middleware import RateLimitMiddleware, LoggingMiddleware
from app.db.database import engine
from app.db.models import Base
import logging
import sys

# Configuração mais detalhada de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Log de inicialização
logger.info("=== INICIANDO COLLAPP BACKEND ===")

# Forçar criação de tabelas em produção
try:
    Base.metadata.drop_all(bind=engine)  # Remove tabelas antigas
    Base.metadata.create_all(bind=engine)  # Cria tabelas novas
    print("✅ Tabelas criadas com sucesso!")
except Exception as e:
    print(f"⚠️ Erro ao criar tabelas: {e}")
    Base.metadata.create_all(bind=engine)  # Tenta criar mesmo assim

app = FastAPI(title="Collapp Auth API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add middleware
app.middleware("http")(RateLimitMiddleware(calls=100, period=60))
app.middleware("http")(LoggingMiddleware())

# Include routers
app.include_router(auth_router)
app.include_router(onboarding_router)
app.include_router(matching_router)
app.include_router(wanted_router)
app.include_router(chat_router)
app.include_router(health_router)
app.include_router(ai_router)
app.include_router(invitations_router)
app.include_router(linkinbio_router)
app.include_router(mediakit_router)
app.include_router(notifications_router)
app.include_router(offers_router)
app.include_router(subscriptions_router)
app.include_router(admin_router)
app.include_router(reports_router)
app.include_router(profile_router)


@app.get("/")
def read_root():
    return {"message": "Collapp Auth API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint working - no auth required", "status": "ok"}

@app.get("/make-admin/{email}")
def make_admin_endpoint(email: str):
    from sqlalchemy.orm import sessionmaker
    from app.db.models import User
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return {"error": "User not found"}
        
        user.is_admin = True
        db.commit()
        
        return {"message": f"User {user.name} is now admin!", "email": email}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()