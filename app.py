import streamlit as st
from datetime import date

# =========================================================
# MIKU WORLD — PYTHON + STREAMLIT
# Cute pastel welcome page, separate buttons, no timer
# =========================================================

st.set_page_config(
    page_title="Miku World",
    page_icon="🩵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------- SESSION DATA -------------------------
defaults = {
    "page": "welcome",
    "tasks": [],
    "xp": 0,
    "chat_history": [],
    "miku_style": "Original",
    "sound": True,
    "language": "English",
    "theme": "Sky Blue",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go(page):
    st.session_state.page = page


def level():
    return (st.session_state.xp // 100) + 1


def footer():
    st.markdown(
        "<div class='miku-footer'>୨୧ MIKU WORLD ♡ STUDY WITH SPARKLE ✦</div>",
        unsafe_allow_html=True,
    )


def title(text):
    st.markdown(f"<h2 class='section-title'>✦ {text} ✦</h2>", unsafe_allow_html=True)


def back_button():
    if st.button("(˶ᵔ ᵕ ᵔ˶)  BACK TO MENU", use_container_width=True, key="back_menu"):
        go("home")


def empty_miku():
    st.markdown("<div class='miku-space-title'>✧ MIKU'S SPACE ✧</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="miku-placeholder">
            <div class="miku-face">/ᐠ｡ꞈ｡ᐟ\\</div>
            <div class="miku-caption">Your 3D Miku model will live here ♡</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


SUBJECTS = [
    "Advanced Mathematics",
    "Basic Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Environmental Science",
    "Arabic",
    "English",
    "French",
    "History",
    "Geography",
    "Islamic Studies",
    "Arts",
    "Music",
    "Technology",
    "Physical Education",
]

# ------------------------- STYLE -------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --ink: #607b99;
    --ink-deep: #496985;
    --aqua: #c9f8fb;
    --pink: #ffe1f1;
    --lavender: #e9e3ff;
    --white: #ffffff;
}

.stApp {
    background:
        radial-gradient(ellipse at 82% 12%, rgba(255,255,255,.88) 0%, transparent 28%),
        radial-gradient(ellipse at 12% 82%, rgba(255,220,246,.72) 0%, transparent 34%),
        radial-gradient(ellipse at 55% 55%, rgba(225,248,255,.7) 0%, transparent 45%),
        repeating-linear-gradient(135deg,
            #c9f7fb 0px, #c9f7fb 42px,
            #b9eff7 42px, #b9eff7 84px);
    font-family: 'Nunito', sans-serif;
    color: var(--ink-deep);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.35rem;
    padding-bottom: 2rem;
}
header, footer { visibility: hidden; }

h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {
    font-family: 'Nunito', sans-serif;
}
h1, h2, h3, h4 {
    color: var(--ink) !important;
    font-family: 'Baloo 2', 'Nunito', sans-serif !important;
}
p { line-height: 1.8; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f0fdff 0%, #f8edff 55%, #fff0f8 100%);
    border-right: 2px solid rgba(255,255,255,.95);
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
    color: var(--ink) !important;
}

/* Buttons: each button is its own separate surface */
div.stButton > button,
.stFormSubmitButton > button {
    width: 100%;
    min-height: 64px;
    background: linear-gradient(180deg, #ffffff 0%, #fffaff 52%, #eafaff 100%);
    color: #7189a0;
    border: 2px solid rgba(255,255,255,.98);
    border-radius: 18px;
    font-family: 'Baloo 2', 'Nunito', sans-serif;
    font-size: 1.12rem;
    font-weight: 800;
    box-shadow:
        0 5px 0 rgba(165,199,215,.72),
        0 10px 22px rgba(91,144,172,.13),
        inset 0 2px 0 #ffffff;
    transition: transform .18s ease, background .18s ease, color .18s ease, box-shadow .18s ease;
}
div.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-3px) scale(1.025);
    background: linear-gradient(140deg, #fff5fb, #e6fdff 55%, #f0eaff);
    color: #587a9c;
    border-color: #ffffff;
    box-shadow:
        0 0 0 3px rgba(255,255,255,.45),
        0 7px 0 rgba(174,203,220,.75),
        0 14px 26px rgba(91,144,172,.20);
}
div.stButton > button:active,
.stFormSubmitButton > button:active {
    transform: scale(.985) translateY(2px);
}

/* Glass cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, rgba(255,255,255,.82), rgba(248,250,255,.70));
    border: 2px solid rgba(255,255,255,.92) !important;
    border-radius: 24px !important;
    box-shadow: 0 7px 0 rgba(167,205,220,.42), 0 14px 28px rgba(91,144,172,.10);
}

/* Form elements */
.stTextInput input, .stTextArea textarea, .stDateInput input {
    border-radius: 14px !important;
    border: 1px solid #d7eaf4 !important;
    background: rgba(255,255,255,.92) !important;
    color: #58718c !important;
}
.stSelectbox div[data-baseweb="select"] {
    border-radius: 14px !important;
    background: rgba(255,255,255,.92);
}
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,.86);
    border: 2px solid #ffffff;
    border-radius: 18px;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #8beaf0, #e6b9f4, #ffcce8);
}
.stCheckbox label {
    color: #607b99 !important;
    font-weight: 800;
}
.section-title {
    text-align: center;
    letter-spacing: .4px;
    margin: .2rem 0 1.1rem 0;
}
.miku-space-title {
    color: #6887a3;
    font-family: 'Baloo 2', sans-serif;
    font-size: 1.65rem;
    font-weight: 800;
    text-align: center;
    margin: 0 0 .8rem 0;
}
.miku-placeholder {
    min-height: 390px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 2px solid rgba(255,255,255,.92);
    border-radius: 32px;
    background:
        radial-gradient(circle at 50% 40%, rgba(255,255,255,.86), rgba(232,249,255,.45) 48%, rgba(246,228,255,.40)),
        linear-gradient(145deg, rgba(255,255,255,.55), rgba(220,248,255,.4));
    box-shadow: inset 0 0 28px rgba(255,255,255,.7), 0 8px 0 rgba(171,205,222,.32);
}
.miku-face {
    color: #7897b5;
    font-size: clamp(3.2rem, 6vw, 5.8rem);
    font-weight: 800;
    text-shadow: 0 5px 0 rgba(255,255,255,.85), 0 12px 20px rgba(127,163,190,.18);
    animation: floaty 3.5s ease-in-out infinite;
}
.miku-caption {
    color: #819bb2;
    font-size: 1rem;
    font-weight: 700;
    margin-top: 1.1rem;
    text-align: center;
}
@keyframes floaty {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
.miku-footer {
    text-align: center;
    color: #6e8aa5;
    font-family: 'Baloo 2', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    margin-top: 1.8rem;
    letter-spacing: .5px;
}
.small-note {
    text-align: center;
    color: #7e97ad;
    font-weight: 700;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------- SIDEBAR -------------------------
with st.sidebar:
    st.markdown("# ୨୧ MIKU WORLD")
    st.caption("Your little study universe ♡")
    st.divider()

    if st.button("(⌂)  HOME", use_container_width=True, key="nav_home"):
        go("home")
    if st.button("(≧▽≦)  MY TASKS", use_container_width=True, key="nav_tasks"):
        go("tasks")
    if st.button("(｡•̀ᴗ-)✧  ASK MIKU", use_container_width=True, key="nav_chat"):
        go("chat")
    if st.button("(๑˃ᴗ˂)ﻭ  ACHIEVEMENTS", use_container_width=True, key="nav_achievements"):
        go("achievements")
    if st.button("♡  CHANGE MIKU", use_container_width=True, key="nav_customization"):
        go("customization")
    if st.button("(⚙)  SETTINGS", use_container_width=True, key="nav_settings"):
        go("settings")

    st.divider()
    st.markdown(f"### ♡ LEVEL {level()}")
    st.markdown(f"### {st.session_state.xp} XP")

# ------------------------- WELCOME -------------------------
if st.session_state.page == "welcome":
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        st.markdown("# ✦ MIKU WORLD ✦")
        st.markdown("### Your magical study adventure ♡")
        with st.container(border=True):
            st.markdown("## Welcome to Miku World ♡")
            st.markdown(
                """
                Your little universe for studying, creating, and celebrating every achievement.

                Every tiny step brings you closer to your dreams.
                Miku is right here with you!  (˶ᵔ ᵕ ᵔ˶)
                """
            )
            st.markdown("### Ready to begin your journey?")
        st.write("")
        if st.button("✧  ENTER APP  ✧", use_container_width=True, key="enter_app"):
            go("home")
        st.write("")
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            if st.button("(๑˃ᴗ˂)ﻭ  ACHIEVEMENTS", use_container_width=True, key="welcome_achievements"):
                go("achievements")
        with col2:
            if st.button("(⚙)  SETTINGS", use_container_width=True, key="welcome_settings"):
                go("settings")
        if st.button("♡  CHANGE MIKU  ♡", use_container_width=True, key="welcome_customization"):
            go("customization")
    with right:
        empty_miku()
    footer()

# ------------------------- HOME -------------------------
elif st.session_state.page == "home":
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        st.markdown("# HELLO, STUDY STAR! ♡")
        st.markdown("### ✦ Let's make today magical ✦")
        with st.container(border=True):
            st.markdown("## Welcome back to Miku World")
            st.write("Choose a space and start a new little adventure. (≧▽≦)")
        st.write("")
        if st.button("(≧▽≦)  MY TASKS", use_container_width=True, key="home_tasks"):
            go("tasks")
        if st.button("(｡•̀ᴗ-)✧  ASK MIKU", use_container_width=True, key="home_chat"):
            go("chat")
        if st.button("(๑˃ᴗ˂)ﻭ  ACHIEVEMENTS", use_container_width=True, key="home_achievements"):
            go("achievements")
        if st.button("♡  CUSTOMIZATION", use_container_width=True, key="home_customization"):
            go("customization")
    with right:
        empty_miku()
    footer()

# ------------------------- TASKS -------------------------
elif st.session_state.page == "tasks":
    title("MY TASKS & HOMEWORK")
    with st.container(border=True):
        st.markdown("### Every finished task is a little victory! (๑˃ᴗ˂)ﻭ")
        st.write("Add your homework, choose a subject, and set its due date.")
    st.write("")

    with st.form("task_form", clear_on_submit=True):
        task_name = st.text_input("Task name")
        subject = st.selectbox("Subject", SUBJECTS)
        due_date = st.date_input("Due date", value=date.today())
        submitted = st.form_submit_button("＋  ADD TASK", use_container_width=True)
        if submitted:
            if task_name.strip():
                st.session_state.tasks.append({
                    "name": task_name.strip(),
                    "subject": subject,
                    "due": str(due_date),
                    "done": False,
                })
                st.success("Task added! (˶ᵔ ᵕ ᵔ˶)")
                st.rerun()
            else:
                st.warning("Please enter a task name first.")

    st.divider()
    title("TASK LIST")
    if not st.session_state.tasks:
        st.info("No tasks yet. Add your first one! ♡")
    else:
        for i, task in enumerate(st.session_state.tasks):
            with st.container(border=True):
                st.markdown(f"### {task['subject']}")
                st.write(task["name"])
                st.caption(f"Due date: {task['due']}")
                checked = st.checkbox("Completed!", value=task["done"], key=f"task_done_{i}")
                if checked and not task["done"]:
                    task["done"] = True
                    st.session_state.xp += 25
                    st.success("Great job! +25 XP ♡")
                    st.rerun()
                elif not checked and task["done"]:
                    task["done"] = False
                    st.session_state.xp = max(0, st.session_state.xp - 25)
                    st.rerun()
                if st.button("(×)  DELETE TASK", key=f"delete_{i}"):
                    if task["done"]:
                        st.session_state.xp = max(0, st.session_state.xp - 25)
                    st.session_state.tasks.pop(i)
                    st.rerun()
    back_button()
    footer()

# ------------------------- ASK MIKU -------------------------
elif st.session_state.page == "chat":
    title("ASK MIKU")
    with st.container(border=True):
        st.markdown("## Miku is here to help! (｡•̀ᴗ-)✧")
        st.write("Write a school question or tell Miku what you want to understand.")
    st.write("")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    user_message = st.chat_input("Write a message to Miku...")
    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "I got your question! ♡ AI connection can be added in the next step.",
        })
        st.rerun()
    if st.button("(×)  CLEAR CHAT", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()
    back_button()
    footer()

# ------------------------- ACHIEVEMENTS -------------------------
elif st.session_state.page == "achievements":
    title("MY ACHIEVEMENTS")
    with st.container(border=True):
        st.markdown("## You're doing amazing! ♡")
        st.markdown(f"# LEVEL {level()}")
        st.markdown(f"## {st.session_state.xp} XP")
        st.write("Keep going. Every little step makes a difference. (≧▽≦)")
    st.write("")
    progress = (st.session_state.xp % 100) / 100
    st.progress(progress)
    st.caption(f"{100 - (st.session_state.xp % 100)} XP until your next level!")
    completed = sum(1 for task in st.session_state.tasks if task["done"])
    total = len(st.session_state.tasks)
    with st.container(border=True):
        st.markdown("### COMPLETED TASKS")
        st.markdown(f"# {completed} / {total}")
    back_button()
    footer()

# ------------------------- CUSTOMIZATION -------------------------
elif st.session_state.page == "customization":
    title("CHANGE MIKU")
    with st.container(border=True):
        st.markdown("## Choose your favorite style ♡")
        st.write("Miku's space is ready for the 3D model whenever you add it.")
    st.selectbox("Miku Style", ["Original", "Cute", "Crystal", "Baby Pink"], key="miku_style")
    empty_miku()
    back_button()
    footer()

# ------------------------- SETTINGS -------------------------
elif st.session_state.page == "settings":
    title("SETTINGS")
    with st.container(border=True):
        st.markdown("## Customize your world ♡")
        st.write("Make your Miku World feel like your own.")
    st.checkbox("Enable sound effects", key="sound")
    st.selectbox("App language", ["English"], key="language")
    st.selectbox("Interface theme", ["Sky Blue", "Lavender", "Baby Pink"], key="theme")
    if st.button("(↶)  BACK TO WELCOME", use_container_width=True, key="settings_welcome"):
        go("welcome")
    footer()
