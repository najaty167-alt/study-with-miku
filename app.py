import streamlit as st
import streamlit.components.v1 as components
import base64

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Study with Miku",
    page_icon="୨୧",
    layout="centered"
)

# =========================================================
# SESSION STATE
# =========================================================

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================================================
# LOAD MIKU IMAGE
# =========================================================

try:
    with open("miku.png", "rb") as image_file:
        miku_base64 = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

except FileNotFoundError:
    st.error("لم يتم العثور على miku.png داخل المشروع.")
    st.stop()

# =========================================================
# ORIGINAL STYLE
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                #e8fbff 0%,
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                #eafcff 0%,
                transparent 30%
            ),
            #ffffff;
    }

    .main-title {
        text-align: center;
        padding: 24px 18px;
        border-radius: 30px;

        background:
            linear-gradient(
                135deg,
                #e8fbff,
                #ffffff
            );

        border: 2px solid #c8f2f7;

        box-shadow:
            0 12px 35px
            rgba(83, 205, 220, 0.13);

        margin-bottom: 18px;
    }

    .main-title h1 {
        color: #35b4c4;
        margin-bottom: 8px;
        font-size: 42px;
    }

    .main-title p {
        color: #579ba4;
        font-size: 18px;
        margin: 0;
    }

    .section-title {
        color: #35aebb;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #e7fbff 0%,
                #f9feff 55%,
                #ffffff 100%
            );

        border-right: 2px solid #d7f5f8;
    }

    .sidebar-title {
        text-align: center;
        color: #35adbb;
        font-size: 27px;
        font-weight: 700;
        padding: 10px 5px 3px;
    }

    .sidebar-decoration {
        text-align: center;
        color: #75cbd4;
        font-size: 18px;
        letter-spacing: 4px;
        margin-bottom: 12px;
    }

    .welcome-box {
        background: rgba(255,255,255,0.88);

        border: 2px solid #c8f2f7;

        border-radius: 22px;

        padding: 15px;

        text-align: center;

        color: #579ba4;

        margin-bottom: 18px;

        box-shadow:
            0 8px 22px
            rgba(83,205,220,0.08);
    }

    /* BUTTONS */

    .stButton > button {
        border-radius: 18px !important;

        border: 1.5px solid #c8f2f7 !important;

        background:
            linear-gradient(
                135deg,
                #ffffff,
                #f0fcff
            ) !important;

        color: #429eaa !important;

        font-weight: 600 !important;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 8px 20px
            rgba(70,190,205,0.15);

        border-color: #8bdde5 !important;
    }

    /* CARDS */

    .cute-card {
        background:
            rgba(255,255,255,0.92);

        border: 2px solid #d4f4f7;

        border-radius: 25px;

        padding: 20px;

        margin: 12px 0;

        box-shadow:
            0 8px 25px
            rgba(80,190,205,0.08);
    }

    .cute-card-title {
        color: #36adbb;
        font-size: 22px;
        font-weight: 700;
    }

    .cute-card-text {
        color: #669fa6;
        font-size: 16px;
    }

    /* METRICS */

    [data-testid="stMetric"] {
        background: white;

        border: 2px solid #d5f4f7;

        padding: 15px;

        border-radius: 22px;

        box-shadow:
            0 8px 20px
            rgba(70,190,205,0.07);
    }

    /* INPUTS */

    input,
    textarea {
        border-radius: 17px !important;
        border: 2px solid #d7f4f7 !important;
    }

    .tiny-decoration {
        text-align: center;
        color: #82d2da;
        font-size: 16px;
        letter-spacing: 6px;
        margin: 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            Study with Miku
        </div>

        <div class="sidebar-decoration">
            ୨୧ ✦ ♡ ✦ ୨୧
        </div>

        <div class="welcome-box">
            こんにちは ♡<br>
            أهلاً بكِ في عالم ميكو ✦<br>
            خلينا نذاكر مع بعض ୨୧
        </div>
        """,
        unsafe_allow_html=True
    )

    pages = [
        ("home", "⌂  الرئيسية"),
        ("study", "♡  دراسة مع ميكو"),
        ("homework", "✦  حل الواجبات"),
        ("ask", "୨୧  اسألي ميكو"),
        ("timer", "◷  جلسة مذاكرة"),
        ("achievements", "☆  إنجازاتي")
    ]

    for page_id, page_name in pages:

        if st.button(
            page_name,
            use_container_width=True,
            key=f"page_{page_id}"
        ):

            st.session_state.page = page_id
            st.rerun()

    st.markdown(
        """
        <div class="tiny-decoration">
            ♡ ୨୧ ✦ ୨୧ ♡
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">

        <h1>Study with Miku</h1>

        <p>
            ୨୧ ذاكري معي وخلي إنجازاتك تكبر يومًا بعد يوم ୨୧
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HOME
# =========================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="cute-card">

            <div class="cute-card-title">
                ♡ أهلاً بكِ!
            </div>

            <div class="cute-card-text">
                أنا ميكو ✦ وأنا مستعدة أذاكر معكِ
                وأساعدكِ في رحلتك الدراسية ୨୧
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # INTERACTIVE MIKU
    # =====================================================

    miku_html = f"""
    <!DOCTYPE html>

    <html lang="ar">

    <head>

    <meta charset="UTF-8">

    <style>

    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: transparent;
        font-family: sans-serif;
    }}

    .game-area {{
        width: 100%;
        height: 500px;
        position: relative;

        display: flex;
        justify-content: center;
        align-items: center;

        perspective: 1000px;
    }}

    .glow {{
        position: absolute;

        width: 330px;
        height: 330px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(73,220,238,0.28),
                rgba(73,220,238,0.05),
                transparent
            );

        filter: blur(12px);

        animation:
            glow 3s ease-in-out infinite;
    }}

    @keyframes glow {{

        0%,100% {{
            transform: scale(1);
            opacity: .75;
        }}

        50% {{
            transform: scale(1.12);
            opacity: 1;
        }}

    }}

    .character {{

        width: min(320px,75vw);

        max-height: 390px;

        object-fit: cover;

        border-radius: 30px;

        position: relative;

        z-index: 5;

        cursor: pointer;

        user-select: none;

        -webkit-user-drag: none;

        box-shadow:
            0 20px 45px
            rgba(0,190,220,.25);

        transition:
            transform .15s ease-out,
            box-shadow .2s ease;

        animation:
            float 3.5s ease-in-out infinite;
    }}

    @keyframes float {{

        0%,100% {{
            margin-top: 0;
        }}

        50% {{
            margin-top: -12px;
        }}

    }}

    .character:hover {{

        box-shadow:
            0 25px 55px
            rgba(0,200,230,.40);
    }}

    .character.clicked {{

        animation:
            happyBounce .65s ease,
            float 3.5s ease-in-out infinite;
    }}

    @keyframes happyBounce {{

        0% {{
            transform: scale(1);
        }}

        30% {{
            transform:
                scale(1.08)
                rotate(-3deg);
        }}

        55% {{
            transform:
                scale(.97)
                rotate(3deg);
        }}

        75% {{
            transform:
                scale(1.04)
                rotate(-2deg);
        }}

        100% {{
            transform: scale(1);
        }}

    }}

    .speech {{

        position: absolute;

        top: 18px;

        right: 8%;

        z-index: 10;

        background: white;

        color: #39aebc;

        padding: 12px 18px;

        border-radius: 20px;

        box-shadow:
            0 8px 22px
            rgba(0,180,210,.16);

        font-size: 16px;

        font-weight: bold;

        opacity: 0;

        transform: scale(.7);

        transition:
            opacity .25s ease,
            transform .25s ease;
    }}

    .speech.show {{

        opacity: 1;

        transform: scale(1);
    }}

    .speech::after {{

        content: "";

        position: absolute;

        bottom: -10px;

        left: 25px;

        width: 20px;

        height: 20px;

        background: white;

        transform: rotate(45deg);
    }}

    .star {{

        position: absolute;

        z-index: 8;

        font-size: 25px;

        pointer-events: none;

        animation:
            popStar 1s ease forwards;
    }}

    @keyframes popStar {{

        0% {{
            opacity: 0;
            transform:
                scale(0)
                rotate(0deg);
        }}

        40% {{
            opacity: 1;
            transform:
                scale(1.3)
                rotate(90deg);
        }}

        100% {{
            opacity: 0;

            transform:
                translateY(-80px)
                scale(.3)
                rotate(180deg);
        }}

    }}

    .hint {{

        position: absolute;

        bottom: 8px;

        left: 0;

        right: 0;

        text-align: center;

        color: #66aab2;

        font-size: 15px;

        z-index: 10;
    }}

    </style>

    </head>

    <body>

    <div class="game-area" id="game">

        <div class="glow"></div>

        <div class="speech" id="speech">
            ♡ هييي! ضغطتي عليّ! ୨୧
        </div>

        <img
            src="data:image/png;base64,{miku_base64}"
            class="character"
            id="miku"
            alt="Miku"
        >

        <div class="hint">
            ୨୧ اضغطي على ميكو أو حركي إصبعك عليها ୨୧
        </div>

    </div>

    <script>

    const game =
        document.getElementById("game");

    const miku =
        document.getElementById("miku");

    const speech =
        document.getElementById("speech");

    let isInteracting = false;

    function showMessage() {{

        speech.classList.add("show");

        setTimeout(() => {{

            speech.classList.remove("show");

        }},1800);

    }}

    function createStar() {{

        const star =
            document.createElement("div");

        const stars =
            ["✦","♡","୨୧","✧"];

        star.className = "star";

        star.textContent =
            stars[
                Math.floor(
                    Math.random() *
                    stars.length
                )
            ];

        star.style.left =
            (35 + Math.random()*30) + "%";

        star.style.top =
            (40 + Math.random()*20) + "%";

        game.appendChild(star);

        setTimeout(() => {{

            star.remove();

        }},1000);

    }}

    function react() {{

        isInteracting = true;

        miku.classList.remove("clicked");

        void miku.offsetWidth;

        miku.classList.add("clicked");

        showMessage();

        for(
            let i = 0;
            i < 6;
            i++
        ) {{

            setTimeout(
                createStar,
                i * 70
            );

        }}

        setTimeout(() => {{

            isInteracting = false;

        }},700);

    }}

    function moveCharacter(
        clientX,
        clientY
    ) {{

        if(isInteracting)
            return;

        const rect =
            miku.getBoundingClientRect();

        const x =
            (clientX - rect.left) /
            rect.width;

        const y =
            (clientY - rect.top) /
            rect.height;

        const rotateY =
            (x-.5)*18;

        const rotateX =
            (.5-y)*18;

        miku.style.transform =
            `rotateX(${{rotateX}}deg)
             rotateY(${{rotateY}}deg)
             scale(1.03)`;
    }}

    game.addEventListener(
        "mousemove",
        event => {{

            moveCharacter(
                event.clientX,
                event.clientY
            );

        }}
    );

    game.addEventListener(
        "mouseleave",
        () => {{

            miku.style.transform =
                "rotateX(0deg) rotateY(0deg) scale(1)";

        }}
    );

    game.addEventListener(
        "touchmove",
        event => {{

            const touch =
                event.touches[0];

            moveCharacter(
                touch.clientX,
                touch.clientY
            );

        }},
        {{passive:true}}
    );

    game.addEventListener(
        "touchend",
        () => {{

            miku.style.transform =
                "rotateX(0deg) rotateY(0deg) scale(1)";

        }}
    );

    miku.addEventListener(
        "click",
        react
    );

    miku.addEventListener(
        "touchstart",
        react
    );

    </script>

    </body>
    </html>
    """

    components.html(
        miku_html,
        height=520,
        scrolling=False
    )

    level = (
        st.session_state.xp // 100
    ) + 1

    st.markdown(
        "<h2 class='section-title'>✦ تقدمك ✦</h2>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "♡ XP",
            st.session_state.xp
        )

    with col2:
        st.metric(
            "୨୧ المستوى",
            level
        )

# =========================================================
# STUDY PAGE
# =========================================================

elif st.session_state.page == "study":

    st.markdown(
        "<h2 class='section-title'>♡ دراسة مع ميكو</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="cute-card">

            <div class="cute-card-title">
                ୨୧ مساحة الدراسة
            </div>

            <div class="cute-card-text">
                هنا ستكون جلستك الخاصة مع ميكو ✦
                وستكون الشخصية ثلاثية الأبعاد
                وتتحرك وتتفاعل معكِ.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.button(
        "✦ ابدئي الدراسة ✦",
        use_container_width=True
    )

# =========================================================
# HOMEWORK PAGE
# =========================================================

elif st.session_state.page == "homework":

    st.markdown(
        "<h2 class='section-title'>✦ حل الواجبات</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="cute-card">

            <div class="cute-card-title">
                ♡ أرسلي السؤال لميكو
            </div>

            <div class="cute-card-text">
                ارفعي صورة السؤال وسنضيف
                تحليل الذكاء الاصطناعي هنا لاحقًا ୨୧
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "୨୧ ارفعي صورة السؤال",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:

        st.image(
            uploaded,
            caption="السؤال الذي أرسلتيه ♡",
            use_container_width=True
        )

        st.success(
            "✦ وصلت الصورة! ميكو جاهزة لتحليلها."
        )

# =========================================================
# ASK MIKU
# =========================================================

elif st.session_state.page == "ask":

    st.markdown(
        "<h2 class='section-title'>୨୧ اسألي ميكو</h2>",
        unsafe_allow_html=True
    )

    question = st.text_area(
        "♡ اكتبي سؤالك لميكو",
        placeholder="مثال: اشرحي لي قانون السرعة بطريقة سهلة..."
    )

    if st.button(
        "✦ إرسال لميكو ✦",
        use_container_width=True
    ):

        if question.strip():

            st.success(
                "♡ ميكو استلمت سؤالك!"
            )

            st.write(
                "هنا سنربط الذكاء الاصطناعي "
                "بميكو لاحقًا ୨୧"
            )

        else:

            st.warning(
                "اكتبي سؤالك أولًا ♡"
            )

# =========================================================
# TIMER
# =========================================================

elif st.session_state.page == "timer":

    st.markdown(
        "<h2 class='section-title'>◷ جلسة مذاكرة</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="cute-card">

            <div class="cute-card-title">
                ♡ اختاري وقتك
            </div>

            <div class="cute-card-text">
                أنتِ تحددين وقت الدراسة والبريك
                وعدد الجولات على كيفك ୨୧
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    study_minutes = st.number_input(
        "✦ مدة الدراسة بالدقائق",
        min_value=1,
        max_value=180,
        value=60
    )

    break_minutes = st.number_input(
        "♡ مدة البريك بالدقائق",
        min_value=1,
        max_value=60,
        value=10
    )

    rounds = st.number_input(
        "୨୧ عدد الجولات",
        min_value=1,
        max_value=10,
        value=1
    )

    st.divider()

    st.write(
        f"✦ الدراسة: **{study_minutes} دقيقة**"
    )

    st.write(
        f"♡ البريك: **{break_minutes} دقيقة**"
    )

    st.write(
        f"୨୧ الجولات: **{rounds}**"
    )

    if st.button(
        "✦ ابدئي الجلسة ✦",
        use_container_width=True
    ):

        st.success(
            "♡ جلسة المذاكرة جاهزة!"
        )

        st.write(
            "المؤقت التفاعلي وميكو التي تدرس معكِ "
            "سنضيفهما في المرحلة القادمة ୨୧"
        )

# =========================================================
# ACHIEVEMENTS
# =========================================================

elif st.session_state.page == "achievements":

    st.markdown(
        "<h2 class='section-title'>☆ إنجازاتي ☆</h2>",
        unsafe_allow_html=True
    )

    level = (
        st.session_state.xp // 100
    ) + 1

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "♡ مجموع XP",
            st.session_state.xp
        )

    with col2:
        st.metric(
            "୨୧ المستوى",
            level
        )

    completed = [
        task
        for task in st.session_state.tasks
        if task["done"]
    ]

    st.markdown(
        f"""
        <div class="cute-card">

            <div class="cute-card-title">
                ✦ إنجازاتك
            </div>

            <div class="cute-card-text">
                عدد المهام المكتملة:
                <b>{len(completed)}</b>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if completed:

        for task in completed:

            st.write(
                f"♡ {task['subject']} — {task['name']}"
            )

    else:

        st.info(
            "لسه ما عندك إنجازات مكتملة ♡"
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7ab8bf;
        font-size:15px;
        padding:10px;
    ">
        ୨୧ ✦ ♡ Study with Miku ♡ ✦ ୨୧
    </div>
    """,
    unsafe_allow_html=True
)
