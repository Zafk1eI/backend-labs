from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .note import Note


class User(Base):
    email: Mapped[str] = mapped_column(String(45), unique=True)
    firstname: Mapped[str] = mapped_column(String(45))
    lastname: Mapped[str] = mapped_column(String(45))

    # relationships
    notes: Mapped[list["Note"]] = relationship(back_populates="user", cascade="all, delete-orphan")
