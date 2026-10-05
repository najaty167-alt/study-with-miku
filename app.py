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
# GOTHIC STAINED-GLASS FULL BACKGROUND (CSS)
# =========================================================
# يمكن استبدال رابط الصورة أدناه برابط خلفيتكِ المباشر
BACKGROUND_IMAGE_URL = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=2000&auto=format&fit=crop"

css_code = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Tajawal:wght@400;700&display=swap');

/* Fullscreen Gothic Stained Glass Image Background */
.stApp {
    background: linear-gradient(rgba(2, 12, 20, 0.65), rgba(2, 12, 20, 0.85)), 
                url('BACKGROUND_URL_PLACEHOLDER') center/cover no-repeat fixed !important;
    color: #d1f4ff;
    font-family: 'Tajawal', sans-serif;
}

/* Hide Streamlit Header & Footer */
header, footer { visibility: hidden; }

/* Title Styling */
.vn-title-container {
    text-align: center;
    margin-top: 10px;
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
    background: rgba(4, 24, 36, 0.82) !important;
    border: 1.5px solid #00838f !important;
    color: #e0f7fa !important;
    font-family: 'Cinzel', 'Tajawal', serif !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    padding: 13px 20px !important;
    border-radius: 20px !important;
    letter-spacing: 3px !important;
    box-shadow: inset 0 0 12px rgba(0, 229, 255, 0.15), 0 5px 20px rgba(0,0,0,0.7) !important;
    transition: all 0.3s ease-in-out !important;
    text-shadow: 0 0 8px rgba(0, 229, 255, 0.5);
    margin-bottom: 10px;
}

.stButton>button:hover {
    background: linear-gradient(90deg, rgba(0, 131, 143, 0.9), rgba(4, 24, 36, 0.95)) !important;
    border-color: #80deea !important;
    color: #ffffff !important;
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.6) !important;
    transform: scale(1.02);
}

/* Transparent Frame Container for 3D Model */
.miku-3d-box {
    width: 100%;
    height: 530px;
    border-radius: 20px;
    overflow: hidden;
    border: 1.5px solid rgba(0, 229, 255, 0.3);
    box-shadow: 0 0 30px rgba(0, 229, 255, 0.2);
    background: rgba(2, 12, 20, 0.3);
    backdrop-filter: blur(3px);
}

/* Content Panels for Inner Screens */
.vn-panel {
    background: rgba(4, 24, 36, 0.92);
    border: 1px solid #00838f;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.8);
}
</style>
""".replace("BACKGROUND_URL_PLACEHOLDER", BACKGROUND_IMAGE_URL)

st.markdown(css_code, unsafe_allow_html=True)

# =========================================================
# ROUTING & SCREENS
# =========================================================

if st.session_state.screen == "MENU":
    col_left, col_right = st.columns([1.35, 1])

    with col_left:
        sketchfab_embed = """
        <div class="miku-3d-box">
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
                c1, c2 = st
