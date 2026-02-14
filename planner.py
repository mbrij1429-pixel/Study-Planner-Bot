"""
Study planner logic: subjects, goals, and schedule generation.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Subject:
    name: str
    hours_per_week: float = 0.0
    priority: int = 1  # 1 = high, 2 = medium, 3 = low
    deadline: Optional[str] = None


@dataclass
class StudyPlan:
    subjects: list[Subject] = field(default_factory=list)

    def add_subject(self, name: str, hours: float = 0, priority: int = 1, deadline: str | None = None) -> str:
        self.subjects.append(
            Subject(name=name, hours_per_week=hours, priority=priority, deadline=deadline)
        )
        return f"Added subject: **{name}** (target: {hours}h/week, priority: {priority})"

    def list_subjects(self) -> str:
        if not self.subjects:
            return "No subjects added yet. Say something like: *Add Math with 5 hours per week*"
        lines = ["**Your subjects:**"]
        for i, s in enumerate(self.subjects, 1):
            deadline = f", deadline: {s.deadline}" if s.deadline else ""
            lines.append(f"{i}. **{s.name}** — {s.hours_per_week}h/week, priority {s.priority}{deadline}")
        return "\n".join(lines)

    def suggest_daily_schedule(self, study_hours_per_day: float = 4.0) -> str:
        if not self.subjects:
            return "Add some subjects first, then I can suggest a daily schedule."
        total = sum(s.hours_per_week for s in self.subjects)
        if total <= 0:
            total = len(self.subjects) * 2  # default 2h each
        # Sort by priority, then distribute hours
        sorted_subs = sorted(self.subjects, key=lambda x: (x.priority, -x.hours_per_week))
        daily_hours = study_hours_per_day
        lines = [f"**Suggested daily schedule** ({daily_hours}h total):"]
        for s in sorted_subs:
            ratio = (s.hours_per_week or 1) / max(total, 1)
            mins = int(daily_hours * 60 * ratio)
            if mins < 15:
                mins = 15
            lines.append(f"• **{s.name}**: {mins} min")
        return "\n".join(lines)

    def clear(self) -> str:
        self.subjects.clear()
        return "All subjects cleared. You can add new ones anytime."


def parse_add_command(text: str) -> dict | None:
    """Parse messages like 'add Math 5 hours', 'add Linear Algebra 4', or 'add Physics'."""
    t = text.strip().lower()
    if not t.startswith("add "):
        if " add " in t:
            rest = text.strip().split(" add ", 1)[-1].strip()
        else:
            return None
    else:
        rest = text.strip()[4:].strip()
    rest = rest.replace("subject", "").replace("topic", "").strip()
    if not rest:
        return None
    parts = rest.split()
    name_parts = []
    hours = 0.0
    for i, p in enumerate(parts):
        try:
            hours = float(p)
            break
        except ValueError:
            name_parts.append(p)
    name = " ".join(name_parts) if name_parts else (parts[0] if parts else "")
    if not name:
        return None
    if hours == 0:
        hours = 2.0
    return {"name": name.strip(), "hours": hours}


def get_greeting() -> str:
    return (
        "Hi! I'm your **Study Planner Bot**. I can help you:\n"
        "• **Add subjects** — e.g. *Add Math 5 hours* or *Add Physics*\n"
        "• **List subjects** — say *list subjects* or *show my subjects*\n"
        "• **Get a daily schedule** — say *schedule* or *daily plan*\n"
        "• **Clear subjects** — say *clear* to start over\n\n"
        "What would you like to do?"
    )
