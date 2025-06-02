from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db import async_session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# from app.backend.db import SessionLocal
#
#
# async def get_session():
#     db_session=SessionLocal()
#     try:
#         yield db_session
#     finally:
#         db_session.close()