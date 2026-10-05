import streamlit as st
import streamlit.components.v1 as components
import requests

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Study with Miku — Raison d'être",
    page_icon="✦",
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
# GOTHIC AQUA / STAINED GLASS STYLE
# =========================================================
st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Tajawal:wght@400;500;700&display=swap');

    /* -----------------------------------------------------
       MAIN BACKGROUND
    ----------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(circle at 15% 20%,
                rgba(32, 145, 170, 0.22) 0%,
                transparent 25%),

            radial-gradient(circle at 85% 15%,
                rgba(104, 76, 170, 0.20) 0%,
                transparent 25%),

            radial-gradient(circle at 70% 85%,
                rgba(0, 190, 205, 0.14) 0%,
                transparent 30%),

            linear-gradient(
                135deg,
                #020b13 0%,
                #061b29 30%,
                #082c3b 55%,
                #071827 75%,
                #020911 100%
            );

        color: #e5fbff;
        font-family: 'Tajawal', sans-serif;
        min-height: 100vh;
    }

    /* Decorative stained-glass atmosphere */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;

        background:
            linear-gradient(
                120deg,
                transparent 0%,
                rgba(91, 226, 238, 0.035) 25%,
                transparent 45%
            ),
            linear-gradient(
                45deg,
                transparent 35%,
                rgba(124, 88, 190, 0.035) 60%,
                transparent 80%
            );

        opacity: 1;
    }

    /* -----------------------------------------------------
       HIDE STREAMLIT DEFAULT HEADER / FOOTER
    ----------------------------------------------------- */

    header,
    footer {
        visibility: hidden;
    }

    /* -----------------------------------------------------
       MAIN TITLE
    ----------------------------------------------------- */

    .vn-title {
        font-family: 'Cinzel', serif;
        font-size: 46px;
        font-weight: 700;

        color: #ffffff;

        text-shadow:
            0 0 10px rgba(77, 225, 240, 0.75),
            0 0 25px rgba(39, 154, 180, 0.55),
            0 0 45px rgba(81, 82, 170, 0.30),
            2px 2px 5px #000;

        letter-spacing: 3px;
        text-align: right;
        margin-bottom: 5px;
    }

    .vn-subtitle {
        font-family: 'Cinzel', serif;

        font-size: 15px;
        color: #8ed9e4;

        text-align: right;

        letter-spacing: 4px;
        margin-bottom: 30px;

        text-shadow:
            0 0 10px rgba(81, 220, 235, 0.35);
    }

    /* -----------------------------------------------------
       3D FRAME
    ----------------------------------------------------- */

    .miku-frame {
        position: relative;

        border-radius: 24px;

        border: 1px solid rgba(76, 210, 228, 0.55);

        background:
            linear-gradient(
                145deg,
                rgba(11, 49, 63, 0.65),
                rgba(3, 17, 27, 0.82)
            );

        box-shadow:
            0 0 20px rgba(39, 196, 218, 0.12),
            0 0 55px rgba(43, 99, 150, 0.12),
            inset 0 0 35px rgba(0, 180, 205, 0.05);

        padding: 5px;
    }

    /* -----------------------------------------------------
       MENU BUTTONS
    ----------------------------------------------------- */

    .stButton > button {
        width: 100% !important;

        background:
            linear-gradient(
                100deg,
                rgba(8, 38, 54, 0.78),
                rgba(7, 26, 42, 0.92)
            ) !important;

        border: 1px solid rgba(58, 157, 178, 0.75) !important;

        color: #c7f3f7 !important;

        font-family:
            'Cinzel',
            'Tajawal',
            serif !important;

        font-size: 17px !important;
        font-weight: 600 !important;

        padding: 12px 20px !important;

        border-radius: 9px !important;

        letter-spacing: 2px !important;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.40),
            inset 0 0 15px rgba(60, 210, 225, 0.03) !important;

        transition:
            all 0.3s ease !important;

        margin-bottom: 9px;
    }

    .stButton > button:hover {
        background:
            linear-gradient(
                90deg,
                rgba(23, 104, 125, 0.92),
                rgba(11, 43, 59, 0.95)
            ) !important;

        border-color: #63e9f7 !important;

        color: #ffffff !important;

        box-shadow:
            0 0 20px rgba(81, 229, 247, 0.45),
            inset 0 0 18px rgba(81, 229, 247, 0.08) !important;

        transform: translateX(-5px);
    }

    /* -----------------------------------------------------
       PANELS
    ----------------------------------------------------- */

    .vn-panel {
        background:
            linear-gradient(
                145deg,
                rgba(6, 31, 44, 0.90),
                rgba(3, 17, 27, 0.94)
            );

        border: 1px solid rgba(45, 135, 156, 0.65);

        border-radius: 17px;

        padding: 25px;

        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.55),
            inset 0 0 30px rgba(40, 190, 210, 0.025);
    }

    /* -----------------------------------------------------
       DECORATIVE TEXT
    ----------------------------------------------------- */

    .glass-line {
        height: 1px;

        margin: 15px 0 25px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(87, 219, 232, 0.65),
                rgba(128, 91, 190, 0.45),
                transparent
            );
    }

    .small-note {
        color: #71bfc9;
        font-size: 13px;
        letter-spacing: 1px;
    }

    /* -----------------------------------------------------
       INPUTS
    ----------------------------------------------------- */

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(4, 23, 34, 0.85) !important;
        color: #dffaff !important;

        border-color: #236e80 !important;
    }

    /* -----------------------------------------------------
       MOBILE FRIENDLY
    ----------------------------------------------------- */

    @media (max-width: 900px) {

        .vn-title {
            font-size: 32px;
            text-align: center;
        }

        .vn-subtitle {
            text-align: center;
            font-size: 12px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# MAIN MENU
# =========================================================
if st.session_state.screen == "MENU":

    col_left, col_right = st.columns([1.3, 1])

    # -----------------------------------------------------
    # 3D MIKU
    # -----------------------------------------------------
    with col_left:

        sketchfab_embed = """
        <div class="miku-frame"
             style="
             width:100%;
             height:520px;
             border-radius:24px;
             overflow:hidden;
             ">

            <iframe
                title="Hatsune Miku II"
                frameborder="0"
                allowfullscreen
                mozallowfullscreen="true"
                webkitallowfullscreen="true"

                allow="
                    autoplay;
                    fullscreen;
                    xr-spatial-tracking
                "

                src="https://sketchfab.com/models/47de46d489e24baeae73129ed3527b71/embed?autostart=1&transparent=1&ui_controls=0&ui_infos=0&ui_watermark=0&ui_help=0&ui_settings=0&ui_inspector=0"

                style="
                    width:100%;
                    height:100%;
                    border:0;
                ">
            </iframe>

        </div>
        """

        components.html(
            sketchfab_embed,
            height=535
        )

    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------
    with col_right:

        st.markdown(
            '<div class="vn-title">Raison d\'être</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="vn-subtitle">❖ STUDY WITH MIKU 3D ❖</div>',
            unsafe_allow_html=True
        )

        # Decorative line
        st.markdown(
            '<div class="glass-line"></div>',
            unsafe_allow_html=True
        )

        # Main study menu
        if st.button("❖  S T U D Y   W I T H   M I K U"):
            st.session_state.screen = "STUDY"
            st.rerun()

        if st.button("◷  S T U D Y   S E S S I O N"):
            st.session_state.screen = "SESSION"
            st.rerun()

        if st.button("✦  H O M E W O R K"):
            st.session_state.screen = "HOMEWORK"
            st.rerun()

        if st.button("♡  A S K   M I K U"):
            st.session_state.screen = "MEMORY"
            st.rerun()

        if st.button("☆  A C H I E V E M E N T S"):
            st.session_state.screen = "GALLERY"
            st.rerun()

        if st.button("♢  T A S K S"):
            st.session_state.screen = "LOAD_GAME"
            st.rerun()

        st.markdown(
            """
            <div class="small-note"
                 style="
                 text-align:right;
                 margin-top:18px;
                 ">
                ✦ 3D Study World · Version 1.0
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# STUDY WITH MIKU
# =========================================================
elif st.session_state.screen == "STUDY":

    if st.button("◀  B A C K"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">❖ STUDY WITH MIKU ❖</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            color:#8ed9e4;
            font-size:17px;
        ">
            Study together, stay focused, and grow your progress.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass-line"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="vn-panel">

        <h3 style="
            color:#bcecf2;
            font-family:Cinzel;
        ">
            ✦ Welcome back
        </h3>

        <p style="color:#91cbd3;">
            Miku is ready to study with you.
            Choose a task and begin your study journey.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# STUDY SESSION
# =========================================================
elif st.session_state.screen == "SESSION":

    if st.button("◀  B A C K"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">◷ STUDY SESSION ◷</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            color:#8ed9e4;
        ">
            Create your own study session.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)

    study_minutes = st.number_input(
        "Study duration",
        min_value=1,
        max_value=180,
        value=25
    )

    break_minutes = st.number_input(
        "Break duration",
        min_value=1,
        max_value=60,
        value=5
    )

    rounds = st.number_input(
        "Number of rounds",
        min_value=1,
        max_value=10,
        value=1
    )

    if st.button("✦  S T A R T   S E S S I O N"):

        st.success(
            f"Session ready — {study_minutes} min study / "
            f"{break_minutes} min break / {rounds} round(s)."
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# HOMEWORK
# =========================================================
elif st.session_state.screen == "HOMEWORK":

    if st.button("◀  B A C K"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">✦ HOMEWORK ✦</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            color:#8ed9e4;
        ">
            Upload your work and prepare it for Miku.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your homework",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if uploaded_file is not None:

        st.success(
            "Your file is ready for Miku."
        )

        st.info(
            "Homework analysis will be connected here next."
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# TASKS
# =========================================================
elif st.session_state.screen == "LOAD_GAME":

    if st.button("◀  B A C K"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">♢ TASKS ♢</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="text-align:center; color:#79cad8;">Your current study tasks</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)

    active_tasks = [
        task
        for task in st.session_state.tasks
        if not task["done"]
    ]

    if not active_tasks:

        st.info(
            "No active tasks yet. Create one from the study menu."
        )

    else:

        for i, task in enumerate(st.session_state.tasks):

            if not task["done"]:

                c_info, c_btn = st.columns([3, 1])

                with c_info:

                    st.write(
                        f"**{task['subject']}** — "
                        f"{task['name']}"
                    )

                with c_btn:

                    if st.button(
                        "✦ DONE",
                        key=f"load_done_{i}"
                    ):

                        st.session_state.tasks[i]["done"] = True
                        st.session_state.xp += 25

                        st.success("+25 XP")
                        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# ASK MIKU / MEMORY
# =========================================================
elif st.session_state.screen == "MEMORY":

    if st.button("◀  B A C K"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">♡ ASK MIKU ♡</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            color:#79cad8;
        ">
            Talk with Miku and ask about your studies.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.chat_history:

        if msg["role"] == "assistant":
            role_name = "✦ Miku"
        else:
            role_name = "◇ You"

        st.write(
            f"**{role_name}:** {msg['content']}"
        )

    user_input = st.text_input(
        "Your message",
        key="memory_input"
    )

    if st.button("✦  S E N D"):

        if user_input.strip():

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            api_key = st.secrets.get(
                "GEMINI_API_KEY"
            )

            if not api_key:

                st.warning(
                    "Add GEMINI_API_KEY to Streamlit Secrets "
                    "to activate Miku's AI responses."
                )

            else:

                try:

                    url = (
                        "https://generativelanguage.googleapis.com/"
                        "v1beta/models/gemini-1.5-flash:"
                        f"generateContent?key={api_key}"
                    )

                    payload = {
                        "contents": [
                            {
                                "role": "user",
                                "parts": [
                                    {
                                        "text": user_input
                                    }
                                ]
                            }
                        ],

                        "system_instruction": {
                            "parts": [
                                {
                                    "text":
                                    "You are Miku, a calm and supportive "
                                    "AI study companion. Help the student "
                                    "understand school subjects clearly. "
                                    "Be encouraging and explain step by step."
                                }
                            ]
                        }
                    }

                    res = requests.post(
                        url,
                        json=payload,
                        timeout=10
                    )

                    if res.status_code == 200:

                        reply = (
                            res.json()
                            ["candidates"][0]
                            ["content"]["parts"][0]
                            ["text"]
                        )

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": reply
                            }
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Miku could not connect right now."
                        )

                except Exception as e:

                    st.error(
                        f"Connection error: {e}"
                    )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# ACHIEVEMENTS
# =========================================================
elif st.session_state.screen == "GALLERY":

    if st.button("◀  B A C K"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">☆ ACHIEVEMENTS ☆</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="text-align:center; color:#79cad8;">Your study progress and achievements</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)

    level = (st.session_state.xp // 100) + 1

    st.write(
        f"✦ **Total XP:** `{st.session_state.xp}`"
    )

    st.write(
        f"☆ **Current Level:** `Level {level}`"
    )

    st.divider()

    st.write(
        "❖ **Completed Tasks**"
    )

    completed = [
        task
        for task in st.session_state.tasks
        if task["done"]
    ]

    if not completed:

        st.write(
            "No completed tasks yet."
        )

    else:

        for task in completed:

            st.write(
                f"✦ `{task['subject']}` — "
                f"{task['name']}"
            )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# EXIT / RESET
# =========================================================
elif st.session_state.screen == "EXIT":

    if st.button("◀  B A C K"):
        st.session_state.screen = "MENU"
        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">❖ SETTINGS ❖</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="vn-panel">', unsafe_allow_html=True)

    st.write(
        "Manage your current study data."
    )

    if st.button("♢  RESET ALL DATA"):

        st.session_state.tasks = []
        st.session_state.xp = 0
        st.session_state.chat_history = []
        st.session_state.screen = "MENU"

        st.success(
            "All study data has been reset."
        )

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
