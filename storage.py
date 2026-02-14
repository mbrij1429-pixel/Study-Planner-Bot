"""
Persistence layer for Ultimate AI Study Planner Bot.
Saves/loads plan, user stats, and behavior log to a single JSON file.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Data file in project root (create .gitignore entry study_plan_data.json to avoid committing)
DATA_DIR = Path(__file__).resolve().parent
DATA_FILE = DATA_DIR / "study_plan_data.json"


def load_raw() -> dict[str, Any]:
    """Load raw JSON data. Returns empty dict if file missing or invalid."""
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_raw(data: dict[str, Any]) -> None:
    """Write raw JSON data to disk."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_plan_data() -> dict[str, Any]:
    """Load plan-related data: subjects, tasks, exams."""
    raw = load_raw()
    return {
        "subjects": raw.get("subjects", []),
        "tasks": raw.get("tasks", []),
        "exams": raw.get("exams", []),
    }


def save_plan_data(subjects: list[dict], tasks: list[dict], exams: list[dict]) -> None:
    """Persist subjects, tasks, exams."""
    raw = load_raw()
    raw["subjects"] = subjects
    raw["tasks"] = tasks
    raw["exams"] = exams
    save_raw(raw)


def load_user_stats() -> dict[str, Any]:
    """Load user stats: points, level, streak, last_completion_date."""
    raw = load_raw()
    return raw.get("user_stats", {})


def save_user_stats(stats: dict[str, Any]) -> None:
    """Persist user stats without overwriting plan data."""
    raw = load_raw()
    raw["user_stats"] = stats
    save_raw(raw)


def load_behavior_log() -> list[dict[str, Any]]:
    """Load completion/skip history for adaptation."""
    raw = load_raw()
    return raw.get("behavior_log", [])


def save_behavior_log(log: list[dict[str, Any]]) -> None:
    """Persist behavior log. Keeps last N entries to avoid huge files."""
    MAX_ENTRIES = 500
    raw = load_raw()
    raw["behavior_log"] = log[-MAX_ENTRIES:]
    save_raw(raw)


def save_all(
    subjects: list[dict],
    tasks: list[dict],
    exams: list[dict],
    user_stats: dict[str, Any],
    behavior_log: list[dict],
) -> None:
    """Persist full state in one write."""
    save_raw({
        "subjects": subjects,
        "tasks": tasks,
        "exams": exams,
        "user_stats": user_stats,
        "behavior_log": behavior_log,
    })
