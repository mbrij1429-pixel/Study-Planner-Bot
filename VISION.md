# Ultimate AI Study Planner Bot — Vision & Gap Analysis

**Project:** Ultimate AI Study Planner Bot  
**Author:** Krishna Singh ([@mbrij1429-pixel](https://github.com/mbrij1429-pixel))  
**Role:** Autonomous mentor that controls, optimizes, and trains study behavior — not a normal chatbot or planner.

---

## 1. Project Vision (What the Bot Must Do)

| Area | Requirement |
|------|-------------|
| **Planning** | Daily, weekly, and exam-oriented schedules; break large goals into small, time-bound, high-ROI tasks. |
| **Domains** | Coding (DSA, programming, debugging, interview prep) + college (theory, numericals, derivations, exams). |
| **Control** | Decide what to study, when, and for how long; reduce decision fatigue. |
| **Tracking** | Task completion, delays, skips, accuracy, consistency. |
| **Adaptation** | Understand study behavior; adapt plans automatically; stricter when procrastinating, raise difficulty when improving. |
| **Gamification** | Points, levels, penalties, streaks, progression to enforce discipline. |
| **Teaching** | Explain concepts clearly, exam-oriented, step-by-step; focus on results, not comfort. |
| **Persona** | Strict but intelligent mentor; clear, point-wise, no-fluff communication. |

---

## 2. Current Codebase Summary

### Folder structure
```
Study & Planner Bot/
├── app.py           # Streamlit chat UI; session state only
├── planner.py       # Subject + StudyPlan; add/list subjects, suggest daily time split
├── requirements.txt
├── README.md
├── PROJECT.md       # Roadmap
├── VISION.md        # This file
└── .gitignore
```

### What exists today
- **Subjects:** Name, hours/week, priority, optional deadline.
- **Actions:** Add subject, list subjects, suggest daily schedule (time split by priority/hours), clear.
- **UI:** Chat-style Streamlit; keyword-based intent (no real AI).
- **State:** In-memory only; lost on refresh.

### Strengths
- Clear separation: UI (`app.py`) vs domain logic (`planner.py`).
- Readable, minimal code; easy to extend.

---

## 3. Gap Analysis (Vision vs Current)

| Vision requirement | Current support | Gap severity |
|--------------------|-----------------|--------------|
| Daily + weekly + exam planning | Daily time-split only; no weekly, no exams | **High** |
| Coding vs college (DSA, theory, numericals) | Generic “subjects” only | **Medium** |
| Small, time-bound, high-ROI **tasks** | No tasks; only subjects + time blocks | **Critical** |
| Bot **decides** what/when/how long | Suggests only; no enforcement | **High** |
| Track completion, delays, skips, accuracy | None | **Critical** |
| Adapt plans from behavior | None | **Critical** |
| Points, levels, penalties, streaks | None | **Critical** |
| Stricter / harder based on behavior | None | **Critical** |
| Teaching, exam-oriented content | None | **Future** |
| **Persistence** (data survives refresh/restart) | Session only | **Critical** |

**Weaknesses**
- No persistence → no history, no adaptation, no real “control.”
- No task model → nothing to complete, skip, or score; no points/levels/streaks.
- No behavior log → can’t adapt difficulty or strictness.
- Flat structure → will need `src/`, tests, and clearer modules as we add features.

---

## 4. Single Most Important Next Feature: **Persistence**

**Recommendation:** Implement **data persistence** (save/load study plan + future state) as the next feature.

**Why this first**
1. **Everything else depends on it.** Tracking behavior, points, streaks, and adaptation require data that survives refresh and restart. Without persistence, the bot cannot “remember” or “control” anything across sessions.
2. **Smallest foundational step.** We already have `StudyPlan` and `Subject`; we only need to serialize/deserialize and load on startup, save on change. No new domain concepts yet.
3. **Unblocks all later work.** Tasks, points, and behavior log will need to be persisted from day one; adding persistence now avoids rework and keeps the repo clean.

**What “persistence” means for this step**
- Save/load **subjects** (and later: tasks, user stats, behavior log) to a single file (e.g. JSON) or SQLite.
- Load on app start; save after every change (or on a short debounce).
- Keep the current in-memory model; add a thin persistence layer so the rest of the app stays unchanged.

**Immediately after persistence**
- **Tasks:** Add tasks under subjects (with done/skip/due); then the bot has something to assign, track, and score. That unlocks points, levels, and streaks.

---

## 5. How We’ll Work (Cursor + GitHub)

- **Steps:** Small, PR-worthy changes; one feature or one refactor at a time.
- **Code:** Clean, modular, production-quality; explain when you ask.
- **Architecture:** I’ll ask before major structural or stack changes.
- **Git:** After each completed feature: suggest commit message, PR title, and PR description so the repo stays GitHub-ready.

---

## 6. Next Action

**Build persistence next.**  
Say **“Add persistence”** (or “go ahead with persistence”) and I’ll implement save/load for the current plan (subjects) and wire it into the app, then suggest a commit and PR.
