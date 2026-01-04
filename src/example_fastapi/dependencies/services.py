from .db_session import DbSession, get_db
from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from example_fastapi.services.note_service import NoteService
from example_fastapi.services.user_service import UserService

async def get_users_service(
        session: DbSession
    ):
    return UserService(session=session)

async def get_notes_services(
        session: DbSession 
    ):
    return NoteService(session=session)

async def get_users_service_faststream(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session=session)