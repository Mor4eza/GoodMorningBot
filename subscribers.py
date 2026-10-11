import json
from pathlib import Path

SUBSCRIBERS_FILE = Path(__file__).resolve().parent / "subscribers.json"


def load_subscribers() -> list[int]:
    """Return the list of subscribed chat ids (sorted, unique)."""
    if not SUBSCRIBERS_FILE.exists():
        return []
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    ids = []
    for value in data:
        try:
            ids.append(int(value))
        except (TypeError, ValueError):
            continue
    return sorted(set(ids))


def save_subscribers(ids) -> list[int]:
    unique = sorted({int(i) for i in ids})
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2)
    return unique


def add_subscriber(chat_id: int) -> bool:
    """Add a chat id. Returns True if it was newly added."""
    ids = load_subscribers()
    if int(chat_id) in ids:
        return False
    ids.append(int(chat_id))
    save_subscribers(ids)
    return True


def remove_subscriber(chat_id: int) -> bool:
    """Remove a chat id. Returns True if it existed."""
    ids = load_subscribers()
    if int(chat_id) not in ids:
        return False
    ids = [i for i in ids if i != int(chat_id)]
    save_subscribers(ids)
    return True
