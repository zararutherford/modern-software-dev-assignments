# Refactored for TODO 3: Well-defined API contracts and better error handling
from __future__ import annotations

from typing import Optional
import logging
import sqlite3

from fastapi import APIRouter, HTTPException, Query

from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm
from ..schemas import (
    ExtractRequest,
    ExtractResponse,
    ActionItemResponse,
    MarkDoneRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(request: ExtractRequest) -> ExtractResponse:
    """
    Extract action items from text using heuristic-based approach.

    Args:
        request: ExtractRequest containing text and save_note flag

    Returns:
        ExtractResponse with note_id (if saved) and extracted action items

    Raises:
        HTTPException: If extraction or database operation fails
    """
    try:
        note_id: Optional[int] = None
        if request.save_note:
            note_id = db.insert_note(request.text)

        items = extract_action_items(request.text)
        ids = db.insert_action_items(items, note_id=note_id)

        action_items = [
            ActionItemResponse(
                id=item_id,
                text=text,
                note_id=note_id,
                done=False,
                created_at=""  # Will be set by database
            )
            for item_id, text in zip(ids, items)
        ]

        return ExtractResponse(note_id=note_id, items=action_items)
    except sqlite3.Error as e:
        logger.error(f"Database error during extraction: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Generated code for TODO 4: LLM extraction endpoint
@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(request: ExtractRequest) -> ExtractResponse:
    """
    Extract action items from text using LLM-powered approach via Ollama.

    Args:
        request: ExtractRequest containing text and save_note flag

    Returns:
        ExtractResponse with note_id (if saved) and extracted action items

    Raises:
        HTTPException: If extraction or database operation fails
    """
    try:
        note_id: Optional[int] = None
        if request.save_note:
            note_id = db.insert_note(request.text)

        items = extract_action_items_llm(request.text)
        ids = db.insert_action_items(items, note_id=note_id)

        action_items = [
            ActionItemResponse(
                id=item_id,
                text=text,
                note_id=note_id,
                done=False,
                created_at=""  # Will be set by database
            )
            for item_id, text in zip(ids, items)
        ]

        return ExtractResponse(note_id=note_id, items=action_items)
    except sqlite3.Error as e:
        logger.error(f"Database error during LLM extraction: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error during LLM extraction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("", response_model=list[ActionItemResponse])
def list_all(note_id: Optional[int] = Query(None, description="Filter by note ID")) -> list[ActionItemResponse]:
    """
    List all action items, optionally filtered by note ID.

    Args:
        note_id: Optional note ID to filter by

    Returns:
        List of action items

    Raises:
        HTTPException: If database query fails
    """
    try:
        rows = db.list_action_items(note_id=note_id)
        return [
            ActionItemResponse(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=bool(r["done"]),
                created_at=r["created_at"],
            )
            for r in rows
        ]
    except sqlite3.Error as e:
        logger.error(f"Database error listing action items: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, request: MarkDoneRequest) -> dict:
    """
    Mark an action item as done or undone.

    Args:
        action_item_id: The action item ID
        request: MarkDoneRequest containing done status

    Returns:
        Updated action item status

    Raises:
        HTTPException: If update fails
    """
    try:
        db.mark_action_item_done(action_item_id, request.done)
        return {"id": action_item_id, "done": request.done}
    except sqlite3.Error as e:
        logger.error(f"Database error marking item done: {e}")
        raise HTTPException(status_code=500, detail="Database error")


