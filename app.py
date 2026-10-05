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
# SESSION STATE
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
# DARK CRYSTAL GLASS DESIGN
# =========================================================
st.markdown(
    """
    <style>

    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                ellipse at 15% 20%,
                rgba(0, 190, 220, 0.20) 0%,
                transparent 35%
            ),
            radial-gradient(
                ellipse at 85% 15%,
                rgba(110, 70, 210, 0.16) 0%,
                transparent 35%
            ),
            radial-gradient(
                ellipse at 50% 100%,
                rgba(0, 120, 170, 0.20) 0%,
                transparent 45%
            ),
            linear-gradient(
                135deg,
                #01070c 0%,
                #03131d 28%,
                #061d2a 52%,
                #020b13 78%,
                #010509 100%
            );

        color: #dffcff;
        min-height: 100vh;
    }

    /* Crystal light layers */

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;

        background:
            linear-gradient(
                125deg,
                transparent 0%,
                rgba(102, 235, 255, 0.045) 24%,
                transparent 25%
            ),
            linear-gradient(
                35deg,
                transparent 0%,
                rgba(145, 90, 255, 0.035) 32%,
                transparent 33%
            ),
            linear-gradient(
                160deg,
                transparent 0%,
                rgba(255,255,255,0.025) 48%,
                transparent 49%
            );

        background-size: 420px 420px;
        animation: crystalDrift 18s linear infinite;
    }

    @keyframes crystalDrift {
        from {
            transform: translate3d(0,0,0);
        }

        50% {
            transform: translate3d(-20px,15px,0);
        }

        to {
            transform: translate3d(0,0,0);
        }
    }

    /* Floating glass lights */

    .stApp::after {
        content: "";
        position: fixed;
        width: 500px;
        height: 500px;
        right: -180px;
        top: 10%;
        pointer-events: none;
        z-index: 0;

        background:
            radial-gradient(
                circle,
                rgba(74, 224, 255, 0.11),
                transparent 68%
            );

        filter: blur(25px);

        animation: aura 7s ease-in-out infinite;
    }

    @keyframes aura {
        0%,100% {
            transform: scale(1);
            opacity: .6;
        }

        50% {
            transform: scale(1.2);
            opacity: 1;
        }
    }

    /* =====================================================
       HIDE STREAMLIT DEFAULT UI
       ===================================================== */

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    /* =====================================================
       PAGE TRANSITION
       ===================================================== */

    .transition-overlay {
        position: fixed;
        inset: 0;
        z-index: 999999;
        pointer-events: none;

        background:
            radial-gradient(
                circle at center,
                rgba(73, 235, 255, 0.22),
                transparent 45%
            ),
            #01070c;

        animation: pageTransition 0.85s ease-out forwards;
    }

    @keyframes pageTransition {

        0% {
            opacity: 1;
            backdrop-filter: blur(20px);
        }

        45% {
            opacity: .65;
            backdrop-filter: blur(12px);
        }

        100% {
            opacity: 0;
            backdrop-filter: blur(0);
        }
    }

    /* =====================================================
       TITLE
       ===================================================== */

    .vn-title {
        font-family: Georgia, serif;

        font-size: 50px;
        font-weight: 700;

        color: #f4ffff;

        text-align: right;

        letter-spacing: 4px;

        text-shadow:
            0 0 8px rgba(112, 242, 255, .8),
            0 0 25px rgba(0, 190, 220, .45),
            0 0 50px rgba(0, 150, 220, .25);

        margin-top: 25px;
        margin-bottom: 5px;
    }

    .vn-subtitle {
        text-align: right;

        color: #83dce9;

        font-size: 16px;

        letter-spacing: 4px;

        text-shadow:
            0 0 12px rgba(81, 220, 240, .45);

        margin-bottom: 35px;
    }

    /* =====================================================
       GLASS PANELS
       ===================================================== */

    .vn-panel {
        position: relative;

        background:
            linear-gradient(
                135deg,
                rgba(18, 55, 70, 0.62),
                rgba(3, 18, 28, 0.78)
            );

        border: 1px solid rgba(103, 225, 242, 0.32);

        border-radius: 22px;

        padding: 28px;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,.10),
            inset 0 -1px 0 rgba(0,0,0,.35),
            0 20px 60px rgba(0,0,0,.55),
            0 0 35px rgba(0,180,220,.08);

        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);

        overflow: hidden;
    }

    .vn-panel::before {
        content: "";

        position: absolute;

        top: 0;
        left: -100%;

        width: 70%;
        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(180,250,255,.9),
                transparent
            );

        animation: glassShine 6s ease-in-out infinite;
    }

    @keyframes glassShine {

        0% {
            left: -100%;
        }

        45%,100% {
            left: 140%;
        }
    }

    /* =====================================================
       MENU BUTTONS
       ===================================================== */

    .stButton > button {

        width: 100% !important;

        min-height: 58px;

        background:
            linear-gradient(
                135deg,
                rgba(13,48,63,.72),
                rgba(3,20,31,.82)
            ) !important;

        border:
            1px solid
            rgba(81,208,229,.38) !important;

        border-radius: 12px !important;

        color: #c8f7fb !important;

        font-family:
            Georgia,
            serif !important;

        font-size: 18px !important;

        letter-spacing: 4px !important;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,.08),
            0 8px 25px rgba(0,0,0,.35),
            0 0 15px rgba(0,180,220,.06) !important;

        transition:
            transform .28s ease,
            box-shadow .28s ease,
            border-color .28s ease,
            background .28s ease !important;
    }

    .stButton > button:hover {

        transform:
            translateX(-8px)
            scale(1.025) !important;

        background:
            linear-gradient(
                90deg,
                rgba(20,91,108,.80),
                rgba(4,27,40,.95)
            ) !important;

        border-color:
            rgba(107,235,250,.9) !important;

        box-shadow:
            0 0 15px rgba(70,220,240,.35),
            0 0 35px rgba(50,190,230,.18),
            inset 0 1px 0 rgba(255,255,255,.14) !important;

        color: #ffffff !important;
    }

    .stButton > button:active {

        transform:
            translateX(-3px)
            scale(.98) !important;

    }

    /* =====================================================
       TEXT INPUTS
       ===================================================== */

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] {

        background:
            rgba(3,18,27,.75) !important;

        color:
            #dffcff !important;

        border:
            1px solid
            rgba(90,215,235,.30) !important;

        border-radius:
            10px !important;
    }

    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {

        background:
            rgba(8,35,48,.58);

        border:
            1px solid
            rgba(80,210,230,.25);

        border-radius:
            15px;

        padding:
            15px;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,.06),
            0 10px 25px rgba(0,0,0,.30);
    }

    /* =====================================================
       3D FRAME
       ===================================================== */

    .miku-frame {

        border-radius: 24px;

        border:
            1px solid
            rgba(80,225,245,.42);

        box-shadow:
            0 0 30px rgba(0,200,230,.14),
            inset 0 0 30px rgba(0,200,230,.05);

        overflow: hidden;

        background:
            rgba(1,12,19,.45);

        backdrop-filter:
            blur(12px);
    }

    /* =====================================================
       SMALL TEXT
       ===================================================== */

    .soft-text {
        color: #83cbd5;
        line-height: 1.8;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# PAGE TRANSITION
# =========================================================

st.markdown(
    '<div class="transition-overlay"></div>',
    unsafe_allow_html=True
)

# =========================================================
# MAIN MENU
# =========================================================

if st.session_state.screen == "MENU":

    col_left, col_right = st.columns([1.35, 1])

    # -----------------------------------------------------
    # 3D MIKU
    # -----------------------------------------------------

    with col_left:

        sketchfab_embed = """
        <div class="miku-frame"
             style="
             width:100%;
             height:560px;
             border-radius:24px;
             overflow:hidden;
             border:1px solid rgba(80,225,245,.42);
             box-shadow:
             0 0 45px rgba(0,210,240,.16),
             inset 0 0 40px rgba(0,200,230,.06);
             background:#020c13;
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

                src="
                https://sketchfab.com/models/47de46d489e24baeae73129ed3527b71/embed?autostart=1&transparent=1&ui_controls=0&ui_infos=0&ui_watermark=0&ui_help=0&ui_settings=0&ui_inspector=0
                "

                style="
                width:100%;
                height:100%;
                ">
            </iframe>

        </div>
        """

        components.html(
            sketchfab_embed,
            height=575
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
            '<div class="vn-subtitle">◇ STUDY WITH MIKU 3D ◇</div>',
            unsafe_allow_html=True
        )

        st.write("")

        if st.button("◇  N E W   G A M E"):

            st.session_state.screen = "NEW_GAME"

            st.rerun()

        if st.button("◇  L O A D   G A M E"):

            st.session_state.screen = "LOAD_GAME"

            st.rerun()

        if st.button("◇  M E M O R Y"):

            st.session_state.screen = "MEMORY"

            st.rerun()

        if st.button("◇  G A L L E R Y"):

            st.session_state.screen = "GALLERY"

            st.rerun()

        if st.button("◇  E X I T"):

            st.session_state.screen = "EXIT"

            st.rerun()

        st.markdown(
            """
            <p style="
                text-align:right;
                color:#4d8d9a;
                margin-top:25px;
                letter-spacing:2px;
            ">
                Version 1.0.0 — 3D Miku Edition
            </p>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# NEW GAME
# =========================================================

elif st.session_state.screen == "NEW_GAME":

    if st.button("‹  Back to Menu"):

        st.session_state.screen = "MENU"

        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">◇ NEW GAME ◇</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="soft-text" style="text-align:center;">
        ابدئي جلسة جديدة وأضيفي مهمة للمذاكرة
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="vn-panel">',
        unsafe_allow_html=True
    )

    task_name = st.text_input(
        "عنوان المهمة الدراسية",
        placeholder="مثال: حل واجب الفيزياء ص 29"
    )

    subject = st.selectbox(
        "المادة",
        [
            "رياضيات",
            "كيمياء",
            "فيزياء",
            "أحياء",
            "اللغة العربية",
            "English",
            "تقنية معلومات"
        ]
    )

    if st.button("◇ حفظ وبدء المهمة"):

        if task_name.strip():

            st.session_state.tasks.append(
                {
                    "name": task_name.strip(),
                    "subject": subject,
                    "done": False
                }
            )

            st.success(
                "تمت إضافة المهمة بنجاح."
            )

        else:

            st.warning(
                "اكتبي اسم المهمة أولاً."
            )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# LOAD GAME
# =========================================================

elif st.session_state.screen == "LOAD_GAME":

    if st.button("‹  Back to Menu"):

        st.session_state.screen = "MENU"

        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">◇ LOAD GAME ◇</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="soft-text" style="text-align:center;">
        تابعي مهامك وأهدافك الحالية
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="vn-panel">',
        unsafe_allow_html=True
    )

    active_tasks = [
        t for t in st.session_state.tasks
        if not t["done"]
    ]

    if not active_tasks:

        st.info(
            "لا توجد مهام محفوظة حالياً. "
            "ابدئي مهمة جديدة من القائمة."
        )

    else:

        for i, task in enumerate(
            st.session_state.tasks
        ):

            if not task["done"]:

                c_info, c_btn = st.columns(
                    [3, 1]
                )

                with c_info:

                    st.write(
                        f"**{task['subject']}** — "
                        f"{task['name']}"
                    )

                with c_btn:

                    if st.button(
                        "إنجاز",
                        key=f"load_done_{i}"
                    ):

                        st.session_state.tasks[i]["done"] = True

                        st.session_state.xp += 25

                        st.success(
                            "+25 XP — إنجاز رائع."
                        )

                        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# MEMORY
# =========================================================

elif st.session_state.screen == "MEMORY":

    if st.button("‹  Back to Menu"):

        st.session_state.screen = "MENU"

        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">◇ MEMORY ◇</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="soft-text" style="text-align:center;">
        تحدثي مع ميكو واحفظي محادثاتك الدراسية
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="vn-panel">',
        unsafe_allow_html=True
    )

    for msg in st.session_state.chat_history:

        if msg["role"] == "assistant":

            role_name = "Miku"

        else:

            role_name = "You"

        st.write(
            f"**{role_name}:** "
            f"{msg['content']}"
        )

    user_input = st.text_input(
        "رسالتك إلى ميكو",
        key="memory_input"
    )

    if st.button("◇ إرسال الرسالة"):

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
                    "أضيفي GEMINI_API_KEY في Secrets "
                    "لتفعيل ردود ميكو."
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
                                    "أنتِ ميكو، "
                                    "مساعدة دراسية لطيفة وهادئة. "
                                    "تحدثي باللغة العربية "
                                    "وساعدي الطالبة في الدراسة "
                                    "وحل الأسئلة وشرح الدروس."
                                }
                            ]
                        }
                    }

                    res = requests.post(
                        url,
                        json=payload,
                        timeout=15
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
                            "حدث خطأ أثناء الاتصال بميكو."
                        )

                except Exception:

                    st.error(
                        "تعذر الاتصال بالخدمة حالياً."
                    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# GALLERY
# =========================================================

elif st.session_state.screen == "GALLERY":

    if st.button("‹  Back to Menu"):

        st.session_state.screen = "MENU"

        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">◇ GALLERY ◇</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="soft-text" style="text-align:center;">
        إنجازاتك وتقدمك في رحلة الدراسة
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="vn-panel">',
        unsafe_allow_html=True
    )

    level = (
        st.session_state.xp // 100
    ) + 1

    st.write(
        f"**نقاط الخبرة:** "
        f"`{st.session_state.xp} XP`"
    )

    st.write(
        f"**المستوى الحالي:** "
        f"`Level {level}`"
    )

    st.divider()

    st.write(
        "**المهام المكتملة:**"
    )

    completed = [
        t for t in st.session_state.tasks
        if t["done"]
    ]

    if not completed:

        st.write(
            "لم تكملي أي مهمة بعد."
        )

    else:

        for task in completed:

            st.write(
                f"◇ `{task['subject']}` — "
                f"{task['name']}"
            )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# EXIT
# =========================================================

elif st.session_state.screen == "EXIT":

    if st.button("‹  Back to Menu"):

        st.session_state.screen = "MENU"

        st.rerun()

    st.markdown(
        '<div class="vn-title" style="text-align:center;">◇ EXIT ◇</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="vn-panel" style="text-align:center;">',
        unsafe_allow_html=True
    )

    st.write(
        "هل تريدين إعادة تصفير بيانات الجلسة "
        "أو العودة إلى الشاشة الرئيسية؟"
    )

    if st.button(
        "◇ إعادة تعيين كافة البيانات"
    ):

        st.session_state.tasks = []

        st.session_state.xp = 0

        st.session_state.chat_history = []

        st.session_state.screen = "MENU"

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
