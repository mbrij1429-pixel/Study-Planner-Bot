"""
Study Planner Bot — chat with the bot to plan your study schedule.
"""
import streamlit as st
from planner import (
    StudyPlan,
    get_greeting,
    parse_add_command,
)

# Page config
st.set_page_config(
    page_title="Study Planner Bot",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for a cleaner chat look
st.markdown("""
<style>
    .stChatMessage {
        padding: 0.75rem 1rem;
        border-radius: 12px;
    }
    [data-testid="stChatMessage"] {
        background-color: rgba(240, 242, 246, 0.8);
    }
    .block-container {
        max-width: 720px;
        padding-top: 1.5rem;
    }
    h1 {
        font-size: 1.75rem;
        margin-bottom: 0.25rem;
    }
    .subtitle {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Persist plan in session state
if "plan" not in st.session_state:
    st.session_state.plan = StudyPlan()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": get_greeting()},
    ]


def bot_response(user_input: str) -> str:
    plan = st.session_state.plan
    text = user_input.strip().lower()

    # Add subject
    add_parsed = parse_add_command(user_input)
    if add_parsed:
        return plan.add_subject(
            name=add_parsed["name"],
            hours=add_parsed["hours"],
        )

    # List subjects
    if any(x in text for x in ("list", "show", "my subjects", "what are")):
        return plan.list_subjects()

    # Daily schedule
    if any(x in text for x in ("schedule", "daily", "plan for today", "today's plan")):
        return plan.suggest_daily_schedule(study_hours_per_day=4.0)

    # Clear
    if "clear" in text or "reset" in text:
        return plan.clear()

    # Hello / help
    if any(x in text for x in ("hi", "hello", "hey", "help")):
        return get_greeting()

    return (
        "I didn't quite get that. You can **add** a subject (e.g. *Add Math 5 hours*), "
        "**list** your subjects, ask for a **schedule**, or say **clear** to start over."
    )


# Title
st.title("📚 Study Planner Bot")
st.markdown('<p class="subtitle">Chat to add subjects and get a daily study plan.</p>', unsafe_allow_html=True)

# Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Add a subject, ask for schedule, or say 'list'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = bot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
