# Ultimate AI Study Planner Bot — Project Overview

**Author:** Krishna Singh ([@mbrij1429-pixel](https://github.com/mbrij1429-pixel))  
**Vision:** Autonomous AI mentor that controls, optimizes, and trains study behavior. See **[VISION.md](VISION.md)** for full vision, gap analysis, and roadmap.

---

## Current structure

```
Study & Planner Bot/
├── app.py           # Streamlit UI: chat + sidebar (stats, today’s tasks)
├── planner.py       # Domain: Subject, Task, Exam, UserStats, StudyPlan, persistence
├── storage.py       # Persistence layer (JSON)
├── requirements.txt
├── README.md
├── PROJECT.md       # This file
├── VISION.md        # Vision, gaps, roadmap
└── .gitignore
```

---

## Recommended next feature

**Persistence** — Save/load study plan (and later tasks, stats) so data survives refresh and restarts. This is the foundation for tracking, adaptation, points, and streaks.

Details and rationale: **[VISION.md §4](VISION.md#4-single-most-important-next-feature-persistence)**.

---

## Workflow

- Build step by step; small, PR-worthy changes.
- After each feature: suggest commit message + PR title/description.
- Major architecture changes: propose first, then implement after your go-ahead.
