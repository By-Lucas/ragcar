from decouple import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = config(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:123@localhost:5432/test_db",
)

# Cria engine assíncrono
engine = create_async_engine(DATABASE_URL, echo=False)

# Cria sessionmaker para sessões assíncronas
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
