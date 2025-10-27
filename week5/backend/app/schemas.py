from enum import Enum

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str] = []

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1)


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True


class NotesSort(str, Enum):
    created_desc = "created_desc"
    title_asc = "title_asc"


class NotesSearchResponse(BaseModel):
    items: list[NoteRead]
    total: int
    page: int
    page_size: int


class ExtractionResult(BaseModel):
    tags: list[str]
    action_items: list[str]
    applied: bool
