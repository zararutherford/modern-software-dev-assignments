# Refactored for TODO 3: Database layer cleanup with better error handling
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


def ensure_data_directory_exists() -> None:
    """Ensure the data directory exists, creating it if necessary"""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create data directory: {e}")
        raise


def get_connection() -> sqlite3.Connection:
    """
    Get a database connection with proper configuration.

    Returns:
        sqlite3.Connection: A configured database connection

    Raises:
        sqlite3.Error: If connection fails
    """
    try:
        ensure_data_directory_exists()
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        # Enable foreign key constraints
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise


def init_db() -> None:
    """
    Initialize the database schema.

    Creates tables for notes and action_items if they don't exist.

    Raises:
        sqlite3.Error: If database initialization fails
    """
    try:
        ensure_data_directory_exists()
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER,
                    text TEXT NOT NULL,
                    done INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                );
                """
            )
            connection.commit()
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def insert_note(content: str) -> int:
    """
    Insert a new note into the database.

    Args:
        content: The note content

    Returns:
        The ID of the newly created note

    Raises:
        sqlite3.Error: If insertion fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            connection.commit()
            note_id = int(cursor.lastrowid)
            logger.debug(f"Created note with ID {note_id}")
            return note_id
    except sqlite3.Error as e:
        logger.error(f"Failed to insert note: {e}")
        raise


def list_notes() -> list[sqlite3.Row]:
    """
    Retrieve all notes from the database.

    Returns:
        List of note records ordered by ID descending

    Raises:
        sqlite3.Error: If query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
            return list(cursor.fetchall())
    except sqlite3.Error as e:
        logger.error(f"Failed to list notes: {e}")
        raise


def get_note(note_id: int) -> Optional[sqlite3.Row]:
    """
    Retrieve a single note by ID.

    Args:
        note_id: The note ID to retrieve

    Returns:
        The note record or None if not found

    Raises:
        sqlite3.Error: If query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            return row
    except sqlite3.Error as e:
        logger.error(f"Failed to get note {note_id}: {e}")
        raise


def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    """
    Insert multiple action items into the database.

    Args:
        items: List of action item texts
        note_id: Optional note ID to associate with the action items

    Returns:
        List of IDs for the newly created action items

    Raises:
        sqlite3.Error: If insertion fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            ids: list[int] = []
            for item in items:
                cursor.execute(
                    "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                    (note_id, item),
                )
                ids.append(int(cursor.lastrowid))
            connection.commit()
            logger.debug(f"Created {len(ids)} action items")
            return ids
    except sqlite3.Error as e:
        logger.error(f"Failed to insert action items: {e}")
        raise


def list_action_items(note_id: Optional[int] = None) -> list[sqlite3.Row]:
    """
    Retrieve action items, optionally filtered by note ID.

    Args:
        note_id: Optional note ID to filter by

    Returns:
        List of action item records ordered by ID descending

    Raises:
        sqlite3.Error: If query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            if note_id is None:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
                )
            else:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                    (note_id,),
                )
            return list(cursor.fetchall())
    except sqlite3.Error as e:
        logger.error(f"Failed to list action items: {e}")
        raise


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    """
    Mark an action item as done or undone.

    Args:
        action_item_id: The action item ID to update
        done: Whether the item is done

    Raises:
        sqlite3.Error: If update fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            connection.commit()
            logger.debug(f"Marked action item {action_item_id} as {'done' if done else 'undone'}")
    except sqlite3.Error as e:
        logger.error(f"Failed to mark action item {action_item_id} as done: {e}")
        raise


