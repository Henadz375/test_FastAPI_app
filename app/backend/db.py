from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_async_engine('postgresql+asyncpg://ecommerce:221901@localhost:5432/ecommerce', echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass




# engine = create_engine('sqlite:////Users/Worker/PycharmProjects/fastapi_ecommerce/ecommerce.db', echo=True)
#
# SessionLocal = sessionmaker(bind=engine)
