from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from example_fastapi.database.models.note import Note
from example_fastapi.schemas.note import NoteCreate, NoteUpdate
import logging

logger = logging.getLogger(__name__)

class NoteService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_notes(self) -> list[Note]:
        logger.info("Getting all notes")
        stmt = select(Note)
        result = await self.session.execute(stmt)
        notes = list(result.scalars().all())
        logger.info("Retrieved %s notes.", len(notes))
        return notes

    async def create_note(self, note_data: NoteCreate) -> Note:
        logger.info("Creating note with data: %r", note_data)
        note = Note(id=uuid4(), **note_data.model_dump())
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)
        logger.info("Note created with id: %s", note.id)
        return note

    async def get_note_by_id(self, note_id: UUID) -> Note | None:
        logger.info("Getting note by id: %s", note_id)
        stmt = select(Note).where(Note.id == note_id)
        result = await self.session.execute(stmt)
        note = result.scalar_one_or_none()
        if note:
            logger.info("Note with id: %s found.", note_id)
        else:
            logger.warning("Note with id: %s not found.", note_id)
        return note

    async def update_note(self, note_id: UUID, note_data: NoteUpdate) -> Note | None:
        logger.info("Updating note with id: %s", note_id)
        note = await self.get_note_by_id(note_id)
        if note is None:
            logger.warning("Note with id: %s not found for update.", note_id)
            return None
        
        for key, value in note_data.model_dump(exclude_unset=True).items():
            setattr(note, key, value)
        
        await self.session.commit()
        await self.session.refresh(note)
        logger.info("Note with id: %s updated successfully.", note_id)
        return note

    async def delete_note(self, note_id: UUID) -> Note | None:
        logger.info("Deleting note with id: %s", note_id)
        note = await self.get_note_by_id(note_id)
        if note is None:
            logger.warning("Note with id: %s not found for deletion.", note_id)
            return None
        
        await self.session.delete(note)
        await self.session.commit()
        logger.info("Note with id: %s deleted successfully.", note_id)
        return note