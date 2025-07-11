from typing import Any
import json
import os

MEMORY_FILE = "memory.json"


def load_memory() -> dict[str, Any]:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        empty: dict[str, Any] = {}
        save_memory(empty)  # <-- Crea el archivo vacío
        return empty


def save_memory(data: dict[str, Any]) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
