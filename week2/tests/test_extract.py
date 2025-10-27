import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ========== LLM EXTRACTION TESTS ==========
# Generated code for TODO 2: Add Unit Tests
# These tests cover extract_action_items_llm() with multiple input types


def test_extract_action_items_llm_with_bullets():
    """Test LLM extraction with bullet-point formatted action items"""
    text = """
    Meeting notes:
    - Set up database
    - Implement API endpoint
    - Write unit tests
    """.strip()

    items = extract_action_items_llm(text)
    assert len(items) >= 2, "Should extract multiple action items from bullet list"
    # Check that at least some expected items are present
    assert any("database" in item.lower() for item in items)
    assert any("test" in item.lower() for item in items)


def test_extract_action_items_llm_with_keyword_prefixes():
    """Test LLM extraction with keyword-prefixed lines (TODO, ACTION, etc.)"""
    text = """
    Project plan:
    TODO: Complete the documentation
    ACTION: Review pull request
    NEXT: Deploy to staging
    Some other narrative text.
    """.strip()

    items = extract_action_items_llm(text)
    assert len(items) >= 2, "Should extract action items from keyword-prefixed lines"
    assert any("documentation" in item.lower() for item in items)


def test_extract_action_items_llm_with_empty_input():
    """Test LLM extraction with empty or whitespace-only input"""
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []
    assert extract_action_items_llm("\n\n") == []


def test_extract_action_items_llm_with_narrative_text():
    """Test LLM extraction with narrative text containing implicit action items"""
    text = """
    We need to refactor the authentication module and update the API documentation.
    It would be good to add error handling to the database layer.
    """.strip()

    items = extract_action_items_llm(text)
    # LLM should identify action items even in narrative form
    assert len(items) >= 1, "Should extract action items from narrative text"


def test_extract_action_items_llm_with_mixed_formats():
    """Test LLM extraction with mixed formatting styles"""
    text = """
    Sprint tasks:
    1. Implement user login
    - [ ] Add password reset feature
    TODO: Write API tests
    We should also optimize database queries.
    """.strip()

    items = extract_action_items_llm(text)
    assert len(items) >= 3, "Should extract action items from mixed formats"
    assert any("login" in item.lower() for item in items)


def test_extract_action_items_llm_deduplication():
    """Test that LLM extraction removes duplicate action items"""
    text = """
    - Write tests
    - Write unit tests
    - Write tests
    """.strip()

    items = extract_action_items_llm(text)
    # Should deduplicate similar items
    assert len(items) <= 2, "Should deduplicate action items"
