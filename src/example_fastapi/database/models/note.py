from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Note(Base):

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text())

    #relationships
    user: Mapped["User"] = relationship(back_populates="notes")
