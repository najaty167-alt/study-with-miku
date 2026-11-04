
import streamlit as st
from datetime import datetime

# ==========================================================
# MIKU WORLD | Study with Miku
# A cute anime-style study dashboard
# ==========================================================

st.set_page_config(
    page_title="Miku World",
    page_icon="🩵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "page": "welcome",
    "tasks": [],
    "xp": 0,
    "chat_history": [],
    "miku_style": "Original",
    "sound": True,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def navigate(page):
    st.session_state.page = page


# ==========================================================
# CSS DESIGN
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Tajawal:wght@400;500;600;700;800&display=swap');

:root {
    --aqua: #11d5df;
    --deep-aqua: #00b6c9;
    --white: #ffffff;
    --soft-blue: #e8fbff;
    --lavender: #e8dcff;
    --dark: #45677e;
}

html, body, [class*="css"] {
    font-family: 'Tajawal', 'Baloo 2', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 15%,
            rgba(220,255,255,.55), transparent 35%),
        radial-gradient(ellipse at 15% 80%,
            rgba(225,210,255,.35), transparent 40%),
        repeating-linear-gradient(
            135deg,
            #16c5d6 0px,
            #16c5d6 42px,
            #10b8cd 42px,
            #10b8cd 84px
        );
    color: var(--dark);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.1rem;
    padding-bottom: 2rem;
}

header, footer {
    visibility: hidden;
}

h1, h2, h3, h4 {
    font-family: 'Baloo 2', 'Tajawal', sans-serif !important;
    color: #45677e !important;
}

p {
    line-height: 1.8;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e8fbff, #e8ddff);
    border-right: 3px solid rgba(255,255,255,.7);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: #50728c !important;
}

/* ===================== */
/* GAME MENU BUTTONS     */
/* ===================== */

div.stButton > button {
    width: 100%;
    min-height: 70px;

    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f6fcff 48%,
        #e5f5fa 100%
    );

    color: #7a8794;
    border: 3px solid #ffffff;
    border-radius: 5px;

    font-family: 'Baloo 2', 'Tajawal', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;

    box-shadow:
        0 7px 0 #9aabb7,
        0 12px 20px rgba(30,90,120,.16),
        inset 0 2px 0 #ffffff;

    transition:
        transform .18s ease,
        background .18s ease,
        color .18s ease,
        box-shadow .18s ease;

    clip-path: polygon(
        0 0,
        94% 0,
        100% 50%,
        94% 100%,
        0 100%,
        3% 50%
    );
}

/* Hover animation */
div.stButton > button:hover {
    transform: scale(1.035);

    background: linear-gradient(
        180deg,
        #62f4f2,
        #08cbd8
    );

    color: #ffffff;

    box-shadow:
        0 0 12px rgba(220,255,255,.9),
        0 8px 0 #07899b,
        0 15px 25px rgba(0,90,120,.25);

    border-color: #ffffff;
}

/* Button press */
div.stButton > button:active {
    transform: scale(.985) translateY(3px);

    box-shadow:
        0 3px 0 #07899b,
        0 5px 12px rgba(0,90,120,.2);
}

/* General cards */
.glass-card {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.96),
        rgba(235,250,255,.88)
    );

    border: 3px solid rgba(255,255,255,.95);
    border-radius: 24px;

    padding: 25px;

    box-shadow:
        0 12px 0 rgba(105,174,197,.45),
        0 20px 35px rgba(35,100,130,.15),
        inset 0 2px 0 #ffffff;
}

/* Main title */
.game-title {
    color: #ffffff;
    font-family: 'Baloo 2', sans-serif;
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.1;

    text-shadow:
        0 4px 0 #0a98b5,
        0 8px 15px rgba(0,75,100,.25);
}

/* Subtitle */
.game-subtitle {
    color: #eaffff;
    font-size: 1.15rem;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0,90,120,.2);
}

/* Empty character stage */
.miku-stage {
    height: 560px;
    width: 100%;

    position: relative;
    overflow: hidden;

    border-radius: 28px;

    background:
        radial-gradient(
            circle at 50% 55%,
            rgba(255,255,255,.35),
            transparent 55%
        ),
        linear-gradient(
            145deg,
            rgba(235,255,255,.22),
            rgba(230,220,255,.18)
        );

    border: 3px solid rgba(255,255,255,.4);

    box-shadow:
        inset 0 0 35px rgba(255,255,255,.15),
        0 15px 35px rgba(0,90,120,.12);
}

/* Soft decorative stars */
.star-decoration {
    color: #ffffff;
    font-size: 2rem;
    opacity: .75;
}

/* Section header */
.section-heading {
    background: linear-gradient(180deg, #ffffff, #e7f8ff);
    border: 3px solid #ffffff;
    border-radius: 16px;

    padding: 15px 22px;

    color: #638097;
    font-family: 'Baloo 2', sans-serif;
    font-weight: 800;
    font-size: 1.65rem;

    box-shadow:
        0 6px 0 #9aabb7,
        0 10px 20px rgba(0,80,120,.12);
}

/* Small footer */
.miku-footer {
    margin-top: 25px;
    padding: 12px;

    text-align: center;

    color: #ffffff;
    font-family: 'Baloo 2', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;

    text-shadow: 0 2px 5px rgba(0,80,120,.2);
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div,
.stNumberInput input {
    border-radius: 14px !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,.88);
    border: 2px solid white;
    border-radius: 20px;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #76e9ee, #c7aaff);
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# SUBJECTS
# ==========================================================

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


# ==========================================================
# COMMON COMPONENTS
# ==========================================================

def show_empty_miku():
    """
    Empty character area.
    Miku's 3D model can be added here later.
    """

    st.markdown("""
    <div class="miku-stage">
        <div style="
            position:absolute;
            top:25px;
            left:35px;
            color:white;
            font-size:28px;
            opacity:.7;">
            ✦
        </div>

        <div style="
            position:absolute;
            bottom:35px;
            right:35px;
            color:white;
            font-size:32px;
            opacity:.7;">
            ♡
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_footer():
    st.markdown("""
    <div class="miku-footer">
        ୨୧ MIKU WORLD ♡ STUDY WITH SPARKLE ✦
    </div>
    """, unsafe_allow_html=True)


def show_back_button():
    if st.button("⬅ العودة إلى القائمة الرئيسية",
                 use_container_width=True):
        navigate("home")


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center;">
        <h1>୨୧ MIKU WORLD</h1>
        <p style="color:#7898b1;">
            Your little study universe 🩵
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🏠  الرئيسية", use_container_width=True):
        navigate("home")

    if st.button("📚  مهامي وواجباتي", use_container_width=True):
        navigate("tasks")

    if st.button("💬  اسألي ميكو", use_container_width=True):
        navigate("chat")

    if st.button("🏆  إنجازاتي", use_container_width=True):
        navigate("achievements")

    if st.button("🎀  تغيير شكل ميكو", use_container_width=True):
        navigate("change_miku")

    if st.button("⚙️  الإعدادات", use_container_width=True):
        navigate("settings")

    st.markdown("---")

    level = (st.session_state.xp // 100) + 1

    st.markdown(f"""
    <div style="
        background:rgba(255,255,255,.75);
        padding:15px;
        border-radius:18px;
        text-align:center;
        border:2px solid white;">
        <h3>⭐ Level {level}</h3>
        <p>🩵 {st.session_state.xp} XP</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# WELCOME PAGE
# ==========================================================

if st.session_state.page == "welcome":

    left, right = st.columns([1.1, 1], gap="large")

    with left:

        st.markdown("""
        <div style="padding:25px 10px 20px 10px;">

            <div class="game-title">
                MIKU<br>WORLD
            </div>

            <div class="game-subtitle">
                ✦ Your magical study adventure ✦
            </div>

            <br>

            <div class="glass-card">

                <h2>Welcome to Miku World ♡</h2>

                <p style="
                    color:#718ba0;
                    font-size:1.15rem;
                    line-height:2;">
                    عالمك الصغير للدراسة والإنجاز والإبداع.<br>
                    كل خطوة تخطينها هنا تقرّبك من هدفك…<br>
                    وميكو معك في كل لحظة! 🩵
                </p>

                <h3>Ready to begin your journey?</h3>

            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button("✦  ENTER APP  ✦",
                     use_container_width=True):
            navigate("home")

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🏆 ACHIEVEMENTS",
                         use_container_width=True):
                navigate("achievements")

        with col2:
            if st.button("⚙️ SETTINGS",
                         use_container_width=True):
                navigate("settings")

        if st.button("🎀 CHANGE MIKU",
                     use_container_width=True):
            navigate("change_miku")

    with right:

        show_empty_miku()

    show_footer()


# ==========================================================
# HOME PAGE
# ==========================================================

elif st.session_state.page == "home":

    left, right = st.columns([1.1, 1], gap="large")

    with left:

        st.markdown("""
        <div style="padding:15px 5px;">

            <div class="game-title">
                HELLO,<br>STUDY STAR! ♡
            </div>

            <div class="game-subtitle">
                ✦ Let's make today magical ✦
            </div>

            <br>

            <div class="glass-card">
                <h2>أهلًا بكِ في عالم ميكو 🩵</h2>

                <p style="color:#718ba0;font-size:1.1rem;">
                    اختاري القسم الذي تريدين الدخول إليه،
                    وابدئي رحلة جديدة من الإنجازات.
                </p>
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button("📚  MY TASKS", use_container_width=True):
            navigate("tasks")

        if st.button("💬  ASK MIKU", use_container_width=True):
            navigate("chat")

        if st.button("🏆  ACHIEVEMENTS", use_container_width=True):
            navigate("achievements")

        if st.button("🎀  CUSTOMIZATION", use_container_width=True):
            navigate("change_miku")

    with right:

        show_empty_miku()

    show_footer()


# ==========================================================
# TASKS PAGE
# ==========================================================

elif st.session_state.page == "tasks":

    st.markdown("""
    <div class="section-heading">
        📚 مهامي وواجباتي
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="glass-card">
        <h3>كل مهمة تخلصينها هي إنجاز جديد! ✨</h3>
        <p style="color:#718ba0;">
            أضيفي واجباتك، واختاري المادة، ثم تابعي إنجازاتك.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    with st.form("add_task_form", clear_on_submit=True):

        task_name = st.text_input("اسم المهمة")

        subject = st.selectbox(
            "المادة",
            SUBJECTS
        )

        due_date = st.date_input(
            "موعد التسليم",
            value=datetime.today()
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

                st.success("تمت إضافة المهمة بنجاح! 🩵")
                st.rerun()

            else:

                st.warning("اكتبي اسم المهمة أولًا.")

    st.write("---")
    st.markdown("### ✦ قائمة المهام")

    if not st.session_state.tasks:

        st.info("ما عندك مهام حاليًا، أضيفي أول مهمة!")

    else:

        for i, task in enumerate(st.session_state.tasks):

            st.markdown(f"""
            <div class="glass-card" style="padding:15px;margin-bottom:10px;">
                <h4>{task['subject']}</h4>
                <p>{task['name']}</p>
                <small>📅 {task['due']}</small>
            </div>
            """, unsafe_allow_html=True)

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

            if st.button(
                "🗑 حذف المهمة",
                key=f"delete_task_{i}"
            ):

                if task["done"]:
                    st.session_state.xp = max(
                        0,
                        st.session_state.xp - 25
                    )

                st.session_state.tasks.pop(i)
                st.rerun()

    show_back_button()
    show_footer()


# ==========================================================
# CHAT PAGE
# ==========================================================

elif st.session_state.page == "chat":

    st.markdown("""
    <div class="section-heading">
        💬 اسألي ميكو
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="glass-card">
        <h2>ميكو هنا لمساعدتك! 🩵</h2>
        <p style="color:#718ba0;">
            اسألي عن دروسك أو اكتبي ما تريدين فهمه.
        </p>
    </div>
    """, unsafe_allow_html=True)

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
                "ربط الذكاء الاصطناعي يحتاج إعداد مفتاح Gemini."
            )
        })

        st.rerun()

    if st.button("🗑 مسح المحادثة"):
        st.session_state.chat_history = []
        st.rerun()

    show_back_button()
    show_footer()


# ==========================================================
# ACHIEVEMENTS PAGE
# ==========================================================

elif st.session_state.page == "achievements":

    st.markdown("""
    <div class="section-heading">
        🏆 إنجازاتي
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    level = (st.session_state.xp // 100) + 1
    progress = (st.session_state.xp % 100) / 100

    st.markdown(f"""
    <div class="glass-card">
        <h2>You're doing amazing! ♡</h2>

        <h1 style="font-size:3rem;">
            ⭐ LEVEL {level}
        </h1>

        <h2>
            🩵 {st.session_state.xp} XP
        </h2>

        <p style="color:#718ba0;">
            استمري، كل خطوة صغيرة تصنع فرقًا كبيرًا.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.progress(progress)

    st.caption(
        f"باقي {100 - (st.session_state.xp % 100)} XP للمستوى القادم!"
    )

    st.write("")

    completed = sum(
        1 for task in st.session_state.tasks
        if task["done"]
    )

    total = len(st.session_state.tasks)

    st.markdown(f"""
    <div class="glass-card">
        <h3>📚 المهام المكتملة</h3>
        <h1>{completed} / {total}</h1>
    </div>
    """, unsafe_allow_html=True)

    show_back_button()
    show_footer()


# ==========================================================
# CHANGE MIKU PAGE
# ==========================================================

elif st.session_state.page == "change_miku":

    st.markdown("""
    <div class="section-heading">
        🎀 تغيير شكل ميكو
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="glass-card">
        <h2>اختاري الستايل الذي تحبينه ♡</h2>
        <p style="color:#718ba0;">
            مساحة ميكو جاهزة لإضافة المجسّم ثلاثي الأبعاد لاحقًا.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.selectbox(
        "Miku Style",
        ["Original", "Cute", "Crystal", "Baby Pink"],
        key="miku_style"
    )

    show_empty_miku()

    show_back_button()
    show_footer()


# ==========================================================
# SETTINGS PAGE
# ==========================================================

elif st.session_state.page == "settings":

    st.markdown("""
    <div class="section-heading">
        ⚙️ الإعدادات
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="glass-card">
        <h2>Customize your world ♡</h2>
        <p style="color:#718ba0;">
            خصّصي تجربتك في عالم ميكو.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.checkbox(
        "تفعيل المؤثرات الصوتية",
        key="sound"
    )

    st.selectbox(
        "لغة التطبيق",
        ["العربية", "English"]
    )

    st.selectbox(
        "لون الواجهة",
        ["Sky Blue", "Lavender", "Baby Pink"]
    )

    if st.button("↩ العودة إلى صفحة البداية",
                 use_container_width=True):
        navigate("welcome")

    show_footer()


# ==========================================================
# OTHER MENU ITEMS
# ==========================================================

else:

    st.markdown("""
    <div class="section-heading">
        🩵 Miku World
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h2>هذه الصفحة جاهزة للتطوير ✨</h2>
        <p style="color:#718ba0;">
            سنضيف محتواها لاحقًا.
        </p>
    </div>
    """, unsafe_allow_html=True)

    show_back_button()
    show_footer()
