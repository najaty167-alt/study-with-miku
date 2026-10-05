import streamlit as st
import streamlit.components.v1 as components
import requests

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
# GOTHIC STAINED-GLASS STYLING (CSS)
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Tajawal:wght@400;700&display=swap');

    /* Fullscreen Gothic Stained-Glass Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #082232 0%, #020c14 100%);
        color: #d1f4ff;
        font-family: 'Tajawal', sans-serif;
    }

    /* Hide Streamlit default components */
    header, footer { visibility: hidden; }

    /* VN Game Title Styling */
    .vn-title-container {
        text-align: center;
        margin-bottom: 25px;
    }

    .vn-title {
        font-family: 'Cinzel', serif;
        font-size: 40px;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 20px #22d3ee, 0 0 40px #0891b2, 2px 2px 5px #000;
        letter-spacing: 4px;
        margin: 0;
    }

    .vn-subtitle {
        font-family: 'Cinzel', serif;
        font-size: 15px;
        color: #67e8f9;
        letter-spacing: 6px;
        margin-top: 6px;
        text-shadow: 0 0 10px rgba(103, 232, 249, 0.5);
    }

    /* Gothic UI Buttons Override */
    .stButton>button {
        width: 100% !important;
        background: rgba(6, 30, 45, 0.75) !important;
        border: 1.5px solid #164e63 !important;
        color: #cffaffe6 !important;
        font-family: 'Cinzel', 'Tajawal', serif !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 14px 20px !important;
        border-radius: 25px !important;
        letter-spacing: 3px !important;
        box-shadow: inset 0 0 15px rgba(34, 211, 238, 0.1), 0 4px 20px rgba(0, 0, 0, 0.6) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-shadow: 0 0 8px rgba(34, 211, 238, 0.6);
        margin-bottom: 12px;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, rgba(14, 116, 144, 0.8), rgba(8, 51, 68, 0.9)) !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        box-shadow: inset 0 0 25px rgba(56, 189, 248, 0.3), 0 0 25px rgba(56, 189, 248, 0.5) !important;
        transform: translateY(-2px) scale(1.02);
    }

    /* Content Panels */
    .vn-panel {
        background: rgba(4, 20, 31, 0.9);
        border: 1px solid #155e75;
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.8), inset 0 0 20px rgba(34, 211, 238, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# ROUTING & SCREENS
# =========================================================

# ---------------------------------------------------------
# SCREEN: MAIN MENU (الواجهة الرئيسية مع مجسم 3D في الإطار الغوطي)
# ---------------------------------------------------------
if st.session_state.screen == "MENU":
    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        # Sketchfab 3D Embed (Hatsune Miku II) داخل إطار الزجاج المعشق
        sketchfab_embed = """
        <div style="width:100%; height:530px; border-radius:20px; overflow:hidden; border:2px solid #155e75; box-shadow: 0 0 35px rgba(34, 211, 238, 0.25); background: #020c14;">
            <iframe 
                title="Hatsune Miku II 3D" 
                frameborder="0" 
                allowfullscreen 
                mozallowfullscreen="true" 
                webkitallowfullscreen="true" 
                allow="autoplay; fullscreen; xr-spatial-tracking" 
                src="https://sketchfab.com/models/47de46d489e24baeae73129ed3527b71/embed?autostart=1&transparent=1&ui_controls=0&ui_infos=0&ui_watermark=0&ui_help=0&ui_settings=0&ui_inspector=0"
                style="width: 100%; height: 100%;">
            </iframe>
        </div>
        """
        components.html(sketchfab_embed, height=545)

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
# SCREEN 1: NEW GAME
# ---------------------------------------------------------
elif st.session_state.screen == "NEW_GAME":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◀ Back"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">NEW GAME</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    task_name = st.text_input("عنوان المهمة الدراسية:", placeholder="مثال: حل واجب الفيزياء ص 29")
    subject = st.selectbox(
        "المادة:",
        ["📐 رياضيات متقدمة", "⚗️ كيمياء", "🔬 فيزياء", "🧬 أحياء", "📚 اللغة العربية", "🇬🇧 English", "💻 تقنية معلومات"]
    )

    if st.button("✨ حفظ المهمة"):
        if task_name.strip():
            st.session_state.tasks.append({"name": task_name.strip(), "subject": subject, "done": False})
            st.success("تمت إضافة المهمة بنجاح إلى سجل اللعبة! 🌹")
        else:
            st.warning("الرجاء كتابة اسم المهمة أولاً!")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# SCREEN 2: LOAD GAME
# ---------------------------------------------------------
elif st.session_state.screen == "LOAD_GAME":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◀ Back"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">LOAD GAME</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    active_tasks = [t for t in st.session_state.tasks if not t["done"]]
    if not active_tasks:
        st.info("لا توجد مهام محفوظة معلقة حالياً.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            if not task["done"]:
                c_info, c_btn = st.columns([3, 1])
                with c_info:
                    st.write(f"📖 **{task['subject']}** — {task['name']}")
                with c_btn:
                    if st.button("✅ إنجاز", key=f"load_done_{i}"):
                        st.session_state.tasks[i]["done"] = True
                        st.session_state.xp += 25
                        st.success("+25 XP!")
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# SCREEN 3: MEMORY (AI CHAT)
# ---------------------------------------------------------
elif st.session_state.screen == "MEMORY":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◀ Back"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">MEMORY</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        role_icon = "🩵 Miku:" if msg["role"] == "assistant" else "👤 You:"
        st.write(f"**{role_icon}** {msg['content']}")

    user_input = st.text_input("اكتبي رسالتك لميكو:", key="memory_input")
    if st.button("إرسال الرسالة 🕊️"):
        if user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.warning("⚠️ الرجاء إضافة GEMINI_API_KEY في إعدادات Secrets لتفعيل ردود ميكو!")
            else:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    payload = {
                        "contents": [{"role": "user", "parts": [{"text": user_input}]}],
                        "system_instruction": {"parts": [{"text": "أنتِ ميكو من لعبة Visual Novel غامضة ولطيفة. تتحدثين بأسلوب هادئ وشارح وداعم للدراسة باللغة العربية."}]}
                    }
                    res = requests.post(url, json=payload, timeout=10)
                    if res.status_code == 200:
                        reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        st.rerun()
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {e}")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# SCREEN 4: GALLERY
# ---------------------------------------------------------
elif st.session_state.screen == "GALLERY":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◀ Back"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">GALLERY</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    level = (st.session_state.xp // 100) + 1
    st.write(f"🏆 **نقاط الخبرة الإجمالية (XP):** `{st.session_state.xp}`")
    st.write(f"👑 **المستوى الحالي:** `Level {level}`")

    st.divider()
    st.write("🖼️ **المهام المكتملة:**")
    completed = [t for t in st.session_state.tasks if t["done"]]
    if not completed:
        st.write("لم تقمي بإكمال أي مهمة بعد.")
    else:
        for task in completed:
            st.write(f"🌟 `{task['subject']}` — {task['name']}")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# SCREEN 5: EXIT
# ---------------------------------------------------------
elif st.session_state.screen == "EXIT":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◀ Back"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title-container"><div class="vn-title">EXIT</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.write("هل ترغبين في إعادة تصفير الجلسة؟")
    if st.button("🔄 إعادة تعيين كافة البيانات"):
        st.session_state.tasks = []
        st.session_state.xp = 0
        st.session_state.chat_history = []
        st.session_state.screen = "MENU"
        st.success("تم إعادة التعيين بنجاح!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
