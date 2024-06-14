from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config

engine = AsyncEngine(
    create_engine(
        url = Config.DATABASE_URL,
        echo = True
    )
)

async def init_db():
    async with engine.begin() as conn:
        stat = text("SELECT 'start';")
        res = await conn.execute(stat)
        print(res.all())
        
async def get_session() -> AsyncSession:
    
    Session = sessionmaker(
        bind = engine,
        class_= AsyncSession,
        expire_on_commit = False 
    )
    
    async with Session() as session:
        yield session