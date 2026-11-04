
import streamlit as st
from datetime import date

# =========================================================
# MIKU WORLD — PYTHON + STREAMLIT
# =========================================================

st.set_page_config(
    page_title="Miku World",
    page_icon="🩵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION DATA
# =========================================================

defaults = {
    "page": "welcome",
    "tasks": [],
    "xp": 0,
    "chat_history": [],
    "miku_style": "Original",
    "sound": True,
    "language": "العربية",
    "theme": "Sky Blue",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go(page):
    st.session_state.page = page


# =========================================================
# COLORS + STYLE
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 80% 10%, #a4f4f5 0%, transparent 30%),
        radial-gradient(ellipse at 10% 90%, #e8bfff 0%, transparent 35%),
        repeating-linear-gradient(
            135deg,
            #18c5d6 0px,
            #18c5d6 38px,
            #0fb5ca 38px,
            #0fb5ca 76px
        );
    font-family: 'Tajawal', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

header, footer {
    visibility: hidden;
}

h1, h2, h3, h4 {
    font-family: 'Baloo 2', 'Tajawal', sans-serif !important;
    color: #54728b !important;
}

p {
    line-height: 1.8;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e8fbff, #f4e5ff);
    border-right: 3px solid #ffffff;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: #54728b !important;
}

/* All buttons */
div.stButton > button {
    width: 100%;
    min-height: 68px;

    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f8fdff 50%,
        #e8f7fb 100%
    );

    color: #7c8995;
    border: 3px solid #ffffff;
    border-radius: 4px;

    font-family: 'Baloo 2', 'Tajawal', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;

    box-shadow:
        0 7px 0 #91a9b7,
        0 12px 22px rgba(30, 90, 120, .16),
        inset 0 2px 0 #ffffff;

    transition:
        transform .18s ease,
        background .18s ease,
        color .18s ease,
        box-shadow .18s ease;

    clip-path: polygon(
        0 0,
        93% 0,
        100% 50%,
        93% 100%,
        0 100%,
        3% 50%
    );
}

/* Hover */
div.stButton > button:hover {
    transform: scale(1.035);

    background: linear-gradient(
        180deg,
        #65f3f2,
        #0acbd9
    );

    color: #ffffff;

    border: 3px solid #ffffff;

    box-shadow:
        0 0 14px rgba(225, 255, 255, .9),
        0 8px 0 #078a9b,
        0 15px 25px rgba(0, 90, 120, .25);
}

/* Click */
div.stButton > button:active {
    transform: scale(.985) translateY(3px);
}

/* Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.96),
        rgba(237,250,255,.90)
    );

    border: 2px solid #ffffff !important;
    border-radius: 22px !important;

    box-shadow:
        0 8px 0 rgba(110, 175, 195, .45),
        0 15px 30px rgba(30, 90, 120, .12);
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div,
.stDateInput input {
    border-radius: 13px !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,.90);
    border: 2px solid #ffffff;
    border-radius: 18px;
}

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, #6ce9ef, #d4aaff);
}

/* Checkbox */
.stCheckbox label {
    color: #54728b !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# COMMON HELPERS
# =========================================================

SUBJECTS = [
    "رياضيات متقدمة",
    "رياضيات أساسية",
    "فيزياء",
    "كيمياء",
    "أحياء",
    "علوم بيئة",
    "عربي",
    "إنجليزي",
    "فرنسي",
    "تاريخ",
    "جغرافيا",
    "دراسات إسلامية",
    "فنون",
    "موسيقى",
    "تقنية",
    "رياضة"
]


def title(text):
    st.markdown(f"## ✦ {text} ✦")


def footer():
    st.markdown(
        "୨୧ **MIKU WORLD ♡ STUDY WITH SPARKLE ✦**",
        text_alignment="center"
    )


def back_button():
    if st.button("◀  BACK TO MENU", use_container_width=True):
        go("home")


def empty_miku():
    st.markdown("### ✧ MIKU'S SPACE ✧")

    # مكان ميكو يبقى فارغًا حتى نضيف المجسم
    st.container(border=True)


def level():
    return (st.session_state.xp // 100) + 1


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# ୨୧ MIKU WORLD")
    st.caption("Your little study universe 🩵")

    st.divider()

    if st.button("🏠  الرئيسية", use_container_width=True):
        go("home")

    if st.button("📚  مهامي وواجباتي", use_container_width=True):
        go("tasks")

    if st.button("💬  اسألي ميكو", use_container_width=True):
        go("chat")

    if st.button("🏆  إنجازاتي", use_container_width=True):
        go("achievements")

    if st.button("🎀  تغيير شكل ميكو", use_container_width=True):
        go("customization")

    if st.button("⚙️  الإعدادات", use_container_width=True):
        go("settings")

    st.divider()

    st.markdown(f"### ⭐ Level {level()}")
    st.markdown(f"### 🩵 {st.session_state.xp} XP")


# =========================================================
# WELCOME
# =========================================================

if st.session_state.page == "welcome":

    left, right = st.columns([1.1, 1], gap="large")

    with left:

        st.markdown("# ✦ MIKU WORLD ✦")
        st.markdown("### Your magical study adventure ♡")

        with st.container(border=True):

            st.markdown("## Welcome to Miku World ♡")

            st.markdown("""
            عالمك الصغير للدراسة والإنجاز والإبداع.

            كل خطوة تخطينها هنا تقرّبك من هدفك،
            وميكو معك في رحلتك! 🩵
            """)

            st.markdown("### Ready to begin your journey?")

        st.write("")

        if st.button("✦  ENTER APP  ✦", use_container_width=True):
            go("home")

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🏆 ACHIEVEMENTS", use_container_width=True):
                go("achievements")

        with col2:
            if st.button("⚙️ SETTINGS", use_container_width=True):
                go("settings")

        if st.button("🎀 CHANGE MIKU", use_container_width=True):
            go("customization")

    with right:

        empty_miku()

    footer()


# =========================================================
# HOME
# =========================================================

elif st.session_state.page == "home":

    left, right = st.columns([1.1, 1], gap="large")

    with left:

        st.markdown("# HELLO, STUDY STAR! ♡")
        st.markdown("### ✦ Let's make today magical ✦")

        with st.container(border=True):

            st.markdown("## أهلًا بكِ في عالم ميكو 🩵")

            st.write("""
            اختاري القسم الذي تريدين الدخول إليه،
            وابدئي رحلة جديدة من الإنجازات.
            """)

        st.write("")

        if st.button("📚  MY TASKS  ➜", use_container_width=True):
            go("tasks")

        if st.button("💬  ASK MIKU  ➜", use_container_width=True):
            go("chat")

        if st.button("🏆  ACHIEVEMENTS  ➜", use_container_width=True):
            go("achievements")

        if st.button("🎀  CUSTOMIZATION  ➜", use_container_width=True):
            go("customization")

    with right:

        empty_miku()

    footer()


# =========================================================
# TASKS
# =========================================================

elif st.session_state.page == "tasks":

    title("مهامي وواجباتي")

    with st.container(border=True):

        st.markdown("### ✨ كل مهمة تخلصينها هي إنجاز جديد!")

        st.write("أضيفي واجباتك واختاري المادة وموعد التسليم.")

    st.write("")

    with st.form("task_form", clear_on_submit=True):

        task_name = st.text_input("اسم المهمة")

        subject = st.selectbox(
            "المادة",
            SUBJECTS
        )

        due_date = st.date_input(
            "موعد التسليم",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "＋ إضافة المهمة 🩵",
            use_container_width=True
        )

        if submitted:

            if task_name.strip():

                st.session_state.tasks.append({
                    "name": task_name.strip(),
                    "subject": subject,
                    "due": str(due_date),
                    "done": False
                })

                st.success("تمت إضافة المهمة! 🩵")
                st.rerun()

            else:

                st.warning("اكتبي اسم المهمة أولًا.")

    st.divider()

    title("قائمة المهام")

    if not st.session_state.tasks:

        st.info("ما عندك مهام حاليًا. أضيفي أول مهمة!")

    else:

        for i, task in enumerate(st.session_state.tasks):

            with st.container(border=True):

                st.markdown(f"### 📘 {task['subject']}")
                st.write(task["name"])
                st.caption(f"📅 موعد التسليم: {task['due']}")

                checked = st.checkbox(
                    "تم الإنجاز ✨",
                    value=task["done"],
                    key=f"task_done_{i}"
                )

                if checked and not task["done"]:

                    task["done"] = True
                    st.session_state.xp += 25

                    st.success("أحسنتِ! حصلتِ على 25 XP 🩵")
                    st.rerun()

                elif not checked and task["done"]:

                    task["done"] = False
                    st.session_state.xp = max(
                        0,
                        st.session_state.xp - 25
                    )

                    st.rerun()

                if st.button("🗑 حذف المهمة", key=f"delete_{i}"):

                    if task["done"]:
                        st.session_state.xp = max(
                            0,
                            st.session_state.xp - 25
                        )

                    st.session_state.tasks.pop(i)
                    st.rerun()

    back_button()
    footer()


# =========================================================
# ASK MIKU
# =========================================================

elif st.session_state.page == "chat":

    title("اسألي ميكو")

    with st.container(border=True):

        st.markdown("## ميكو هنا لمساعدتك! 🩵")

        st.write("""
        اكتبي سؤالك الدراسي أو ما تريدين فهمه.
        """)

    st.write("")

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("اكتبي رسالتك إلى ميكو...")

    if user_message:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": (
                "وصلني سؤالك! 🩵 "
                "سنربط ميكو بالذكاء الاصطناعي في الخطوة التالية."
            )
        })

        st.rerun()

    if st.button("🗑 مسح المحادثة"):

        st.session_state.chat_history = []
        st.rerun()

    back_button()
    footer()


# =========================================================
# ACHIEVEMENTS
# =========================================================

elif st.session_state.page == "achievements":

    title("إنجازاتي")

    with st.container(border=True):

        st.markdown("## You're doing amazing! ♡")

        st.markdown(f"# ⭐ LEVEL {level()}")

        st.markdown(f"## 🩵 {st.session_state.xp} XP")

        st.write("استمري، كل خطوة صغيرة تصنع فرقًا كبيرًا.")

    st.write("")

    progress = (st.session_state.xp % 100) / 100

    st.progress(progress)

    st.caption(
        f"باقي {100 - (st.session_state.xp % 100)} XP للمستوى القادم!"
    )

    completed = sum(
        1 for task in st.session_state.tasks
        if task["done"]
    )

    total = len(st.session_state.tasks)

    with st.container(border=True):

        st.markdown("### 📚 المهام المكتملة")

        st.markdown(f"# {completed} / {total}")

    back_button()
    footer()


# =========================================================
# CUSTOMIZATION
# =========================================================

elif st.session_state.page == "customization":

    title("تغيير شكل ميكو")

    with st.container(border=True):

        st.markdown("## اختاري الستايل الذي تحبينه ♡")

        st.write("""
        مساحة ميكو جاهزة لإضافة المجسم ثلاثي الأبعاد لاحقًا.
        """)

    st.selectbox(
        "Miku Style",
        ["Original", "Cute", "Crystal", "Baby Pink"],
        key="miku_style"
    )

    empty_miku()

    back_button()
    footer()


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "settings":

    title("الإعدادات")

    with st.container(border=True):

        st.markdown("## Customize your world ♡")

        st.write("خصّصي تجربتك في عالم ميكو.")

    st.checkbox(
        "تفعيل المؤثرات الصوتية",
        key="sound"
    )

    st.selectbox(
        "لغة التطبيق",
        ["العربية", "English"],
        key="language"
    )

    st.selectbox(
        "لون الواجهة",
        ["Sky Blue", "Lavender", "Baby Pink"],
        key="theme"
    )

    if st.button("↩ العودة إلى صفحة البداية",
                 use_container_width=True):

        go("welcome")

    footer()
