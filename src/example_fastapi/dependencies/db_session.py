from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from example_fastapi.database.db_connection import SessionMaker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionMaker() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


DbSession = Annotated[AsyncSession, Depends(get_db)]
