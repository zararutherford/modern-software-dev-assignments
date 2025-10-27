# Refactored for TODO 3: Well-defined API contracts and better error handling
from __future__ import annotations

import logging
import sqlite3

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreateRequest, NoteResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse)
def create_note(request: NoteCreateRequest) -> NoteResponse:
    """
    Create a new note.

    Args:
        request: NoteCreateRequest containing note content

    Returns:
        The created note

    Raises:
        HTTPException: If creation fails
    """
    try:
        note_id = db.insert_note(request.content)
        note = db.get_note(note_id)
        if note is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve created note")
        return NoteResponse(
            id=note["id"],
            content=note["content"],
            created_at=note["created_at"],
        )
    except sqlite3.Error as e:
        logger.error(f"Database error creating note: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """
    Get a single note by ID.

    Args:
        note_id: The note ID

    Returns:
        The requested note

    Raises:
        HTTPException: If note not found or query fails
    """
    try:
        row = db.get_note(note_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return NoteResponse(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"],
        )
    except sqlite3.Error as e:
        logger.error(f"Database error getting note: {e}")
        raise HTTPException(status_code=500, detail="Database error")


# Generated code for TODO 4: List all notes endpoint
@router.get("", response_model=list[NoteResponse])
def list_notes() -> list[NoteResponse]:
    """
    List all notes.

    Returns:
        List of all notes

    Raises:
        HTTPException: If query fails
    """
    try:
        rows = db.list_notes()
        return [
            NoteResponse(
                id=row["id"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
    except sqlite3.Error as e:
        logger.error(f"Database error listing notes: {e}")
        raise HTTPException(status_code=500, detail="Database error")


