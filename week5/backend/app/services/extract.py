import re
from collections.abc import Iterable

CHECKBOX_RE = re.compile(r"^-\s*\[\s*\]\s*(.+)$", re.IGNORECASE)
HASHTAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_\-]+)")


def _iter_lines(text: str) -> Iterable[str]:
    for raw in text.splitlines():
        line = raw.strip()
        if line:
            yield line


def extract_action_items(text: str) -> list[str]:
    items: list[str] = []
    for line in _iter_lines(text):
        # Checkbox-style task
        m = CHECKBOX_RE.match(line)
        if m:
            items.append(m.group(1).strip())
            continue
        # Normalize common bullet prefixes
        normalized = line.lstrip("-*0123456789. ").strip()
        if normalized.endswith("!") or normalized.lower().startswith("todo:"):
            cleaned = normalized
            if cleaned.lower().startswith("todo:"):
                cleaned = cleaned[len("todo:") :].strip()
            items.append(cleaned)
    # Deduplicate while preserving order
    seen = set()
    unique: list[str] = []
    for it in items:
        key = it.lower()
        if key not in seen:
            seen.add(key)
            unique.append(it)
    return unique


def extract_hashtags(text: str) -> list[str]:
    tags = [m.group(1).lower() for m in HASHTAG_RE.finditer(text)]
    # Deduplicate
    return list(dict.fromkeys(tags).keys())
