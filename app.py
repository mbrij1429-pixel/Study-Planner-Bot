"""
Ultimate AI Study Planner Bot — autonomous mentor UI.
Chat + sidebar stats, today's tasks, points, levels, streaks.
"""
import re
import streamlit as st
from planner import (
    StudyPlan,
    get_greeting,
    parse_add_command,
)

st.set_page_config(
    page_title="Ultimate AI Study Planner Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container { max-width: 900px; padding-top: 1rem; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); }
    [data-testid="stSidebar"] .stMarkdown { color: #e2e8f0; }
    .stat-box { background: #334155; border-radius: 8px; padding: 0.75rem 1rem; margin: 0.5rem 0; }
    .stat-label { font-size: 0.75rem; color: #94a3b8; }
    .stat-value { font-size: 1.25rem; font-weight: 700; color: #f8fafc; }
    h1 { font-size: 1.6rem; }
    .subtitle { color: #64748b; font-size: 0.9rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

if "plan" not in st.session_state:
    st.session_state.plan = StudyPlan()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": get_greeting()}]

plan = st.session_state.plan


def bot_response(user_input: str) -> str:
    text = user_input.strip().lower()
    raw = user_input.strip()

    # Add subject (with optional subject_type: coding/college from parse_add_command)
    add_parsed = parse_add_command(raw)
    if add_parsed:
        return plan.add_subject(
            name=add_parsed["name"],
            hours=add_parsed["hours"],
            subject_type=add_parsed.get("subject_type", "general"),
        )

    # Task <subject> <title> [due YYYY-MM-DD]
    task_match = re.match(r"task\s+(.+?)(?:\s+due\s+(\d{4}-\d{2}-\d{2}))?$", raw, re.I | re.DOTALL)
    if task_match:
        rest = task_match.group(1).strip()
        due = task_match.group(2)
        parts = rest.split(maxsplit=1)
        if len(parts) >= 2:
            return plan.add_task(parts[0], parts[1], due)
        return "Use: *task &lt;subject&gt; &lt;title&gt;* or *task &lt;subject&gt; &lt;title&gt; due YYYY-MM-DD*."

    # Done <task_id>
    done_match = re.match(r"done\s+(\w+)", text)
    if done_match:
        return plan.complete_task(done_match.group(1).strip())

    # Skip <task_id>
    skip_match = re.match(r"skip\s+(\w+)", text)
    if skip_match:
        return plan.skip_task(skip_match.group(1).strip())

    # Revision plan <exam_id>
    rev_match = re.match(r"revision\s+(?:plan\s+)?(\w+)", text)
    if rev_match:
        return plan.get_revision_plan(rev_match.group(1).strip())

    # Exam <name> <subject> <date> [chapters 1-5]
    exam_match = re.match(r"exam\s+(.+?)\s+(\S+)\s+(\d{4}-\d{2}-\d{2})(?:\s+chapters\s+(.+))?$", raw, re.I)
    if exam_match:
        name = exam_match.group(1).strip()
        subj = exam_match.group(2).strip()
        d = exam_match.group(3).strip()
        chapters = (exam_match.group(4) or "").strip()
        return plan.add_exam(name, subj, d, chapters=chapters)

    # List / show
    if any(x in text for x in ("list subjects", "show subjects", "subjects", "what are my subjects")):
        return plan.list_subjects()
    if any(x in text for x in ("list tasks", "show tasks", "my tasks", "tasks")) and "task" in text:
        return plan.list_tasks(pending_only=True)
    if any(x in text for x in ("list exams", "exams", "show exams")):
        return plan.list_exams()
    if "stats" in text or "level" in text or "points" in text or "streak" in text:
        return plan.get_stats_text()

    # Weekly plan
    if any(x in text for x in ("weekly", "week plan", "this week")):
        hours = plan.get_adaptive_study_hours()
        return plan.suggest_weekly_schedule(study_hours_per_day=hours)

    # Schedule / daily plan
    if any(x in text for x in ("schedule", "daily", "plan for today", "today", "plan")):
        hours = plan.get_adaptive_study_hours()
        return plan.suggest_daily_schedule(study_hours_per_day=hours)

    # Clear / reset
    if "clear" in text or "reset" in text:
        return plan.clear()

    # Greeting / help
    if any(x in text for x in ("hi", "hello", "hey", "help")):
        return get_greeting()

    return (
        "Unclear. Use: *add &lt;subject&gt; &lt;hours&gt;*, *schedule*, *weekly*, *task ...*, *tasks*, "
        "*done/skip &lt;id&gt;*, *exam ...*, *revision plan &lt;exam_id&gt;*, *exams*, *stats*, *clear*."
    )


# ----- Sidebar: stats + today's tasks -----
with st.sidebar:
    st.markdown("### 📊 Your stats")
    stats_text = plan.get_stats_text().replace("**", "")
    st.caption(stats_text)
    st.markdown("---")
    st.markdown("### 📋 Today's tasks")
    todays = plan.get_todays_tasks()
    if not todays:
        st.caption("No pending tasks. Add subjects, then *task &lt;subject&gt; &lt;title&gt;*.")
    else:
        for t in todays[:10]:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.caption(f"**{t.title}** — {t.subject_name} `{t.id}`")
            with col2:
                if st.button("✓", key=f"done_{t.id}", help="Mark done"):
                    plan.complete_task(t.id)
                    st.rerun()
                if st.button("⊘", key=f"skip_{t.id}", help="Skip"):
                    plan.skip_task(t.id)
                    st.rerun()
    st.markdown("---")
    st.caption("Ultimate AI Study Planner Bot · Control your study.")

# ----- Main: chat -----
st.title("📚 Ultimate AI Study Planner Bot")
st.markdown('<p class="subtitle">Your autonomous study mentor — add subjects, tasks, exams; track points and streaks.</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Add subject, task, ask for schedule, stats, exams..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = bot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
