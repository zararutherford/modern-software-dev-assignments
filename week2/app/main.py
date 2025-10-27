# Refactored for TODO 3: Improved app lifecycle/configuration and error handling
from __future__ import annotations

from pathlib import Path
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routers import action_items, notes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up Action Item Extractor...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Action Item Extractor...")


app = FastAPI(
    title="Action Item Extractor",
    description="Extract action items from free-form notes using heuristics or LLMs",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """
    Serve the frontend HTML page.

    Returns:
        The HTML content of the index page

    Raises:
        HTTPException: If the HTML file cannot be read
    """
    try:
        html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error("Frontend HTML file not found")
        raise HTTPException(status_code=500, detail="Frontend file not found")
    except Exception as e:
        logger.error(f"Error reading frontend file: {e}")
        raise HTTPException(status_code=500, detail="Error loading frontend")


# Include routers
app.include_router(notes.router)
app.include_router(action_items.router)


# Mount static files
static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")