"""
Ultimate AI Study Planner Bot — core domain logic.
Subjects, tasks, exams, points, levels, streaks, behavior log, and adaptation.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
import uuid

import storage as store

# --- Constants ---
POINTS_PER_TASK = 10
POINTS_PER_SKIP_PENALTY = -3
LEVEL_POINTS_STEP = 100  # level = 1 + total_points // 100
DEFAULT_STUDY_HOURS_PER_DAY = 4.0
MAX_STREAK_BONUS_POINTS = 5  # extra points when on streak


@dataclass
class Subject:
    name: str
    hours_per_week: float = 0.0
    priority: int = 1  # 1 = high
    deadline: Optional[str] = None
    subject_type: str = "general"  # "coding" | "college" | "general"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "hours_per_week": self.hours_per_week,
            "priority": self.priority,
            "deadline": self.deadline,
            "subject_type": self.subject_type,
        }

    @staticmethod
    def from_dict(d: dict) -> Subject:
        return Subject(
            name=d.get("name", ""),
            hours_per_week=float(d.get("hours_per_week", 0)),
            priority=int(d.get("priority", 1)),
            deadline=d.get("deadline"),
            subject_type=d.get("subject_type", "general"),
        )


@dataclass
class Task:
    id: str
    subject_name: str
    title: str
    due_date: Optional[str] = None  # YYYY-MM-DD
    done: bool = False
    skipped: bool = False
    created_at: str = ""
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "subject_name": self.subject_name,
            "title": self.title,
            "due_date": self.due_date,
            "done": self.done,
            "skipped": self.skipped,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @staticmethod
    def from_dict(d: dict) -> Task:
        return Task(
            id=d.get("id", str(uuid.uuid4())[:8]),
            subject_name=d.get("subject_name", ""),
            title=d.get("title", ""),
            due_date=d.get("due_date"),
            done=bool(d.get("done", False)),
            skipped=bool(d.get("skipped", False)),
            created_at=d.get("created_at", ""),
            completed_at=d.get("completed_at"),
        )


@dataclass
class Exam:
    id: str
    name: str
    subject_name: str
    exam_date: str  # YYYY-MM-DD
    weight: str = ""  # e.g. "mid-term", "final"
    chapters: str = ""  # e.g. "1-5"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "subject_name": self.subject_name,
            "exam_date": self.exam_date,
            "weight": self.weight,
            "chapters": self.chapters,
        }

    @staticmethod
    def from_dict(d: dict) -> Exam:
        return Exam(
            id=d.get("id", str(uuid.uuid4())[:8]),
            name=d.get("name", ""),
            subject_name=d.get("subject_name", ""),
            exam_date=d.get("exam_date", ""),
            weight=d.get("weight", ""),
            chapters=d.get("chapters", ""),
        )

    def days_left(self) -> Optional[int]:
        try:
            d = datetime.strptime(self.exam_date, "%Y-%m-%d").date()
            return (d - date.today()).days
        except (ValueError, TypeError):
            return None


@dataclass
class UserStats:
    total_points: int = 0
    current_streak: int = 0
    last_completion_date: Optional[str] = None  # YYYY-MM-DD

    def level(self) -> int:
        return max(1, 1 + self.total_points // LEVEL_POINTS_STEP)

    def to_dict(self) -> dict:
        return {
            "total_points": self.total_points,
            "current_streak": self.current_streak,
            "last_completion_date": self.last_completion_date,
        }

    @staticmethod
    def from_dict(d: dict) -> UserStats:
        return UserStats(
            total_points=int(d.get("total_points", 0)),
            current_streak=int(d.get("current_streak", 0)),
            last_completion_date=d.get("last_completion_date"),
        )


def _today_str() -> str:
    return date.today().isoformat()


def _update_streak(last_date: Optional[str], today: str) -> int:
    """Return new streak: 1 if first time today, or last_streak+1 if yesterday was last_date."""
    if not last_date:
        return 1
    try:
        last = datetime.strptime(last_date, "%Y-%m-%d").date()
        td = date.today()
        delta = (td - last).days
        if delta == 0:
            return 0  # already counted today
        if delta == 1:
            return 1  # will be set to previous_streak + 1 by caller
        return 0  # streak broken
    except (ValueError, TypeError):
        return 1


class StudyPlan:
    """Single source of truth: subjects, tasks, exams, stats, behavior. Persisted to storage."""

    def __init__(self) -> None:
        self.subjects: list[Subject] = []
        self.tasks: list[Task] = []
        self.exams: list[Exam] = []
        self.user_stats = UserStats()
        self.behavior_log: list[dict] = []
        self._load()

    def _load(self) -> None:
        plan = store.load_plan_data()
        self.subjects = [Subject.from_dict(s) for s in plan["subjects"]]
        self.tasks = [Task.from_dict(t) for t in plan["tasks"]]
        self.exams = [Exam.from_dict(e) for e in plan["exams"]]
        stats = store.load_user_stats()
        if stats:
            self.user_stats = UserStats.from_dict(stats)
        self.behavior_log = store.load_behavior_log()

    def _save(self) -> None:
        store.save_all(
            subjects=[s.to_dict() for s in self.subjects],
            tasks=[t.to_dict() for t in self.tasks],
            exams=[e.to_dict() for e in self.exams],
            user_stats=self.user_stats.to_dict(),
            behavior_log=self.behavior_log,
        )

    # --- Subjects ---
    def add_subject(
        self,
        name: str,
        hours: float = 0,
        priority: int = 1,
        deadline: str | None = None,
        subject_type: str = "general",
    ) -> str:
        self.subjects.append(
            Subject(
                name=name,
                hours_per_week=hours,
                priority=priority,
                deadline=deadline,
                subject_type=subject_type,
            )
        )
        self._save()
        return f"Added **{name}** — {hours}h/week, priority {priority}, type: {subject_type}."

    def list_subjects(self) -> str:
        if not self.subjects:
            return "No subjects. Add one: *Add Math 5 hours* or *Add DSA 6*."
        lines = ["**Your subjects:**"]
        for i, s in enumerate(self.subjects, 1):
            extra = f", deadline: {s.deadline}" if s.deadline else f", type: {s.subject_type}"
            lines.append(f"{i}. **{s.name}** — {s.hours_per_week}h/week, P{s.priority}{extra}")
        return "\n".join(lines)

    def clear_subjects(self) -> str:
        self.subjects.clear()
        self._save()
        return "All subjects cleared."

    # --- Tasks ---
    def add_task(self, subject_name: str, title: str, due_date: str | None = None) -> str:
        tid = str(uuid.uuid4())[:8]
        t = Task(
            id=tid,
            subject_name=subject_name,
            title=title,
            due_date=due_date,
            created_at=_today_str(),
        )
        self.tasks.append(t)
        self._save()
        return f"Task added: **{title}** ({subject_name}). Due: {due_date or '—'}."

    def list_tasks(self, subject_name: str | None = None, pending_only: bool = False) -> str:
        tasks = self.tasks
        if subject_name:
            tasks = [t for t in tasks if t.subject_name.lower() == subject_name.lower()]
        if pending_only:
            tasks = [t for t in tasks if not t.done and not t.skipped]
        if not tasks:
            return "No tasks." + (" Add via: *task &lt;subject&gt; &lt;title&gt;*" if not subject_name else "")
        lines = ["**Tasks:**"]
        for t in tasks:
            status = "✓" if t.done else ("⊘ skip" if t.skipped else "○")
            lines.append(f"{status} **{t.title}** — {t.subject_name}" + (f" (due {t.due_date})" if t.due_date else ""))
        return "\n".join(lines)

    def complete_task(self, task_id: str) -> str:
        for t in self.tasks:
            if t.id == task_id:
                if t.done:
                    return "Task already done."
                t.done = True
                t.completed_at = _today_str()
                today = _today_str()
                # Points and streak
                points = POINTS_PER_TASK
                if self.user_stats.last_completion_date == today:
                    pass  # no double count same day
                else:
                    streak_inc = _update_streak(self.user_stats.last_completion_date, today)
                    if streak_inc == 0 and self.user_stats.last_completion_date != today:
                        self.user_stats.current_streak = 1
                    else:
                        self.user_stats.current_streak += 1
                    self.user_stats.last_completion_date = today
                    self.user_stats.total_points += points
                    if self.user_stats.current_streak > 1:
                        self.user_stats.total_points += min(MAX_STREAK_BONUS_POINTS, self.user_stats.current_streak - 1)
                self.behavior_log.append({
                    "date": today,
                    "task_id": task_id,
                    "action": "done",
                    "title": t.title,
                })
                self._save()
                return f"Done. **+{points} pts** | Streak: {self.user_stats.current_streak} | Level {self.user_stats.level()}."
        return "Task not found."

    def _recent_skips(self) -> int:
        """Number of skips in last 14 days (for stricter messaging)."""
        return sum(1 for x in self.behavior_log[-14:] if x.get("action") == "skip")

    def skip_task(self, task_id: str) -> str:
        for t in self.tasks:
            if t.id == task_id:
                if t.done:
                    return "Task already done."
                t.skipped = True
                self.user_stats.total_points += POINTS_PER_SKIP_PENALTY
                self.behavior_log.append({
                    "date": _today_str(),
                    "task_id": task_id,
                    "action": "skip",
                    "title": t.title,
                })
                self._save()
                n = self._recent_skips()
                if n >= 3:
                    return f"Skipped. **{POINTS_PER_SKIP_PENALTY} pts.** You have skipped {n} times recently. Next skip will reduce your daily plan. Do the next task."
                return f"Skipped. **{POINTS_PER_SKIP_PENALTY} pts.** Stay consistent."
        return "Task not found."

    def suggest_daily_schedule(self, study_hours_per_day: float = DEFAULT_STUDY_HOURS_PER_DAY) -> str:
        if not self.subjects:
            return "Add subjects first. Then ask for *schedule*."
        total = sum(s.hours_per_week for s in self.subjects) or len(self.subjects) * 2
        sorted_subs = sorted(self.subjects, key=lambda x: (x.priority, -x.hours_per_week))
        lines = [f"**Today’s plan** ({study_hours_per_day}h total):"]
        for s in sorted_subs:
            ratio = (s.hours_per_week or 1) / max(total, 1)
            mins = max(15, int(study_hours_per_day * 60 * ratio))
            lines.append(f"• **{s.name}**: {mins} min")
        return "\n".join(lines)

    def suggest_weekly_schedule(self, study_hours_per_day: float = DEFAULT_STUDY_HOURS_PER_DAY) -> str:
        """Weekly view: distribute subjects across the week by hours_per_week."""
        if not self.subjects:
            return "Add subjects first. Then ask for *weekly plan*."
        sorted_subs = sorted(self.subjects, key=lambda x: (x.priority, -x.hours_per_week))
        lines = [f"**This week** (~{study_hours_per_day * 7:.0f}h total):"]
        for s in sorted_subs:
            mins_per_day = max(10, int((s.hours_per_week or 1) / 7 * 60))
            lines.append(f"• **{s.name}**: {s.hours_per_week}h/week → ~{mins_per_day} min/day")
        lines.append("")
        lines.append("**Focus:** Mon–Wed high-priority; Thu–Fri catch-up; Sat–Sun revision.")
        return "\n".join(lines)

    def get_todays_tasks(self) -> list[Task]:
        """Pending tasks (not done, not skipped) for today’s focus — by subject from daily plan."""
        pending = [t for t in self.tasks if not t.done and not t.skipped]
        return pending[:15]  # cap for UI

    def get_stats_text(self) -> str:
        s = self.user_stats
        return f"**Level {s.level()}** · {s.total_points} pts · Streak: {s.current_streak} days"

    # --- Exams ---
    def add_exam(self, name: str, subject_name: str, exam_date: str, weight: str = "", chapters: str = "") -> str:
        e = Exam(
            id=str(uuid.uuid4())[:8],
            name=name,
            subject_name=subject_name,
            exam_date=exam_date,
            weight=weight,
            chapters=chapters,
        )
        self.exams.append(e)
        self._save()
        return f"Exam added: **{name}** ({subject_name}) on {exam_date}. Days left: {e.days_left() or '?'}."

    def list_exams(self) -> str:
        if not self.exams:
            return "No exams. Add: *exam &lt;name&gt; &lt;subject&gt; &lt;YYYY-MM-DD&gt;*."
        lines = ["**Exams:** (use *revision plan &lt;id&gt;* for chapter spread)"]
        for e in self.exams:
            dl = e.days_left()
            dl_str = f" — {dl} days left" if dl is not None else ""
            lines.append(f"• **{e.name}** ({e.subject_name}) — {e.exam_date}{dl_str} `{e.id}`")
        return "\n".join(lines)

    def get_revision_plan(self, exam_id: str) -> str:
        """Spread exam chapters over days left. Exam must have chapters set (e.g. '1-5' or '1,2,3')."""
        exam = next((e for e in self.exams if e.id == exam_id), None)
        if not exam:
            return "Exam not found."
        days = exam.days_left()
        if days is None or days <= 0:
            return f"**{exam.name}** — date passed or invalid. No revision plan."
        ch = (exam.chapters or "").strip()
        if not ch:
            return f"**{exam.name}** — Add chapters first: edit exam or add with *exam ... chapters 1-5*."
        # Parse chapters: "1-5" -> [1,2,3,4,5], "1,2,3" -> [1,2,3]
        parts = []
        for p in ch.replace(",", " ").split():
            if "-" in p:
                a, b = p.split("-", 1)
                try:
                    parts.extend(range(int(a.strip()), int(b.strip()) + 1))
                except ValueError:
                    parts.append(p)
            else:
                try:
                    parts.append(int(p))
                except ValueError:
                    parts.append(p)
        if not parts:
            parts = [ch]
        # Spread over days_left (each day 1+ chapters if needed)
        n = len(parts)
        per_day = max(1, (n + days - 1) // days)
        lines = [f"**Revision plan: {exam.name}** — {n} items over {days} days:"]
        day = 1
        i = 0
        while i < n and day <= days:
            chunk = parts[i : i + per_day]
            i += len(chunk)
            ch_str = ", ".join(f"Ch{x}" for x in chunk)
            lines.append(f"• Day {day}: {ch_str}")
            day += 1
        return "\n".join(lines)

    # --- Adaptation (simple) ---
    def get_adaptive_study_hours(self) -> float:
        """Reduce load after skips; maintain or slightly increase when streak good."""
        recent = [x for x in self.behavior_log[-14:]]  # last 2 weeks
        skips = sum(1 for x in recent if x.get("action") == "skip")
        dones = sum(1 for x in recent if x.get("action") == "done")
        if skips > dones and skips >= 3:
            return max(2.0, DEFAULT_STUDY_HOURS_PER_DAY - 1.0)
        if self.user_stats.current_streak >= 3:
            return min(6.0, DEFAULT_STUDY_HOURS_PER_DAY + 0.5)
        return DEFAULT_STUDY_HOURS_PER_DAY

    def get_schedule_strict_note(self) -> str:
        """When consistency is low, return a one-line strict note to append to schedule."""
        if self._recent_skips() >= 3:
            return "\n\n⚠️ **Your plan is reduced** — complete tasks to restore full hours."
        return ""

    def clear(self) -> str:
        self.subjects.clear()
        self.tasks.clear()
        self.exams.clear()
        self.user_stats = UserStats()
        self.behavior_log.clear()
        self._save()
        return "All data cleared. Fresh start."


# --- Subject type from chat (coding / college) ---
SUBJECT_TYPE_KEYWORDS = {
    "coding": ["coding", "code", "dsa", "programming", "algorithms", "interview", "debugging"],
    "college": ["college", "theory", "numericals", "derivations"],
}


def _infer_subject_type(rest_lower: str) -> str:
    for stype, keywords in SUBJECT_TYPE_KEYWORDS.items():
        if any(kw in rest_lower for kw in keywords):
            return stype
    return "general"


# --- Command parsing (for chat) ---
def parse_add_command(text: str) -> dict | None:
    t = text.strip().lower()
    if not t.startswith("add ") and " add " not in t:
        return None
    rest = text.strip().split(" add ", 1)[-1].strip().replace("subject", "").replace("topic", "").strip()
    if not rest:
        return None
    subject_type = _infer_subject_type(rest)
    parts = rest.split()
    name_parts = []
    hours = 0.0
    for p in parts:
        try:
            hours = float(p)
            break
        except ValueError:
            name_parts.append(p)
    name = " ".join(name_parts).strip() if name_parts else (parts[0] if parts else "")
    if not name:
        return None
    if hours == 0:
        hours = 2.0
    return {"name": name, "hours": hours, "subject_type": subject_type}


# --- Explain topic (exam-oriented key points) ---
CONCEPT_BANK: dict[str, list[str]] = {
    "array": [
        "**Array** — contiguous memory; O(1) access by index; fixed size (or dynamic in some languages).",
        "Exam: traversal, two-pointer, prefix sum, sliding window.",
    ],
    "dsa": [
        "**DSA** — Data Structures (array, linked list, stack, queue, tree, graph, hash) + Algorithms (sort, search, recursion, DP).",
        "Exam: identify structure → choose algorithm → code with edge cases.",
    ],
    "recursion": [
        "**Recursion** — base case + recurrence; stack holds state; convert to iteration via stack/queue.",
        "Exam: tree/graph DFS, divide-and-conquer, backtracking.",
    ],
    "dynamic programming": [
        "**DP** — optimal substructure + overlapping subproblems; memoize or tabulate; state = (index, constraint).",
        "Exam: state definition, transition, base case, order of fill.",
    ],
    "linked list": [
        "**Linked list** — node (data, next); O(1) insert/delete at head; need pointer for middle; cycle detection = fast/slow.",
        "Exam: reverse, merge, find middle, detect cycle.",
    ],
    "sorting": [
        "**Sorting** — comparison: Merge O(n log n), Quick average O(n log n); non-comparison: Count, Radix.",
        "Exam: when stable matters; in-place; time/space trade-off.",
    ],
}


def explain_topic(topic: str) -> str:
    """Return exam-oriented key points for a topic. Fuzzy match on CONCEPT_BANK keys."""
    t = topic.strip().lower()
    if not t:
        return "Say *explain &lt;topic&gt;* — e.g. explain array, explain recursion, explain DP."
    for key, points in CONCEPT_BANK.items():
        if key in t or t in key:
            return "**" + key.title() + "** (exam focus):\n\n" + "\n\n".join(points)
    return f"No notes for \"{topic}\". Try: array, DSA, recursion, dynamic programming, linked list, sorting."


def get_greeting() -> str:
    return (
        "**Ultimate AI Study Planner Bot** — I plan, you execute.\n\n"
        "• *Add subject* — e.g. *Add Math 5* or *Add DSA 6*\n"
        "• *Schedule* — get today’s time split\n"
        "• *Task &lt;subject&gt; &lt;title&gt;* — add a task\n"
        "• *Tasks* — list tasks; *done &lt;id&gt;* / *skip &lt;id&gt;*\n"
        "• *Exam &lt;name&gt; &lt;subject&gt; &lt;date&gt;* — add exam\n"
        "• *Exams* — list · *Revision plan &lt;exam_id&gt;* — spread chapters over days left\n"
        "• *Weekly* — this week's plan\n"
        "• *Explain &lt;topic&gt;* — e.g. explain array, explain DP\n"
        "• *Stats* — points, level, streak · *Clear* — reset all\n\n"
        "What do you want to do?"
    )
