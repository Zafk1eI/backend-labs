from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    firstname: str | None = None
    lastname: str | None = None

class UserRead(UserBase):
    id: UUID

    class Config:
        from_attributes = True
