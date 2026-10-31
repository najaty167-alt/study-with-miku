import streamlit as st
import streamlit.components.v1 as components
import json
import os
import time
from datetime import datetime, date

# ==================================================
# 🎀 STUDY WITH MIKU — BABY PINK EDITION
# ==================================================

st.set_page_config(
    page_title="Study with Miku 🎀",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "miku_data.json"

# ==================================================
# 🩷 SAVE AND LOAD DATA
# ==================================================

def load_data():
    default = {
        "tasks": [],
        "xp": 0,
        "sessions": 0,
        "chat_history": []
    }

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            default.update(saved)
        except (json.JSONDecodeError, OSError):
            pass

    return default


def save_data():
    data = {
        "tasks": st.session_state.tasks,
        "xp": st.session_state.xp,
        "sessions": st.session_state.sessions,
        "chat_history": st.session_state.chat_history
    }

    temporary_file = DATA_FILE + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    os.replace(temporary_file, DATA_FILE)


if "initialized" not in st.session_state:
    data = load_data()

    st.session_state.tasks = data["tasks"]
    st.session_state.xp = data["xp"]
    st.session_state.sessions = data["sessions"]
    st.session_state.chat_history = data["chat_history"]

    st.session_state.initialized = True

if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "timer_end" not in st.session_state:
    st.session_state.timer_end = None

if "timer_mode" not in st.session_state:
    st.session_state.timer_mode = "مذاكرة"

if "timer_message" not in st.session_state:
    st.session_state.timer_message = ""

if "timer_completed" not in st.session_state:
    st.session_state.timer_completed = False


# ==================================================
# 🎀 PINK DESIGN SYSTEM
# ==================================================

st.markdown("""
<style>
@import url(
'https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Tajawal:wght@400;500;700;800&display=swap'
);

:root {
    --pink: #f3a8ca;
    --dark-pink: #d96e9d;
    --light-pink: #fff0f6;
    --baby-pink: #ffe0ed;
    --white: #fffdfd;
    --text: #765466;
    --lavender: #f2eaff;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 5%,
            #ffe4ef 0%, transparent 40%),
        radial-gradient(ellipse at 90% 80%,
            #f0e7ff 0%, transparent 40%),
        #fffafd;

    color: var(--text);
    font-family: 'Tajawal', sans-serif;
}

html, body, [class*="css"] {
    font-family: 'Tajawal', sans-serif;
}

header[data-testid="stHeader"] {
    background: rgba(255,250,253,0.75);
}

footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffe5f0,
        #fff6fa 55%,
        #f3ebff
    );
    border-right: 2px solid #f8d4e5;
}

section[data-testid="stSidebar"] * {
    color: #80566c;
}

section[data-testid="stSidebar"] button {
    border-radius: 16px !important;
}

/* Main heading */

.miku-header {
    text-align: center;
    padding: 27px 15px;
    margin-bottom: 24px;
    border-radius: 28px;
    background: rgba(255,255,255,0.78);
    border: 2px solid #f8d7e7;
    box-shadow: 0 10px 35px rgba(219,143,180,0.13);
    position: relative;
    overflow: hidden;
}

.miku-header h1 {
    color: #dc83ac;
    font-family: 'Quicksand', sans-serif;
    font-size: clamp(26px, 5vw, 42px);
    font-weight: 700;
    letter-spacing: 1px;
    margin: 0;
}

.miku-header p {
    color: #a8809a;
    margin-top: 8px;
    font-size: 16px;
}

.ribbon {
    color: #e6a0c1;
    font-size: 24px;
    letter-spacing: 8px;
}

/* Cute cards */

.miku-card {
    background: rgba(255,255,255,0.88);
    border: 1.5px solid #f7d5e5;
    border-radius: 24px;
    padding: 22px;
    margin: 10px 0;
    box-shadow: 0 7px 25px rgba(218,147,183,0.10);
    backdrop-filter: blur(12px);
}

.stat-card {
    background: linear-gradient(140deg, #fff, #fff0f7);
    border: 1.5px solid #f6d5e6;
    border-radius: 22px;
    padding: 19px 10px;
    text-align: center;
    min-height: 112px;
    box-shadow: 0 5px 18px rgba(220,145,184,0.10);
}

.stat-number {
    color: #d86e9e;
    font-family: 'Quicksand', sans-serif;
    font-size: 29px;
    font-weight: 700;
}

.stat-label {
    color: #99748b;
    font-size: 14px;
}

.section-title {
    color: #c86e9a;
    font-size: 23px;
    font-weight: 800;
    margin: 24px 0 12px;
}

.soft-note {
    background: #fff0f7;
    padding: 13px 16px;
    border-radius: 17px;
    border: 1px dashed #e9a8c7;
    color: #97627f;
    margin: 12px 0;
}

/* Miku character */

.miku-stage {
    text-align: center;
    padding: 22px 10px;
    margin: 8px 0 18px;
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.95),
        rgba(255,232,244,.85)
    );
    border: 2px solid #f8d8e8;
    border-radius: 30px;
    box-shadow: 0 12px 30px rgba(214,133,172,.15);
}

.miku-character {
    display: inline-block;
    font-size: 95px;
    animation: floaty 3s ease-in-out infinite;
    filter: drop-shadow(0 10px 7px rgba(220,140,180,.18));
}

@keyframes floaty {
    0%,100% { transform: translateY(0) rotate(-2deg); }
    50% { transform: translateY(-10px) rotate(2deg); }
}

.speech {
    display: inline-block;
    background: white;
    border: 1.5px solid #f3c7dc;
    border-radius: 20px;
    padding: 10px 18px;
    color: #bc6d94;
    margin-top: 12px;
}

/* Buttons */

.stButton > button {
    background: linear-gradient(135deg, #f5b5d2, #e99fc2);
    color: white !important;
    border: 1px solid #efc0d7;
    border-radius: 16px;
    padding: 9px 16px;
    font-family: 'Tajawal', sans-serif;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(221,131,174,.14);
    transition: .2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #eaa0c1, #d982aa);
    border-color: #df94b6;
    transform: translateY(-2px);
}

/* Inputs */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input {
    background: #fff !important;
    color: #765466 !important;
    border: 1.5px solid #f0cede !important;
    border-radius: 14px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: white;
    border-color: #f0cede;
    border-radius: 14px;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #f5b5d2, #d98eb5);
}

hr {
    border-color: #f4dbe7;
}

.task-done {
    color: #9d91a0;
    text-decoration: line-through;
}

.small-label {
    color: #a47d96;
    font-size: 13px;
}

[data-testid="stChatMessage"] {
    background: rgba(255,240,247,.72);
    border: 1px solid #f6d9e8;
    border-radius: 18px;
}

@media (max-width: 640px) {
    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    .miku-character {
        font-size: 75px;
    }

    .miku-card {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 🩷 HELPERS
# ==================================================

def go_to(page):
    st.session_state.page = page


def xp_level():
    return st.session_state.xp // 100 + 1


def completed_count():
    return sum(1 for t in st.session_state.tasks if t["done"])


def draw_header(title, subtitle):
    st.markdown(f"""
    <div class="miku-header">
        <div class="ribbon">୨୧ ♡ 🎀 ♡ ୨୧</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def draw_miku(message="هيي! خلينا نذاكر مع بعض! 🎀"):
    st.markdown(f"""
    <div class="miku-stage">
        <div class="miku-character">🎀🐰</div>
        <div class="speech">{message}</div>
        <div style="color:#dba2c0; margin-top:12px;">
            ♡ ୨୧ ♡  study with miku  ♡ ୨୧ ♡
        </div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label, number, emoji):
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size:24px">{emoji}</div>
        <div class="stat-number">{number}</div>
        <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# 🎀 SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:15px 0 20px;">
        <div style="font-size:60px;">🎀🐰</div>
        <div style="font-size:23px;font-weight:800;color:#d982aa;">
            Study with Miku
        </div>
        <div style="font-size:13px;color:#ac8199;">
            your cute study companion ♡
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    pages = {
        "🏠 الرئيسية": "الرئيسية",
        "📚 واجباتي": "الواجبات",
        "🤖 اسألي ميكو": "ميكو الذكية",
        "⏰ جلسة المذاكرة": "المؤقت",
        "🏆 إنجازاتي": "الإنجازات"
    }

    for label, page_name in pages.items():
        if st.button(label, key="nav_" + page_name, use_container_width=True):
            go_to(page_name)
            st.rerun()

    st.markdown("---")

    st.markdown(f"""
    <div class="miku-card" style="text-align:center;padding:15px;">
        <div style="font-size:30px;">👑</div>
        <b>Level {xp_level()}</b>
        <p style="margin:5px 0;color:#b27c9c;">
            {st.session_state.xp} XP
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Made with ♡ and lots of pink 🎀")


# ==================================================
# 🏠 HOME
# ==================================================

if st.session_state.page == "الرئيسية":

    draw_header(
        "Study with Miku",
        "a little progress every day ♡ كل يوم إنجاز جديد"
    )

    draw_miku("أهلًااا! مستعدة نخلي يومنا مليان إنجازات؟ 🩷")

    total = len(st.session_state.tasks)
    finished = completed_count()
    remaining = total - finished

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        stat_card("كل المهام", total, "📚")
    with c2:
        stat_card("المهام المتبقية", remaining, "📝")
    with c3:
        stat_card("المهام المنجزة", finished, "🌸")
    with c4:
        stat_card("نقاط الخبرة", st.session_state.xp, "⭐")

    st.markdown(
        '<div class="section-title">🎀 خطتك الدراسية</div>',
        unsafe_allow_html=True
    )

    if total:
        progress = finished / total
        st.progress(progress)
        st.caption(f"أنجزتِ {finished} من {total} مهام.")

    else:
        st.markdown("""
        <div class="miku-card" style="text-align:center;">
            <div style="font-size:40px;">🌷📖🌷</div>
            <h3 style="color:#d982aa;">خطوتك الأولى تبدأ هنا!</h3>
            <p>أضيفي أول واجب لكِ، وميكو بتساعدك ترتبين يومك.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("＋ إضافة واجب جديد", use_container_width=True):
            go_to("الواجبات")
            st.rerun()

    with col2:
        if st.button("⏰ ابدئي جلسة مذاكرة", use_container_width=True):
            go_to("المؤقت")
            st.rerun()

    st.markdown(
        '<div class="section-title">♡ مهامي القادمة</div>',
        unsafe_allow_html=True
    )

    upcoming = [t for t in st.session_state.tasks if not t["done"]]

    upcoming.sort(
        key=lambda t: (
            t.get("due", "9999-12-31"),
            {"عالية": 0, "متوسطة": 1, "منخفضة": 2}.get(
                t.get("priority", "متوسطة"), 1
            )
        )
    )

    if upcoming:
        for task in upcoming[:5]:
            due = task.get("due", "")
            due_text = f" · 📅 {due}" if due else ""

            st.markdown(
                f"""
                <div class="miku-card">
                    <b>🎀 {task['name']}</b><br>
                    <span class="small-label">
                        {task['subject']} · الأولوية: {task['priority']}
                        {due_text}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("ما عندك مهام معلقة! أضيفي واجبًا جديدًا وقت ما تحتاجين. 🌸")


# ==================================================
# 📚 TASK MANAGER
# ==================================================

elif st.session_state.page == "الواجبات":

    draw_header("My Study Planner", "رتبي واجباتك بطريقة لطيفة 🎀")

    st.markdown(
        '<div class="section-title">♡ إضافة مهمة جديدة</div>',
        unsafe_allow_html=True
    )

    with st.form("add_task_form", clear_on_submit=True):

        task_name = st.text_input(
            "عنوان المهمة",
            placeholder="مثال: حل أسئلة الفيزياء"
        )

        subjects = [
            "رياضيات",
            "فيزياء",
            "كيمياء",
            "أحياء",
            "لغة عربية",
            "لغة إنجليزية",
            "دراسات اجتماعية",
            "تربية إسلامية",
            "أخرى"
        ]

        subject = st.selectbox("المادة الدراسية", subjects)

        priority = st.selectbox(
            "الأولوية",
            ["عالية", "متوسطة", "منخفضة"]
        )

        due_date = st.date_input(
            "موعد التسليم (اختياري)",
            value=None
        )

        submitted = st.form_submit_button(
            "🎀 حفظ المهمة",
            use_container_width=True
        )

        if submitted:
            if task_name.strip():

                st.session_state.tasks.append({
                    "id": str(time.time_ns()),
                    "name": task_name.strip(),
                    "subject": subject,
                    "priority": priority,
                    "due": due_date.isoformat() if due_date else "",
                    "done": False
                })

                save_data()
                st.success("انضافت المهمة بنجاح! 🌸")
                st.rerun()

            else:
                st.warning("اكتبي عنوان المهمة أولًا يا مجتهدة! 🩷")

    st.markdown("---")

    filter_option = st.radio(
        "عرض المهام",
        ["الكل", "غير المنجزة", "المنجزة"],
        horizontal=True
    )

    filtered_tasks = []

    for task in st.session_state.tasks:
        if filter_option == "غير المنجزة" and task["done"]:
            continue

        if filter_option == "المنجزة" and not task["done"]:
            continue

        filtered_tasks.append(task)

    priority_order = {"عالية": 0, "متوسطة": 1, "منخفضة": 2}

    filtered_tasks.sort(
        key=lambda t: (
            t["done"],
            priority_order.get(t.get("priority", "متوسطة"), 1),
            t.get("due") or "9999-12-31"
        )
    )

    st.markdown(
        '<div class="section-title">📖 قائمة المهام</div>',
        unsafe_allow_html=True
    )

    if not filtered_tasks:
        st.info("ما فيه مهام في هذه القائمة حاليًا. 🎀")

    for task in filtered_tasks:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                if task["done"]:
                    st.markdown(
                        f"~~{task['name']}~~  🌸",
                        unsafe_allow_html=False
                    )
                else:
                    st.markdown(f"### 🎀 {task['name']}")

                st.caption(
                    f"📚 {task['subject']}  ·  "
                    f"الأولوية: {task['priority']}"
                )

                if task.get("due"):
                    st.caption(f"📅 التسليم: {task['due']}")

                if task.get("due") and not task["done"]:
                    try:
                        due = date.fromisoformat(task["due"])
                        days_left = (due - date.today()).days

                        if days_left < 0:
                            st.warning("تجاوز موعد التسليم.")
                        elif days_left == 0:
                            st.warning("موعد التسليم اليوم! 🩷")
                        elif days_left <= 2:
                            st.info(f"باقي {days_left} يوم/أيام.")
                    except ValueError:
                        pass

            with col2:
                if not task["done"]:
                    if st.button("✓ إنجاز", key="finish_" + task["id"]):
                        task["done"] = True
                        st.session_state.xp += 25
                        save_data()
                        st.success("+25 XP 🎉")
                        st.rerun()

                else:
                    st.markdown("🩷 منجزة!")

                if st.button("🗑️ حذف", key="delete_" + task["id"]):
                    st.session_state.tasks = [
                        t for t in st.session_state.tasks
                        if t["id"] != task["id"]
                    ]
                    save_data()
                    st.rerun()


# ==================================================
# 🤖 MIKU AI CHAT (FIXED & CONNECTED)
# ==================================================

elif st.session_state.page == "ميكو الذكية":

    draw_header("Chat with Miku", "اسألي، تعلّمي، واكتشفي أشياء جديدة ♡")

    draw_miku("أنا هنا لمساعدتك في الدراسة! اسأليني أي سؤال دراسي. 🩷")

    st.markdown("""
    <div class="soft-note">
        🎀 يمكنكِ سؤال ميكو عن شرح الدروس، والمسائل، والقواعد،
        والمراجعة. المفتاح الخاص بكِ متصل وجاهز!
    </div>
    """, unsafe_allow_html=True)

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("اكتبي سؤالك لميكو هنا... 🎀")

    if prompt:

        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        if not api_key:
            reply = (
                "يا هلا! 🎀 وصلتني رسالتك، لكن الذكاء الاصطناعي "
                "ما تفعّل بعد. أضيفي GEMINI_API_KEY إلى Secrets "
                "حتى أقدر أجيبك باستخدام Gemini."
            )

        else:
            try:
                import requests

                with st.spinner("ميكو تفكر في إجابتك... 🩷"):

                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

                    contents = []

                    for message in st.session_state.chat_history[-12:]:
                        contents.append({
                            "role": (
                                "model"
                                if message["role"] == "assistant"
                                else "user"
                            ),
                            "parts": [{"text": message["content"]}]
                        })

                    payload = {
                        "system_instruction": {
                            "parts": [{
                                "text": (
                                    "أنت ميكو، مساعدة دراسية لطيفة "
                                    "تتحدث باللغة العربية بوضوح. "
                                    "اشرحي للطالبات بأسلوب مشجع "
                                    "ومناسب لمستواهن الدراسي. "
                                    "في المسائل الحسابية، اشرحي "
                                    "الخطوات بترتيب واضح."
                                )
                            }]
                        },
                        "contents": contents,
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 1800
                        }
                    }

                    response = requests.post(
                        url,
                        json=payload,
                        timeout=45
                    )

                    if response.status_code == 200:
                        result = response.json()
                        reply = result["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        reply = f"تعذّر الاتصال بميكو حالياً (رمز {response.status_code}). تأكدي من المفتاح."

            except Exception as e:
                reply = f"صار خطأ أثناء الاتصال: {e}"

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": reply
        })

        save_data()
        st.rerun()

    if st.button("🧹 مسح سجل المحادثة"):
        st.session_state.chat_history = []
        save_data()
        st.rerun()


# ==================================================
# ⏰ STUDY TIMER
# ==================================================

elif st.session_state.page == "المؤقت":

    draw_header("Study Time", "خذي وقتك، وحققي أهدافك خطوة بخطوة ♡")

    draw_miku("كل دقيقة تذاكرينها تقرّبك من هدفك! 🌷")

    st.markdown(
        '<div class="section-title">⏰ جلسة المذاكرة</div>',
        unsafe_allow_html=True
    )

    if st.session_state.timer_running:

        remaining = max(
            0,
            int(st.session_state.timer_end - time.time())
        )

        minutes, seconds = divmod(remaining, 60)

        st.markdown(f"""
        <div class="miku-card" style="text-align:center;">
            <div style="font-size:22px;color:#d982aa;">
                {"📚 وقت المذاكرة" if st.session_state.timer_mode == "مذاكرة" else "☕ وقت الاستراحة"}
            </div>
            <div style="
                font-family:Quicksand,sans-serif;
                font-size:clamp(50px,10vw,85px);
                color:#d86e9e;
                font-weight:700;
                margin:15px 0;">
                {minutes:02d}:{seconds:02d}
            </div>
            <div style="color:#a8809a;">୨୧ ♡ خذي نفسًا عميقًا ♡ ୨୧</div>
        </div>
        """, unsafe_allow_html=True)

        if remaining <= 0:
            st.session_state.timer_running = False

            if st.session_state.timer_mode == "مذاكرة":
                st.session_state.sessions += 1
                st.session_state.xp += 10
                st.session_state.timer_message = (
                    "أحسنتِ! انتهت جلسة المذاكرة، وحصلتِ على 10 XP! 🎉"
                )
            else:
                st.session_state.timer_message = (
                    "انتهت الاستراحة! أنتِ مستعدة للعودة للدراسة. 🩷"
                )

            st.session_state.timer_completed = True
            save_data()
            st.rerun()

        else:
            col1, col2 = st.columns(2)

            with col1:
                if st.button("⏹️ إيقاف المؤقت", use_container_width=True):
                    st.session_state.timer_running = False
                    st.session_state.timer_message = "أُوقفت الجلسة."
                    st.rerun()

            with col2:
                if st.button("🔄 إعادة الجلسة", use_container_width=True):
                    st.session_state.timer_running = False
                    st.session_state.timer_end = None
                    st.rerun()

            # تحديث العرض كل ثانية
            time.sleep(1)
            st.rerun()

    else:

        if st.session_state.timer_message:
            st.success(st.session_state.timer_message)

        with st.form("timer_form"):

            mode = st.selectbox(
                "نوع الجلسة",
                ["مذاكرة", "استراحة"]
            )

            duration = st.number_input(
                "المدة بالدقائق",
                min_value=1,
                max_value=180,
                value=25 if mode == "مذاكرة" else 5,
                step=5
            )

            start = st.form_submit_button(
                "🎀 ابدئي المؤقت",
                use_container_width=True
            )

            if start:
                st.session_state.timer_mode = mode
                st.session_state.timer_end = (
                    time.time() + int(duration * 60)
                )
                st.session_state.timer_running = True
                st.session_state.timer_message = ""
                st.session_state.timer_completed = False
                st.rerun()

        st.markdown("""
        <div class="miku-card" style="text-align:center;">
            <div style="font-size:36px;">🍓 📖 ☕</div>
            <h3 style="color:#d982aa;">نصيحة ميكو</h3>
            <p>جرّبي 25 دقيقة مذاكرة، ثم 5 دقائق استراحة.</p>
            <p style="color:#b58ba3;">تقدرين تغيرين المدة حسب احتياجك.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        f"### 🌸 الجلسات المكتملة: {st.session_state.sessions}"
    )
    st.markdown(
        f"### ⭐ نقاط الخبرة: {st.session_state.xp} XP"
    )


# ==================================================
# 🏆 ACHIEVEMENTS
# ==================================================

elif st.session_state.page == "الإنجازات":

    draw_header("My Achievements", "كل إنجاز صغير يستحق الاحتفال! 🎀")

    draw_miku("أنا فخورة بكل خطوة تتقدمين فيها! 🩷")

    xp = st.session_state.xp
    level = xp_level()
    current_level_xp = xp % 100

    c1, c2, c3 = st.columns(3)

    with c1:
        stat_card("المستوى", level, "👑")
    with c2:
        stat_card("نقاط الخبرة", xp, "⭐")
    with c3:
        stat_card("جلسات المذاكرة", st.session_state.sessions, "📚")

    st.markdown(
        '<div class="section-title">🌷 تقدم المستوى</div>',
        unsafe_allow_html=True
    )

    st.progress(current_level_xp / 100)

    st.caption(
        f"جمعتِ {current_level_xp} من 100 نقطة للمستوى التالي."
    )

    st.markdown(
        '<div class="section-title">🎀 أوسمتي</div>',
        unsafe_allow_html=True
    )

    badges = [
        (
            "🌱",
            "البداية الجميلة",
            "أضيفي أول مهمة دراسية.",
            len(st.session_state.tasks) >= 1
        ),
        (
            "🌸",
            "إنجاز أول",
            "أكملي أول واجب.",
            completed_count() >= 1
        ),
        (
            "⭐",
            "عشرون دقيقة من الجهد",
            "اجمعي 10 نقاط خبرة.",
            xp >= 10
        ),
        (
            "👑",
            "نجمة الدراسة",
            "اجمعي 100 نقطة خبرة.",
            xp >= 100
        ),
        (
            "📚",
            "قارئة مجتهدة",
            "أكملي خمس مهام.",
            completed_count() >= 5
        ),
        (
            "⏰",
            "صديقة الوقت",
            "أكملي ثلاث جلسات مذاكرة.",
            st.session_state.sessions >= 3
        )
    ]

    for emoji, title, description, unlocked in badges:
        with st.container(border=True):
            c1, c2 = st.columns([1, 5])

            with c1:
                st.markdown(
                    f"<div style='font-size:35px;text-align:center;'>"
                    f"{emoji if unlocked else '🔒'}</div>",
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(f"**{title}**")
                st.caption(description)

                if unlocked:
                    st.success("تم فتح الوسام! 🎉")
                else:
                    st.caption("واصلي التقدم لفتح هذا الوسام.")

    st.markdown("---")

    if st.button("🎀 العودة للرئيسية", use_container_width=True):
        go_to("الرئيسية")
        st.rerun()


# ==================================================
# 🌸 FOOTER
# ==================================================

st.markdown("""
<br>
<div style="
    text-align:center;
    color:#c69ab2;
    padding:20px 5px;
    font-size:14px;">
    ୨୧ ♡  Study with Miku  ♡ ୨୧
    <br>
    made for your little study journey 🎀
    <br><br>
    ✿ take it one step at a time ✿
</div>
""", unsafe_allow_html=True)
