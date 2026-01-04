from uuid import UUID
from pydantic import BaseModel

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    user_id: UUID

class NoteUpdate(BaseModel):
    content: str | None = None

class NoteRead(NoteBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True