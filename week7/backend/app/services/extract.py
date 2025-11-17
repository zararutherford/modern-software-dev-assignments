import re


def extract_action_items(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    results: list[str] = []

    for line in lines:
        # Strip common list markers
        cleaned_line = re.sub(r'^[-*•]\s*', '', line)
        cleaned_line = re.sub(r'^\d+\.\s*', '', cleaned_line)
        normalized = cleaned_line.lower()

        # Pattern 1: TODO: or ACTION:
        if normalized.startswith("todo:") or normalized.startswith("action:"):
            results.append(cleaned_line)
        # Pattern 2: Ends with exclamation mark
        elif cleaned_line.endswith("!"):
            results.append(cleaned_line)
        # Pattern 3: Checkbox patterns ([ ], [x], [X])
        elif re.match(r'^\[[ xX]\]', cleaned_line):
            results.append(cleaned_line)
        # Pattern 4: Priority markers (HIGH:, P0:, etc.)
        elif re.match(r'^(high|medium|low|p[0-3]):', normalized):
            results.append(cleaned_line)
        # Pattern 5: Contains @mention (assignment pattern)
        elif '@' in cleaned_line and re.search(r'@\w+', cleaned_line):
            results.append(cleaned_line)
        # Pattern 6: Contains due date patterns
        elif re.search(r'\b(by|due|deadline)\s+\d', normalized):
            results.append(cleaned_line)

    return results


