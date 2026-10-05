import streamlit as st
import streamlit.components.v1 as components
import requests
import base64
import os

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Study with Miku — Raison d'être",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE MANAGEMENT
# =========================================================
if "screen" not in st.session_state:
    st.session_state.screen = "MENU"
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================================================
# LOAD LOCAL BACKGROUND IMAGE (bg.png)
# =========================================================
def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# البحث عن ملف الخلفية المحلي
bg_base64 = get_base64_image("bg.png") or get_base64_image("bg.jpg")

if bg_base64:
    bg_css_url = f"data:image/png;base64,{bg_base64}"
else:
    # رابط احتياطي في حال عدم إيجاد الملف المحلي بعد
    bg_css_url = ""

# =========================================================
# CUSTOM CSS FOR EXACT MATCH
# =========================================================
css_code = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Tajawal:wght@400;700&display=swap');

/* Fullscreen Background Image */
.stApp {
    background: url('BACKGROUND_URL_PLACEHOLDER') center center / cover no-repeat fixed !important;
    color: #d1f4ff;
    font-family: 'Tajawal', sans-serif;
}

/* Hide Streamlit Header & Footer */
header, footer { visibility: hidden; }

/* Remove block padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 0rem !important;
}

/* Title Styling */
.vn-title-container {
    text-align: center;
    margin-top: 20px;
    margin-bottom: 25px;
}

.vn-title {
    font-family: 'Cinzel', serif;
    font-size: 38px;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0 0 15px #00e5ff, 0 0 30px #00838f, 2px 2px 8px #000;
    letter-spacing: 3px;
    margin: 0;
}

.vn-subtitle {
    font-family: 'Cinzel', serif;
    font-size: 14px;
    color: #80deea;
    letter-spacing: 5px;
    margin-top: 5px;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.6);
}

/* Gothic UI Buttons */
.stButton>button {
    width: 100% !important;
    background: rgba(4, 24, 36, 0.75) !important;
    border: 1.5px solid #00838f !important;
    color: #e0f7fa !important;
    font-family: 'Cinzel', 'Tajawal', serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 12px 20px !important;
    border-radius: 20px !important;
    letter-spacing: 3px !important;
    box-shadow: inset 0 0 12px rgba(0, 229, 255, 0.15), 0 5px 20px rgba(0,0,0,0.7) !important;
    transition: all 0.3s ease-in-out !important;
    text-shadow: 0 0 8px rgba(0, 229, 255, 0.5);
    margin-bottom: 8px;
}

.stButton>button:hover {
    background: linear-gradient(90deg, rgba(0, 131, 143, 0.9), rgba(4, 24, 36, 0.95)) !important;
    border-color: #80deea !important;
    color: #ffffff !important;
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.6) !important;
    transform: scale(1.02);
}

/* Content Panels for Inner Screens */
.vn-panel {
    background: rgba(4, 24, 36, 0.88);
    border: 1px solid #00838f;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    backdrop-filter: blur(5px);
}
</style>
""".replace("BACKGROUND_URL_PLACEHOLDER", bg_css_url)

st.markdown(css_code, unsafe_allow_html=True)

# =========================================================
# ROUTING & SCREENS
# =========================================================

if st.session_state.screen == "MENU":
    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        # ترك الجهة اليسرى فارغة لتظهر رسمة ميكو والطاولة الشطرنج بالكامل وبشكل واضح
        st.write("")

    with col_right:
        st.markdown(
            """
            <div class="vn-title-container">
                <div class="vn-title">STUDY WITH MIKU</div>
                <div class="vn-subtitle">❖ RAISON D'ÊTRE ❖</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button("✦   N E W   G A M E"):
            st.session_state.screen = "NEW_GAME"
            st.rerun()

        if st.button("🌹   L O A D   G A M E"):
            st.session_state.screen = "LOAD_GAME"
            st.rerun()

        if st.button("🦋   M E M O R Y"):
            st.session_state.screen = "MEMORY"
            st.rerun()

        if st.button("✦   G A L L E R Y"):
            st.session_state.screen = "GALLERY"
            st.rerun()

        if st.button("🌙   E X I T"):
            st.session_state.screen = "EXIT"
            st.rerun()

# ---------------------------------------------------------
# NEW GAME SCREEN
# ---------------------------------------------------------
elif st.session_state.screen == "NEW_GAME":
    if st.button("◀ العودة للقائمة الرئيسية"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">NEW GAME</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    task_name = st.text_input("عنوان المهمة الدراسية:", placeholder="مثال: حل واجب الفيزياء ص 29")
    subject = st.selectbox("المادة:", ["📐 رياضيات", "⚗️ كيمياء", "🔬 فيزياء", "🧬 أحياء", "📚 عربي", "🇬🇧 English"])

    if st.button("✨ حفظ المهمة"):
        if task_name.strip():
            st.session_state.tasks.append({"name": task_name.strip(), "subject": subject, "done": False})
            st.success("تمت إضافة المهمة بنجاح! 🌹")
        else:
            st.warning("الرجاء كتابة اسم المهمة أولاً!")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD GAME SCREEN
# ---------------------------------------------------------
elif st.session_state.screen == "LOAD_GAME":
    if st.button("◀ العودة للقائمة الرئيسية"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">LOAD GAME</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    active_tasks = [t for t in st.session_state.tasks if not t["done"]]
    if not active_tasks:
        st.info("لا توجد مهام معلقة حالياً.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            if not task["done"]:
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"📖 **{task['subject']}** — {task['name']}")
                with c2:
                    if st.button("✅ إنجاز", key=f"done_{i}"):
                        st.session_state.tasks[i]["done"] = True
                        st.session_state.xp += 25
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MEMORY SCREEN (AI CHAT)
# ---------------------------------------------------------
elif st.session_state.screen == "MEMORY":
    if st.button("◀ العودة للقائمة الرئيسية"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">MEMORY</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        role = "🩵 Miku:" if msg["role"] == "assistant" else "👤 You:"
        st.write(f"**{role}** {msg['content']}")

    user_input = st.text_input("اكتبي رسالتك لميكو:", key="chat_input")
    if st.button("إرسال 🕊️"):
        if user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            api_key = st.secrets.get("GEMINI_API_KEY")
            if api_key:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    payload = {
                        "contents": [{"role": "user", "parts": [{"text": user_input}]}],
                        "system_instruction": {"parts": [{"text": "أنتِ ميكو من لعبة Visual Novel غامضة وداعم للدراسة."}]}
                    }
                    res = requests.post(url, json=payload, timeout=10)
                    if res.status_code == 200:
                        reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        st.rerun()
                except Exception as e:
                    st.error(f"خطأ: {e}")
            else:
                st.warning("⚠️ يرجى تفعيل GEMINI_API_KEY في Secrets.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# GALLERY SCREEN
# ---------------------------------------------------------
elif st.session_state.screen == "GALLERY":
    if st.button("◀ العودة للقائمة الرئيسية"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">GALLERY</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    st.write(f"🏆 **نقاط الخبرة (XP):** `{st.session_state.xp}`")
    st.write(f"👑 **المستوى:** `Level {(st.session_state.xp // 100) + 1}`")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# EXIT SCREEN
# ---------------------------------------------------------
elif st.session_state.screen == "EXIT":
    if st.button("◀ العودة للقائمة الرئيسية"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">EXIT</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel" style="text-align:center;">', unsafe_allow_html=True)
    if st.button("🔄 إعادة تعيين البيانات"):
        st.session_state.tasks = []
        st.session_state.xp = 0
        st.session_state.chat_history = []
        st.session_state.screen = "MENU"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
