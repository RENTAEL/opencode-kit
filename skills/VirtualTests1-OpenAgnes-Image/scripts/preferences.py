import json
import os
from datetime import datetime

PREFS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_prefs.json")

TRACKED_KEYS = ["style", "color_tone", "composition", "lighting", "mood", "ratio", "size"]


def _load():
    if os.path.isfile(PREFS_FILE):
        with open(PREFS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save(data):
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_preference(user_id, key, default=None):
    data = _load()
    return data.get(user_id, {}).get(key, default)


def set_preference(user_id, key, value):
    data = _load()
    data.setdefault(user_id, {})
    data[user_id][key] = value
    data[user_id]["last_updated"] = datetime.now().isoformat()
    _save(data)


def record_choice(user_id, **params):
    data = _load()
    data.setdefault(user_id, {})
    changed = []
    for k, v in params.items():
        if k in TRACKED_KEYS and v:
            data[user_id][k] = v
            changed.append(k)
    data[user_id]["last_updated"] = datetime.now().isoformat()
    if changed:
        _save(data)
    return changed


def suggest_defaults(user_id):
    data = _load().get(user_id, {})
    return {k: data.get(k) for k in TRACKED_KEYS if data.get(k)}


def clear_preferences(user_id):
    data = _load()
    if user_id in data:
        del data[user_id]
        _save(data)
        return True
    return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage:")
        print("  python preferences.py record <user_id> [key=value ...]")
        print("  python preferences.py get <user_id>")
        print("  python preferences.py clear <user_id>")
        sys.exit(1)

    action = sys.argv[1]
    user_id = sys.argv[2]

    if action == "record":
        kwargs = {}
        for arg in sys.argv[3:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                kwargs[k.strip()] = v.strip()
        changed = record_choice(user_id, **kwargs)
        print(json.dumps({"status": "ok", "changed": changed, "user": user_id}, ensure_ascii=False))

    elif action == "get":
        prefs = suggest_defaults(user_id)
        print(json.dumps(prefs, ensure_ascii=False))

    elif action == "clear":
        ok = clear_preferences(user_id)
        print(json.dumps({"status": "ok" if ok else "not_found", "user": user_id}))

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
