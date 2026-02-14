# Ultimate AI Study Planner Bot

An AI-powered study mentor that **plans your schedule, assigns tasks, tracks completion, and adapts** — for coding (DSA, interview prep) and college subjects.

**Author:** [Krishna Singh](https://github.com/mbrij1429-pixel) · **GitHub:** [@mbrij1429-pixel](https://github.com/mbrij1429-pixel)

---

## What it does

- **Plan** — Daily schedule (time split by subject); adaptive study hours based on your consistency.
- **Subjects** — Add subjects with hours/week and priority (coding vs college).
- **Tasks** — Add tasks per subject, mark **done** (earn points) or **skip** (penalty); track in sidebar.
- **Exams** — Add exams with date; see days left.
- **Points, level, streak** — Earn points per task, level up, build a daily streak; streak bonus points.
- **Persistence** — All data saved to `study_plan_data.json` (survives refresh and restart).
- **Strict mentor tone** — Clear, point-wise responses; focuses on results.

## Setup

1. **Clone and enter the project**
   ```bash
   cd "Study & Planner Bot"
   ```

2. **Virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open the URL (e.g. http://localhost:8501). Use the **sidebar** for stats and today’s tasks; use the **chat** to add subjects, tasks, exams, and ask for schedule/stats.

## Commands (chat)

| Command | Example |
|--------|--------|
| Add subject | `Add Math 5` or `Add DSA 6` |
| Schedule | `schedule` or `today's plan` |
| Add task | `task Math Solve Ch 3 problems` or `task DSA Two sum due 2025-03-01` |
| List tasks | `tasks` |
| Complete / skip | `done abc123` or `skip abc123` |
| Add exam | `exam Midterm Math 2025-03-15` |
| List exams | `exams` |
| Stats | `stats` |
| Clear all | `clear` |

## Project structure

- `app.py` — Streamlit UI (chat + sidebar stats and task buttons).
- `planner.py` — Domain logic: subjects, tasks, exams, points, levels, streaks, behavior log, persistence.
- `storage.py` — Persistence layer (JSON read/write).
- `requirements.txt` — Python dependencies.
- `VISION.md` — Vision, gap analysis, roadmap.
- `PROJECT.md` — Overview and workflow.

## License

MIT — use and modify as you like. A star or credit is appreciated.
