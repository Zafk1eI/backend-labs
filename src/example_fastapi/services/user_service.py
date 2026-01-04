from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from example_fastapi.database.models.user import User
from example_fastapi.schemas.user import UserCreate, UserUpdate
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> list[User]:
        stmt = select(User)
        result = await self.session.execute(stmt)
        users = list(result.scalars().all())
        logger.info("Retrieved %s users.", len(users))
        return users

    async def create_user(self, user_data: UserCreate) -> User:
        logger.info("Creating user with data: %r", user_data)
        user = User(id=uuid4(), **user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info("User created with id: %s", user.id)
        return user

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        logger.info("Getting user by id: %s", user_id)
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if user:
            logger.info("User with id: %s found.", user_id)
        else:
            logger.warning("User with id: %s not found.", user_id)
        return user

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User | None:
        logger.info("Updating user with id: %s", user_id)
        user = await self.get_user_by_id(user_id)
        if user is None:
            logger.warning("User with id: %s not found for update.", user_id)
            return None
        
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        
        await self.session.commit()
        await self.session.refresh(user)
        logger.info("User with id: %s updated successfully.", user_id)
        return user

    async def delete_user(self, user_id: UUID) -> User | None:
        logger.info("Deleting user with id: %s", user_id)
        user = await self.get_user_by_id(user_id)
        if user is None:
            logger.warning("User with id: %s not found for deletion.", user_id)
            return None
        
        await self.session.delete(user)
        await self.session.commit()
        logger.info("User with id: %s deleted successfully.", user_id)
        return user