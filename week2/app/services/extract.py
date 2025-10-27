from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


# ========== LLM-POWERED EXTRACTION ==========
# Generated code for TODO 1: Scaffold a New Feature
# This section implements LLM-powered action item extraction using Ollama

class ActionItems(BaseModel):
    """Pydantic model for structured output from Ollama"""
    items: List[str]


def extract_action_items_llm(text: str, model: str = "llama3.2") -> List[str]:
    """
    Extract action items from text using an LLM via Ollama.

    Args:
        text: The input text containing potential action items
        model: The Ollama model to use (default: llama3.2, a smaller/faster model)

    Returns:
        A list of extracted action item strings
    """
    if not text.strip():
        return []

    # Define the prompt for the LLM
    prompt = f"""You are an assistant that extracts action items from notes.
Given the following text, identify all actionable tasks and return them as a JSON array of strings.
Each action item should be concise and in imperative form (e.g., "Set up database", "Write tests").

Text:
{text}

Extract all action items from the text above. If there are no clear action items, return an empty list."""

    try:
        # Use Ollama chat API with structured output (Pydantic model)
        response = chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            format=ActionItems.model_json_schema()
        )

        # Parse the response message content
        result = ActionItems.model_validate_json(response.message.content)

        # Deduplicate while preserving order
        seen: set[str] = set()
        unique: List[str] = []
        for item in result.items:
            item_stripped = item.strip()
            lowered = item_stripped.lower()
            if lowered and lowered not in seen:
                seen.add(lowered)
                unique.append(item_stripped)

        return unique
    except Exception as e:
        # Fallback to heuristic extraction if LLM fails
        print(f"LLM extraction failed: {e}. Falling back to heuristic extraction.")
        return extract_action_items(text)
