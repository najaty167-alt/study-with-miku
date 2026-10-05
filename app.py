import streamlit as st
import streamlit.components.v1 as components
import requests

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Study with Miku — Raison d'être",
    page_icon="🌹",
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
# VISUAL NOVEL GOTHIC AQUA STYLING (CSS)
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Tajawal:wght@400;700&display=swap');

    /* Fullscreen VN Background */
    .stApp {
        background: linear-gradient(135deg, #03131e 0%, #082838 50%, #021019 100%);
        color: #e0f7fa;
        font-family: 'Tajawal', sans-serif;
    }

    /* Hide Header and Footer */
    header, footer { visibility: hidden; }

    /* Title Logo */
    .vn-title {
        font-family: 'Cinzel', serif;
        font-size: 46px;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 15px #39d5e6, 0 0 30px #0b8093, 2px 2px 4px #000;
        letter-spacing: 3px;
        text-align: right;
        margin-bottom: 5px;
    }

    .vn-subtitle {
        font-size: 16px;
        color: #79cad8;
        text-align: right;
        letter-spacing: 2px;
        margin-bottom: 35px;
    }

    /* VN Menu Buttons Override */
    .stButton>button {
        width: 100% !important;
        background: rgba(8, 38, 54, 0.75) !important;
        border: 1px solid #23788c !important;
        color: #bcecf2 !important;
        font-family: 'Cinzel', 'Tajawal', serif !important;
        font-size: 19px !important;
        font-weight: bold !important;
        padding: 12px 25px !important;
        border-radius: 8px !important;
        letter-spacing: 2px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        transition: all 0.3s ease-in-out !important;
        text-shadow: 0 0 8px rgba(57, 213, 230, 0.5);
        margin-bottom: 10px;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, rgba(23, 102, 122, 0.85), rgba(8, 38, 54, 0.95)) !important;
        border-color: #51e5f7 !important;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(81, 229, 247, 0.6) !important;
        transform: translateX(-8px) scale(1.02);
    }

    /* Card Panels for Content Screens */
    .vn-panel {
        background: rgba(5, 25, 36, 0.88);
        border: 1px solid #1a6478;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# ROUTING & SCREENS
# =========================================================

# ---------------------------------------------------------
# SCREEN: MAIN MENU (الواجهة الرئيسية مع مجسم 3D)
# ---------------------------------------------------------
if st.session_state.screen == "MENU":
    col_left, col_right = st.columns([1.3, 1])

    with col_left:
        # Sketchfab 3D Embed (Hatsune Miku II)
        sketchfab_embed = """
        <div style="width:100%; height:520px; border-radius:20px; overflow:hidden; border:2px solid #1a6478; box-shadow: 0 0 30px rgba(57, 213, 230, 0.2);">
            <iframe 
                title="Hatsune Miku II" 
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
        components.html(sketchfab_embed, height=535)

    with col_right:
        st.markdown('<div class="vn-title">Raison d\'être</div>', unsafe_allow_html=True)
        st.markdown('<div class="vn-subtitle">❖ STUDY WITH MIKU 3D ❖</div>', unsafe_allow_html=True)

        st.write("")

        if st.button("❖  N E W   G A M E"):
            st.session_state.screen = "NEW_GAME"
            st.rerun()

        if st.button("🌹  L O A D   G A M E"):
            st.session_state.screen = "LOAD_GAME"
            st.rerun()

        if st.button("❖  M E M O R Y"):
            st.session_state.screen = "MEMORY"
            st.rerun()

        if st.button("❖  G A L L E R Y"):
            st.session_state.screen = "GALLERY"
            st.rerun()

        if st.button("❖  E X I T"):
            st.session_state.screen = "EXIT"
            st.rerun()

        st.caption("<p style='text-align: right; color: #438796; margin-top: 20px;'>Version 1.0.0 — 3D Miku Edition 🩵</p>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SCREEN 1: NEW GAME
# ---------------------------------------------------------
elif st.session_state.screen == "NEW_GAME":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◀ Back to Menu"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title" style="text-align:center;">❖ NEW GAME ❖</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#79cad8;">بدء جلسة جديدة وإضافة مهمة للمذاكرة</p>', unsafe_allow_html=True)

    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    task_name = st.text_input("عنوان المهمة الدراسية:", placeholder="مثال: حل واجب الفيزياء ص 29")
    subject = st.selectbox(
        "المادة:",
        ["📐 رياضيات متقدمة", "⚗️ كيمياء", "🔬 فيزياء", "🧬 أحياء", "📚 اللغة العربية", "🇬🇧 English", "💻 تقنية معلومات"]
    )

    if st.button("✨ حفظ وبدء المهمة"):
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
        if st.button("◀ Back to Menu"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title" style="text-align:center;">🌹 LOAD GAME 🌹</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#79cad8;">متابعة المهام والأهداف الحالية</p>', unsafe_allow_html=True)

    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)
    active_tasks = [t for t in st.session_state.tasks if not t["done"]]
    if not active_tasks:
        st.info("لا توجد مهام محفوظة معلقة حالياً. ابدئي مهمة جديدة من New Game!")
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
                        st.success("+25 XP! إنجاز رائع 🩵")
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# SCREEN 3: MEMORY
# ---------------------------------------------------------
elif st.session_state.screen == "MEMORY":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◀ Back to Menu"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title" style="text-align:center;">❖ MEMORY ❖</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#79cad8;">سجل الحوار والملاحظات مع ميكو (الذكاء الاصطناعي)</p>', unsafe_allow_html=True)

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
        if st.button("◀ Back to Menu"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title" style="text-align:center;">❖ GALLERY ❖</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#79cad8;">معرض الألقاب والجوائز المكتسبة</p>', unsafe_allow_html=True)

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
        if st.button("◀ Back to Menu"):
            st.session_state.screen = "MENU"
            st.rerun()

    st.markdown('<div class="vn-title" style="text-align:center;">❖ EXIT ❖</div>', unsafe_allow_html=True)
    st.markdown('<div class="vn-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.write("هل ترغبين في إعادة تصفير الجلسة أو العودة للشاشة الرئيسية؟")
    
    if st.button("🔄 إعادة تعيين كافة البيانات (Reset All Data)"):
        st.session_state.tasks = []
        st.session_state.xp = 0
        st.session_state.chat_history = []
        st.session_state.screen = "MENU"
        st.success("تم إعادة التعيين بنجاح!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
