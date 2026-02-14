# Study Planner Bot

A simple chat-style bot that helps you plan your study schedule.

**Author:** [Krishna Singh](https://github.com/mbrij1429-pixel) · **GitHub:** [@mbrij1429-pixel]

Add subjects, set weekly hours, and get a suggested daily plan.

## What it does

- **Add subjects** — e.g. "Add Math 5 hours" or "Add Physics"
- **List subjects** — "list subjects" / "show my subjects"
- **Daily schedule** — "schedule" / "daily plan" to get a time split for today
- **Clear** — "clear" to remove all subjects and start over

## Setup

1. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

4. Open the URL shown in the terminal (usually http://localhost:8501) and chat with the bot.

## Project structure

- `app.py` — Streamlit chat UI and bot flow
- `planner.py` — Study plan logic (subjects, schedule suggestion)
- `requirements.txt` — Python dependencies
- `PROJECT.md` — Roadmap and project overview

## License

MIT — feel free to use and modify. If you use this as a reference, a star or credit is appreciated.
