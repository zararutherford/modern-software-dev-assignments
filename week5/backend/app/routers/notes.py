
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note, Tag
from ..schemas import (
    ExtractionResult,
    NoteCreate,
    NoteRead,
    NotesSearchResponse,
    NotesSort,
)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(db: Session = Depends(get_db)) -> list[NoteRead]:
    rows = db.execute(select(Note)).scalars().all()
    return [
        NoteRead.model_validate(
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "tags": [t.name for t in getattr(n, "tags", [])],
            }
        )
        for n in rows
    ]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": [t.name for t in getattr(note, "tags", [])],
        }
    )


@router.get("/search/", response_model=NotesSearchResponse)
def search_notes(
    q: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort: NotesSort = NotesSort.created_desc,
    db: Session = Depends(get_db),
) -> NotesSearchResponse:
    query = select(Note)
    if q:
        like = f"%{q}%"
        query = query.where(
            func.lower(Note.title).like(func.lower(like))
            | func.lower(Note.content).like(func.lower(like))
        )

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar_one()

    if sort == NotesSort.title_asc:
        query = query.order_by(Note.title.asc())
    else:
        query = query.order_by(Note.created_at.desc())

    rows = db.execute(query.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    items = [
        NoteRead.model_validate(
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "tags": [t.name for t in getattr(n, "tags", [])],
            }
        )
        for n in rows
    ]
    return NotesSearchResponse(items=items, total=total, page=page, page_size=page_size)


@router.post("/{note_id}/extract", response_model=ExtractionResult)
def extract_from_note(
    note_id: int,
    apply: bool = False,
    db: Session = Depends(get_db),
) -> ExtractionResult:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    from ..services.extract import extract_action_items, extract_hashtags

    tags = extract_hashtags(note.content)
    action_items = extract_action_items(note.content)

    if apply:
        # Upsert tags and attach
        existing = {
            t.name: t for t in db.execute(select(Tag).where(Tag.name.in_(tags))).scalars().all()
        }
        attached = []
        for name in tags:
            tag = existing.get(name)
            if not tag:
                tag = Tag(name=name)
                db.add(tag)
                db.flush()
            attached.append(tag)
        for tag in attached:
            if tag not in note.tags:
                note.tags.append(tag)
        # Create action items
        for desc in action_items:
            db.add(ActionItem(description=desc, completed=False))
        db.flush()
        db.refresh(note)

    return ExtractionResult(tags=tags, action_items=action_items, applied=apply)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": [t.name for t in getattr(note, "tags", [])],
        }
    )
