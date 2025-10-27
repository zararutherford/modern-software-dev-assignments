# Generated code for TODO 3: Refactor Existing Code for Clarity
# This file defines well-structured API contracts using Pydantic models

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ========== REQUEST SCHEMAS ==========

class ExtractRequest(BaseModel):
    """Request schema for action item extraction"""
    text: str = Field(..., min_length=1, description="Text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the note to database")


class NoteCreateRequest(BaseModel):
    """Request schema for creating a new note"""
    content: str = Field(..., min_length=1, description="Note content")


class MarkDoneRequest(BaseModel):
    """Request schema for marking action item as done/undone"""
    done: bool = Field(default=True, description="Done status")


# ========== RESPONSE SCHEMAS ==========

class ActionItemResponse(BaseModel):
    """Response schema for an action item"""
    id: int
    text: str
    note_id: Optional[int] = None
    done: bool = False
    created_at: str


class NoteResponse(BaseModel):
    """Response schema for a note"""
    id: int
    content: str
    created_at: str


class ExtractResponse(BaseModel):
    """Response schema for extraction endpoint"""
    note_id: Optional[int] = None
    items: list[ActionItemResponse]


class ActionItemListResponse(BaseModel):
    """Response schema for list of action items"""
    items: list[ActionItemResponse]


class NoteListResponse(BaseModel):
    """Response schema for list of notes"""
    notes: list[NoteResponse]
