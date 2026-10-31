import streamlit as st
import streamlit.components.v1 as components
import json
import os
import time
from datetime import datetime, date
import requests

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
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Tajawal:wght@400;500;700;800&display=swap');

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
    background: radial-gradient(ellipse at 10% 5%, #ffe4ef 0%, transparent 40%),
                radial-gradient(ellipse at 90% 80%, #f0e7ff 0%, transparent 40%),
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

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffe5f0, #fff6fa 55%, #f3ebff);
    border-right: 2px solid #f8d4e5;
}

section[data-testid="stSidebar"] * {
    color: #80566c;
}

section[data-testid="stSidebar"] button {
    border-radius: 16px !important;
}

.miku-header {
    text-align: center;
    padding: 27px 15px;
    margin-bottom: 24px;
    border-radius: 28px;
    background: rgba(255,255,255,0.78);
    border: 2px solid #f8d7e7;
    box-shadow: 0 10px 35px rgba(219,143,180,0.13);
}

.miku-header h1 {
    color: #dc83ac;
    font-family: 'Quicksand', sans-serif;
    font-size: clamp(26px, 5vw, 42px);
    font-weight: 700;
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

.miku-card {
    background: rgba(255,255,255,0.88);
    border: 1.5px solid #f7d5e5;
    border-radius: 24px;
    padding: 22px;
    margin: 10px 0;
    box-shadow: 0 7px 25px rgba(218,147,183,0.10);
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

.miku-stage {
    text-align: center;
    padding: 22px 10px;
    margin: 8px 0 18px;
    background: linear-gradient(145deg, rgba(255,255,255,.95), rgba(255,232,244,.85));
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

.stButton > button {
    background: linear-gradient(135deg, #f5b5d2, #e99fc2);
    color: white !important;
    border: 1px solid #efc0d7;
    border-radius: 16px;
    padding: 9px 16px;
    font-family: 'Tajawal', sans-serif;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(221,131,174,.14);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #eaa0c1, #d982aa);
    transform: translateY(-2px);
}

.small-label {
    color: #a47d96;
    font-size: 13px;
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
        <div style="color:#dba2c0; margin-top:12px;">♡ ୨୧ ♡  study with miku  ♡ ୨୧ ♡</div>
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
        <div style="font-size:23px;font-weight:800;color:#d982aa;">Study with Miku</div>
        <div style="font-size:13px;color:#ac8199;">your cute study companion ♡</div>
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
        <p style="margin:5px 0;color:#b27c9c;">{st.session_state.xp} XP</p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# 🏠 HOME
# ==================================================

if st.session_state.page == "الرئيسية":
    draw_header("Study with Miku", "a little progress every day ♡ كل يوم إنجاز جديد")
    draw_miku("أهلًااا! مستعدة نخلي يومنا مليان إنجازات؟ 🩷")

    total = len(st.session_state.tasks)
    finished = completed_count()
    remaining = total - finished

    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("كل المهام", total, "📚")
    with c2: stat_card("المهام المتبقية", remaining, "📝")
    with c3: stat_card("المهام المنجزة", finished, "🌸")
    with c4: stat_card("نقاط الخبرة", st.session_state.xp, "⭐")

    st.markdown('<div class="section-title">🎀 خطتك الدراسية</div>', unsafe_allow_html=True)
    if total:
        st.progress(finished / total)
        st.caption(f"أنجزتِ {finished} من {total} مهام.")
    else:
        st.info("أضيفي أول واجب لكِ، وميكو بتساعدك ترتبين يومك. 🌷")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("＋ إضافة واجب جديد", use_container_width=True):
            go_to("الواجبات")
            st.rerun()
    with col2:
        if st.button("⏰ ابدئي جلسة مذاكرة", use_container_width=True):
            go_to("المؤقت")
            st.rerun()

# ==================================================
# 📚 TASK MANAGER
# ==================================================

elif st.session_state.page == "الواجبات":
    draw_header("My Study Planner", "رتبي واجباتك بطريقة لطيفة 🎀")
    
    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("عنوان المهمة", placeholder="مثال: حل أسئلة الفيزياء")
        subject = st.selectbox("المادة", ["رياضيات", "فيزياء", "كيمياء", "أحياء", "لغة عربية", "لغة إنجليزية", "أخرى"])
        priority = st.selectbox("الأولوية", ["عالية", "متوسطة", "منخفضة"])
        due_date = st.date_input("موعد التسليم", value=None)
        
        if st.form_submit_button("🎀 حفظ المهمة", use_container_width=True):
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

    st.markdown('<div class="section-title">📖 قائمة المهام</div>', unsafe_allow_html=True)
    for task in st.session_state.tasks:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                if task["done"]:
                    st.markdown(f"~~{task['name']}~~ 🌸")
                else:
                    st.markdown(f"### 🎀 {task['name']}")
                st.caption(f"📚 {task['subject']} · الأولوية: {task['priority']}")
            with col2:
                if not task["done"] and st.button("✓ إنجاز", key="f_" + task["id"]):
                    task["done"] = True
                    st.session_state.xp += 25
                    save_data()
                    st.rerun()
                if st.button("🗑️ حذف", key="d_" + task["id"]):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                    save_data()
                    st.rerun()

# ==================================================
# 🤖 MIKU AI CHAT
# ==================================================

elif st.session_state.page == "ميكو الذكية":
    draw_header("Chat with Miku", "اسألي، تعلّمي، واكتشفي أشياء جديدة ♡")
    draw_miku("أنا هنا لمساعدتك في الدراسة! اسأليني أي سؤال. 🩷")

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("اكتبي سؤالك لميكو هنا... 🎀")

    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not api_key:
            reply = "يا هلا! 🎀 تأكدي من إضافة GEMINI_API_KEY في إعدادات Secrets."
        else:
            try:
                with st.spinner("ميكو تفكر في إجابتك... 🩷"):
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]} for m in st.session_state.chat_history[-12:]]
                    payload = {
                        "system_instruction": {"parts": [{"text": "أنت ميكو، مساعدة دراسية لطيفة تتحدث بالعربية بوضوح وتشجع الطالبة."}]},
                        "contents": contents
                    }
                    res = requests.post(url, json=payload, timeout=45)
                    if res.status_code == 200:
                        reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        reply = f"تعذّر الاتصال (رمز {res.status_code})."
            except Exception as e:
                reply = f"خطأ في الاتصال: {e}"

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        save_data()
        st.rerun()

    if st.button("🧹 مسح المحادثة"):
        st.session_state.chat_history = []
        save_data()
        st.rerun()

# ==================================================
# ⏰ STUDY TIMER
# ==================================================

elif st.session_state.page == "المؤقت":
    draw_header("Study Time", "خذي وقتك وحققي أهدافك ♡")
    draw_miku("كل دقيقة تقربك من هدفك! 🌷")
    
    if st.session_state.timer_running:
        remaining = max(0, int(st.session_state.timer_end - time.time()))
        mins, secs = divmod(remaining, 60)
        st.markdown(f"""
        <div class="miku-card" style="text-align:center;">
            <div style="font-size:55px;color:#d86e9e;font-weight:700;">{mins:02d}:{secs:02d}</div>
        </div>
        """, unsafe_allow_html=True)
        if remaining <= 0:
            st.session_state.timer_running = False
            st.session_state.sessions += 1
            st.session_state.xp += 10
            save_data()
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()
    else:
        with st.form("timer_form"):
            dur = st.number_input("المدة بالدقائق", 1, 180, 25)
            if st.form_submit_button("🎀 ابدئي المؤقت", use_container_width=True):
                st.session_state.timer_end = time.time() + int(dur * 60)
                st.session_state.timer_running = True
                st.rerun()

# ==================================================
# 🏆 ACHIEVEMENTS
# ==================================================

elif st.session_state.page == "الإنجازات":
    draw_header("My Achievements", "كل إنجاز صغير يستحق الاحتفال! 🎀")
    draw_miku("أنا فخورة بكِ جداً! 🩷")
    st.markdown(f"### المستوى: {xp_level()}  |  نقاط الخبرة: {st.session_state.xp} XP")
    st.progress((st.session_state.xp % 100) / 100)
