from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(primary_key=True)

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
