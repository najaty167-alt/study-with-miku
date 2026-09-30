import streamlit as st
import base64

# -------------------------
# Page settings
# -------------------------
st.set_page_config(
    page_title="Study with Miku 🩵",
    page_icon="🎀",
    layout="centered"
)

# -------------------------
# Data
# -------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

# -------------------------
# Miku image
# -------------------------
def get_miku_image():
    with open("miku.png", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


miku_image = get_miku_image()

# -------------------------
# Style
# -------------------------
st.markdown(
    """
    <style>
        .main {
            background-color: #f8fdff;
        }

        h1 {
            color: #39b9c8;
            text-align: center;
        }

        h2, h3 {
            color: #4aaeb8;
        }

        .miku-box {
            padding: 20px;
            border-radius: 25px;
            background: linear-gradient(135deg, #e8fbff, #ffffff);
            text-align: center;
            margin-bottom: 20px;
            border: 2px solid #c9f3f7;
        }

        .miku-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 10px 0 20px 0;
        }

        .miku {
            width: 320px;
            max-width: 85%;
            border-radius: 25px;
            animation: mikuFloat 3s ease-in-out infinite;
            filter: drop-shadow(0px 12px 20px rgba(0, 190, 220, 0.25));
        }

        @keyframes mikuFloat {
            0% {
                transform: translateY(0px) rotate(-1deg);
            }

            50% {
                transform: translateY(-12px) rotate(1deg);
            }

            100% {
                transform: translateY(0px) rotate(-1deg);
            }
        }

        .task-box {
            padding: 15px;
            border-radius: 18px;
            background-color: white;
            margin: 10px 0;
            border: 1px solid #d9f3f5;
        }

        .miku-message {
            text-align: center;
            color: #39aebd;
            font-size: 18px;
            font-weight: bold;
            margin: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Header
# -------------------------
st.markdown(
    """
    <div class="miku-box">
        <h1>🎀 Study with Miku 🩵</h1>
        <p>ذاكري معي وخلي إنجازاتك تكبر يومًا بعد يوم ✨</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Animated Miku
# -------------------------
st.markdown(
    f"""
    <div class="miku-container">
        <img
            class="miku"
            src="data:image/png;base64,{miku_image}"
        >
    </div>

    <div class="miku-message">
        🩵 هيا نذاكر معًا! 🎀
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# XP
# -------------------------
level = (st.session_state.xp // 100) + 1

st.subheader("🌱 تقدمك")

col1, col2 = st.columns(2)

with col1:
    st.metric("⭐ XP", st.session_state.xp)

with col2:
    st.metric("🎀 المستوى", level)

st.divider()

# -------------------------
# Add task
# -------------------------
st.subheader("📝 أضيفي مهمة")

task_name = st.text_input(
    "اسم المهمة",
    placeholder="مثال: حل واجب الفيزياء ص 29"
)

subject = st.selectbox(
    "المادة",
    [
        "📐 رياضيات",
        "⚗️ كيمياء",
        "🔬 فيزياء",
        "📚 عربي",
        "🇬🇧 إنجليزي",
        "☪️ إسلامية",
        "🌍 اجتماعيات",
        "🔬 علوم",
        "✨ أخرى"
    ]
)

if st.button("🎀 أضيفي المهمة"):
    if task_name.strip():
        st.session_state.tasks.append(
            {
                "name": task_name,
                "subject": subject,
                "done": False
            }
        )

        st.success("تمت إضافة المهمة! 🩵")
        st.rerun()

    else:
        st.warning("اكتبي اسم المهمة أولًا 🥹")

st.divider()

# -------------------------
# Tasks
# -------------------------
st.subheader("📚 مهامي اليوم")

if not st.session_state.tasks:

    st.info(
        "ما عندك مهام حاليًا ✨ "
        "أضيفي أول مهمة وابدئي مع ميكو! 🎀"
    )

else:

    for i, task in enumerate(st.session_state.tasks):

        if not task["done"]:

            st.markdown(
                f"""
                <div class="task-box">
                    <b>{task["subject"]}</b><br>
                    {task["name"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "✅ خلصت المهمة",
                key=f"done_{i}"
            ):

                st.session_state.tasks[i]["done"] = True
                st.session_state.xp += 20

                st.success(
                    "ميكو فخورة فيك! 🩵 +20 XP 🎀"
                )

                st.rerun()

# -------------------------
# Completed tasks
# -------------------------
completed = [
    task
    for task in st.session_state.tasks
    if task["done"]
]

if completed:

    st.divider()
    st.subheader("🏆 إنجازاتك")

    for task in completed:

        st.write(
            f"✅ {task['subject']} — {task['name']}"
        )

# -------------------------
# Footer
# -------------------------
st.divider()

st.caption(
    "🩵 Study with Miku — your cute study companion 🎀"
)
