import streamlit as st
from transformers import pipeline
from PIL import Image
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Day Assistant", layout="wide")


# -------------- MODEL -------------------
@st.cache_resource
def load_classifier():
    return pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

classifier = load_classifier()


# -------------- HELPERS -----------------
def parse_tasks(text: str):
    """Split messy text into individual tasks."""
    text = text.replace("•", "-")
    raw = re.split(r"[,\n;]", text)
    tasks = [t.strip() for t in raw if len(t.strip()) > 2]
    return tasks


def analyze_task(task: str, boost=True):
    labels = [
        "Bug fix", "Feature development", "Refactoring", "Documentation",
        "Learning/Research", "Testing", "DevOps/Deployment", "Other"
    ]

    result = classifier(task, labels)
    task_type = result["labels"][0]

    t = task.lower()
    priority = "Medium"

    if boost and any(w in t for w in ["bug", "error", "fail", "crash", "urgent", "issue"]):
        priority = "High"
    elif any(w in t for w in ["doc", "documentation", "readme", "learn", "tutorial"]):
        priority = "Low"

    estimates = {
        "Bug fix": "1–2 hours",
        "Feature development": "3–5 hours",
        "Refactoring": "2–3 hours",
        "Documentation": "30–60 mins",
        "Learning/Research": "1–2 hours",
        "Testing": "1–3 hours",
        "DevOps/Deployment": "2–4 hours",
        "Other": "1–2 hours",
    }

    estimate = estimates.get(task_type, "1–2 hours")
    return task_type, priority, estimate


# -------------- STYLES ------------------
st.markdown(
    """
    <style>
    body {
        font-family: 'Inter', sans-serif;
    }
    .gradient-header {
        background: linear-gradient(120deg, #4f46e5, #7c3aed, #ec4899);
        padding: 18px 24px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 16px 40px rgba(0,0,0,0.45);
    }
    .gradient-title {
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .gradient-subtitle {
        font-size: 14px;
        opacity: 0.95;
    }
    .glass-card {
        background: rgba(15,23,42,0.8);
        border-radius: 18px;
        padding: 20px;
        border: 1px solid rgba(148,163,184,0.35);
        box-shadow: 0 14px 32px rgba(15,23,42,0.7);
    }
    .task-card {
        background: rgba(15,23,42,0.9);
        border-radius: 12px;
        padding: 12px;
        border: 1px solid rgba(148,163,184,0.35);
        margin-bottom: 10px;
    }
    .summary-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 14px;
        padding: 16px;
        border: 1px solid rgba(148,163,184,0.4);
        margin-bottom: 16px;
    }
    .stButton>button {
        background: linear-gradient(120deg, #6366f1, #ec4899);
        color: white !important;
        border-radius: 999px;
        border: none;
        padding: 8px 18px;
        font-weight: 600;
    }
    .stButton>button:hover {
        filter: brightness(1.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------- SESSION INIT ------------
if "username" not in st.session_state:
    st.session_state.username = None

if "tasks" not in st.session_state:
    st.session_state.tasks = []


# -------------- WELCOME SCREEN ----------
if st.session_state.username is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_center = st.columns([1, 1, 1])[1]

    with col_center:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Hi! I'm your AI Day Assistant")
        name = st.text_input("What should I call you?", placeholder="Aastha")
        if st.button("Start planning"):
            if name.strip():
                st.session_state.username = name.strip()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# -------------- MAIN DASHBOARD ----------
username = st.session_state.username

st.markdown(
    """
    <div class="gradient-header">
        <div class="gradient-title">AI Day Assistant</div>
        <div class="gradient-subtitle">
            Hi, I'm your AI buddy, helping you turn messy dev notes into a smart daily plan. ✨
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

top_col1, top_col2 = st.columns([0.2, 0.8])

with top_col1:
    try:
        avatar = Image.open("assistant.png")
        st.image(avatar, width=110)
    except:
        st.write("🤖")

with top_col2:
    st.markdown(f"#### Hey **{username}**, let's plan your day with AI 💻")

    r1, r2 = st.columns(2)
    with r1:
        if st.button("🔄 Reset tasks only"):
            st.session_state.tasks = []
            for k in list(st.session_state.keys()):
                if k.startswith("done_") or k.startswith("prio_"):
                    del st.session_state[k]
            st.rerun()
    with r2:
        if st.button("❌ Full reset (name + tasks)"):
            st.session_state.clear()
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

input_col, result_col = st.columns([0.45, 0.55])


# -------------- INPUT SIDE --------------
with input_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📝 Enter your tasks")
    example = (
        "fix login bug, update README, write tests for payment service, "
        "explore docker basics, refactor user service"
    )
    notes = st.text_area("Paste tasks:", height=170, placeholder=example)
    boost = st.checkbox("Boost urgent tasks", value=True)

    if st.button("⚡ Generate AI plan"):
        if not notes.strip():
            st.warning("Please enter at least one task.")
        else:
            raw_tasks = parse_tasks(notes)
            analyzed = []
            for t in raw_tasks:
                ttype, prio, est = analyze_task(t, boost)
                analyzed.append(
                    {
                        "text": t,
                        "type": ttype,
                        "priority": prio,
                        "estimate": est,
                    }
                )
            st.session_state.tasks = analyzed
            for k in list(st.session_state.keys()):
                if k.startswith("done_") or k.startswith("prio_"):
                    del st.session_state[k]
            st.success("Plan updated with AI ✨")
    st.markdown("</div>", unsafe_allow_html=True)


# -------------- RESULTS SIDE --------------
with result_col:
    tasks = st.session_state.tasks

    if tasks:
        # AI summary
        total = len(tasks)
        high = sum(1 for t in tasks if t["priority"] == "High")
        low = sum(1 for t in tasks if t["priority"] == "Low")

        if high >= 3:
            mood = "🔥 Busy & intense, but manageable!"
        elif total <= 3:
            mood = "✨ Light day, great for focused work."
        else:
            mood = "⚡ Balanced and productive day ahead."

        start_task = next((t["text"] for t in tasks if t["priority"] == "High"), tasks[0]["text"])

        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown("#### 🤖 AI Summary")
        st.write(f"**Mood:** {mood}")
        st.write(f"**Total tasks:** {total}")
        st.write(f"**High priority:** {high}  |  **Low priority:** {low}")
        st.write(f"**Start with:** _{start_task}_")
        st.markdown("</div>", unsafe_allow_html=True)

        # Task List
        st.markdown("#### 📋 Today's Tasks")

        to_delete = []

        for i, t in enumerate(tasks):
            st.markdown('<div class="task-card">', unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns([0.1, 0.55, 0.2, 0.15])

            with c1:
                st.checkbox("", key=f"done_{i}")

            with c2:
                st.markdown(f"**{t['text']}**")
                st.caption(f"{t['type']} • {t['estimate']}")

            with c3:
                new_prio = st.selectbox(
                    "Priority",
                    ["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(t["priority"]),
                    key=f"prio_{i}",
                )
                t["priority"] = new_prio

            with c4:
                if st.button("🗑", key=f"del_{i}"):
                    to_delete.append(i)

            st.markdown("</div>", unsafe_allow_html=True)

        if to_delete:
            for idx in sorted(to_delete, reverse=True):
                if idx < len(tasks):
                    tasks.pop(idx)
            st.session_state.tasks = tasks
            st.rerun()

        # ---- COMPLETION CELEBRATION ----
        all_done = all(st.session_state.get(f"done_{i}", False) for i in range(len(tasks)))

        if tasks and all_done:
            st.markdown(
                """
                <div style="
                    background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899);
                    padding: 25px;
                    border-radius: 18px;
                    text-align: center;
                    color: white;
                    font-weight: 700;
                    font-size: 22px;
                    margin-top: 20px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
                    animation: pop 0.8s ease-out;
                ">
                    🎉 All tasks completed! Amazing job, keep shining! ✨
                </div>

                <style>
                @keyframes pop {
                    0% { transform: scale(0.8); opacity: 0; }
                    100% { transform: scale(1); opacity: 1; }
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown("#### 🤖 AI Summary")
        st.write("No tasks yet. Paste your tasks on the left and click **Generate AI plan**.")
        st.markdown("</div>", unsafe_allow_html=True)