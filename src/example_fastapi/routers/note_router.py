from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from example_fastapi.dependencies.services import get_notes_services
from example_fastapi.schemas.note import NoteCreate, NoteRead, NoteUpdate
from example_fastapi.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=list[NoteRead])
async def get_notes(
    note_service: NoteService = Depends(get_notes_services),
):
    return await note_service.get_notes()


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    note_service: NoteService = Depends(get_notes_services),
):
    return await note_service.create_note(note_data)


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(
    note_id: UUID,
    note_service: NoteService = Depends(get_notes_services),
):
    note = await note_service.get_note_by_id(note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return note


@router.put("/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: UUID,
    note_data: NoteUpdate,
    note_service: NoteService = Depends(get_notes_services),
):
    note = await note_service.update_note(note_id, note_data)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: UUID,
    note_service: NoteService = Depends(get_notes_services),
):
    note = await note_service.delete_note(note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)