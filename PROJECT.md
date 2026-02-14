# AI Study & Planner Agent — Project Overview

**Author:** Krishna Singh ([@mbrij1429-pixel](https://github.com/mbrij1429-pixel))  
**Role:** Senior developer / AI architect  
**Goal:** Build an advanced, portfolio-level AI agent for study planning, task control, and adaptive behavior.

---

## 1. Current State (What You Have)

### Folder structure
```
Study & Planner Bot/
├── app.py          # Streamlit UI + chat flow
├── planner.py      # Core logic (subjects, schedule)
├── requirements.txt
├── README.md
└── PROJECT.md      # This file — roadmap & context
```

Everything is in the project root. No `src/`, no `tests/`, no persistence yet.

### What the code does today

| Component   | Responsibility |
|------------|-----------------|
| **planner.py** | `Subject` and `StudyPlan` dataclasses. Add/list subjects, suggest daily schedule (split by priority + hours). Simple text parsing for “add &lt;name&gt; &lt;hours&gt;”. |
| **app.py**     | Streamlit chat UI. Session state holds one `StudyPlan` and chat `messages`. User input is matched with keywords and passed to planner; no real “AI” yet. |

**Strengths:** Clean separation (UI vs logic), readable code, good base for “add subjects + get a plan.”

**Limitations relative to your vision:**
- No **tasks** (only subjects and a daily time split).
- No **points, levels, or discipline** (gamification / accountability).
- No **behavior tracking** or **adaptive difficulty**.
- No **exam-oriented** planning (revision blocks, countdown, past papers, etc.).
- No **persistence** (data is lost on refresh).
- No **real AI** (keyword matching only).

---

## 2. Where This Fits Your Vision

| Your goal                         | Current support | Next steps (idea) |
|----------------------------------|-----------------|-------------------|
| Study coding + college subjects   | ✅ Subjects + hours | Add “topics” or “chapters” per subject; link to tasks. |
| Daily + exam-oriented planning   | ✅ Daily only   | Add exams (date, weight), revision scheduler, countdown. |
| Tasks, points, levels, discipline| ❌ None         | Introduce tasks (done/not done), points per task, levels, streaks. |
| Track behavior, adapt difficulty | ❌ None         | Log completion + streaks; adjust suggested load by performance. |
| Portfolio-level, unique          | ⚠️ Good base    | Structure (e.g. `src/`), tests, docs, clear architecture. |

---

## 3. Proposed Roadmap (Step by Step)

We can grow in **small, shippable steps**. Each step stays readable and is a good commit.

1. **Stabilize & GitHub-ready**  
   - Add `.gitignore`, pin Streamlit version, maybe add a 1–2 line “how to run” in README.  
   - Optional: suggest a first commit message.

2. **Persistence**  
   - Save/load `StudyPlan` (e.g. JSON file or SQLite).  
   - So refresh and “tomorrow” don’t wipe data.

3. **Tasks**  
   - Tasks under subjects (e.g. “Finish Ch 3”, “Do 5 problems”).  
   - Mark done/not done; optional due date.  
   - UI: list tasks, mark complete, maybe “today’s tasks” from daily plan.

4. **Points & levels**  
   - Points for completing tasks; simple level = f(points).  
   - Show in UI (e.g. “Level 2 — 45 pts”).

5. **Discipline & streaks**  
   - Streak: days in a row with ≥1 task done.  
   - Optional: “discipline” score (e.g. % of planned tasks done this week).

6. **Exam mode**  
   - Exams: name, date, subject, weight.  
   - “Days left” and a simple revision plan (e.g. spread chapters over remaining days).

7. **Behavior & adaptation**  
   - Store completion history (e.g. daily summary).  
   - Use it to suggest “lighter” or “heavier” days, or more revision before exams.

8. **Real AI (optional)**  
   - Replace keyword matching with an LLM (e.g. API) for understanding intent and generating plans.  
   - Keep current logic as fallback and for structured actions.

**Architecture:** When we add persistence and tasks, we can introduce a simple layout (e.g. `src/`, `src/planner/`, `src/app.py` or `src/ui/`) and move code gradually. I’ll **ask before** any big move.

---

## 4. Workflow Rules (How We’ll Work)

- **Small changes:** One feature or one refactor per step.  
- **Readable code:** Clear names, short functions, a few comments where logic is non-obvious.  
- **After a feature:** I’ll suggest a commit message and what to include.  
- **Big changes:** I’ll propose and ask before restructuring or adding a new stack (e.g. DB, API).

---

## 5. Next Step (Your Choice)

Pick one and we’ll do it next:

- **A)** Make the repo GitHub-ready (`.gitignore`, README tweak, suggest first commit).  
- **B)** Add persistence (save/load plan so data survives refresh).  
- **C)** Sketch the “tasks + points + levels” model (data structures only, no UI yet).  
- **D)** Something else (e.g. focus on exam planning first, or a different order).

Tell me A, B, C, or D (or a small combo), and we’ll proceed step by step.
