import streamlit as st
import streamlit.components.v1 as components
import base64
import requests

# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="Study with Miku 🩵",
    page_icon="🎀",
    layout="centered"
)

# =========================================================
# SESSION STATE
# =========================================================
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بكِ! أنا ميكو 🩵 جاهزة أساعدك في الدراسة وحل الواجبات أو الرد على أسئلتك! ✨"}
    ]

# =========================================================
# LOAD MIKU IMAGE
# =========================================================
try:
    with open("miku.png", "rb") as image_file:
        miku_base64 = base64.b64encode(image_file.read()).decode("utf-8")
except FileNotFoundError:
    st.error("لم يتم العثور على miku.png داخل المشروع.")
    st.stop()

# =========================================================
# APP STYLE (Cute Custom CSS & Navigation Tabs)
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top, #e8fbff 0%, #ffffff 50%);
    }

    /* Main Title */
    .main-title {
        text-align: center;
        padding: 20px;
        border-radius: 28px;
        background: linear-gradient(135deg, #e8fbff, #ffffff);
        border: 2px solid #c8f2f7;
        box-shadow: 0 10px 30px rgba(83, 205, 220, 0.12);
        margin-bottom: 20px;
    }

    .main-title h1 {
        color: #39b8c7;
        margin-bottom: 8px;
        font-size: 38px;
        font-weight: 700;
    }

    .main-title p {
        color: #4b909a;
        font-size: 16px;
        margin: 0;
    }

    .section-title {
        color: #39aebb;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 12px;
    }

    /* Tabs Navigation Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
        border-bottom: 2px solid #e0f7fa;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 18px 18px 0px 0px;
        padding: 10px 20px;
        background-color: #f0faff;
        color: #39b8c7;
        font-weight: bold;
        border: 1px solid #c8f2f7;
        border-bottom: none;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #39b8c7 !important;
        color: white !important;
        box-shadow: 0 -4px 12px rgba(57, 184, 199, 0.2);
    }

    /* Metrics & Cards Styling */
    [data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 18px;
        padding: 12px;
        border: 1px solid #e0f7fa;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        text-align: center;
    }
    
    /* Cute Buttons */
    .stButton>button {
        border-radius: 16px !important;
        border: 1px solid #b2ebf2 !important;
        background: linear-gradient(135deg, #e0f7fa, #ffffff) !important;
        color: #268b97 !important;
        font-weight: bold !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton>button:hover {
        background: #39b8c7 !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(57, 184, 199, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div class="main-title">
        <h1>🎀 Study with Miku 🩵</h1>
        <p>✨ ذاكري معي وخلي إنجازاتك تكبر يومًا بعد يوم 🐾</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# NAVIGATION TABS (القوائم)
# =========================================================
tab_home, tab_tasks, tab_chat = st.tabs([
    "☁️ الرئيسية",
    "🎀 قائمة المهام",
    "🫧 اسألي ميكو"
])

# ---------------------------------------------------------
# TAB 1: HOME & INTERACTIVE MIKU
# ---------------------------------------------------------
with tab_home:
    level = (st.session_state.xp // 100) + 1
    progress_xp = (st.session_state.xp % 100) / 100.0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("⭐ نقاط الخبرة (XP)", st.session_state.xp)
    with col2:
        st.metric("👑 المستوى الحالي", f"المستوى {level}")

    st.write("")
    st.caption(f"🐾 التقدم نحو المستوى {level + 1}:")
    st.progress(progress_xp)

    st.divider()

    miku_html = f"""
    <!DOCTYPE html>
    <html lang="ar">
    <head>
    <meta charset="UTF-8">
    <style>
    * {{ box-sizing: border-box; }}
    body {{
        margin: 0; padding: 0; overflow: hidden;
        background: transparent; font-family: sans-serif;
    }}
    .game-area {{
        width: 100%; height: 450px; position: relative;
        display: flex; justify-content: center; align-items: center;
        perspective: 1000px;
    }}
    .glow {{
        position: absolute; width: 310px; height: 310px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(73, 220, 238, 0.28), rgba(73, 220, 238, 0.05), transparent);
        filter: blur(12px);
        animation: glow 3s ease-in-out infinite;
    }}
    @keyframes glow {{
        0%, 100% {{ transform: scale(1); opacity: 0.75; }}
        50% {{ transform: scale(1.12); opacity: 1; }}
    }}
    .character {{
        width: min(300px, 75vw); max-height: 370px; object-fit: cover;
        border-radius: 30px; position: relative; z-index: 5;
        cursor: pointer; user-select: none; -webkit-user-drag: none;
        box-shadow: 0 20px 45px rgba(0, 190, 220, 0.25);
        transition: transform 0.15s ease-out, box-shadow 0.2s ease;
        animation: float 3.5s ease-in-out infinite;
    }}
    @keyframes float {{
        0%, 100% {{ margin-top: 0; }}
        50% {{ margin-top: -12px; }}
    }}
    .character:hover {{
        box-shadow: 0 25px 55px rgba(0, 200, 230, 0.40);
    }}
    .character.clicked {{
        animation: happyBounce 0.65s ease, float 3.5s ease-in-out infinite;
    }}
    @keyframes happyBounce {{
        0% {{ transform: scale(1); }}
        30% {{ transform: scale(1.08) rotate(-3deg); }}
        55% {{ transform: scale(0.97) rotate(3deg); }}
        75% {{ transform: scale(1.04) rotate(-2deg); }}
        100% {{ transform: scale(1); }}
    }}
    .speech {{
        position: absolute; top: 15px; right: 8%; z-index: 10;
        background: white; color: #39aebc; padding: 12px 18px;
        border-radius: 20px; box-shadow: 0 8px 22px rgba(0, 180, 210, 0.16);
        font-size: 15px; font-weight: bold; opacity: 0;
        transform: scale(0.7); transition: opacity 0.25s ease, transform 0.25s ease;
    }}
    .speech.show {{ opacity: 1; transform: scale(1); }}
    .speech::after {{
        content: ""; position: absolute; bottom: -10px; left: 25px;
        width: 20px; height: 20px; background: white; transform: rotate(45deg);
    }}
    .star {{
        position: absolute; z-index: 8; font-size: 24px;
        pointer-events: none; animation: popStar 1s ease forwards;
    }}
    @keyframes popStar {{
        0% {{ opacity: 0; transform: scale(0) rotate(0deg); }}
        40% {{ opacity: 1; transform: scale(1.3) rotate(90deg); }}
        100% {{ opacity: 0; transform: translateY(-80px) scale(0.3) rotate(180deg); }}
    }}
    .hint {{
        position: absolute; bottom: 8px; left: 0; right: 0;
        text-align: center; color: #66aab2; font-size: 14px; z-index: 10;
    }}
    </style>
    </head>
    <body>
    <div class="game-area" id="game">
        <div class="glow"></div>
        <div class="speech" id="speech">🩵 هيا نجتهد اليوم معاً! 🎀</div>
        <img src="data:image/png;base64,{miku_base64}" class="character" id="miku" alt="Miku">
        <div class="hint">🌸 اضغطي على ميكو للتشجيع 🩵</div>
    </div>

    <script>
    const game = document.getElementById("game");
    const miku = document.getElementById("miku");
    const speech = document.getElementById("speech");
    let isInteracting = false;

    const messages = [
        "🩵 هييي! ضغطتي عليّ! 🎀",
        "✨ أنتِ ممتازة وذكية جداً! 🌸",
        "🥐 لا تنسي تأخذي استراحة بسيطة! ☕",
        "🍨 يلا كملي المذاكرة وبدعي! 💫",
        "🐾 ميكو فخورة بكِ وبإنجازاتك! 🧸"
    ];

    function showMessage() {{
        const randomMsg = messages[Math.floor(Math.random() * messages.length)];
        speech.textContent = randomMsg;
        speech.classList.add("show");
        setTimeout(() => {{ speech.classList.remove("show"); }}, 2000);
    }}

    function createStar() {{
        const star = document.createElement("div");
        const stars = ["✨", "⭐", "🩵", "🎀", "🌸", "🫧", "🐾", "🍡"];
        star.className = "star";
        star.textContent = stars[Math.floor(Math.random() * stars.length)];
        star.style.left = (35 + Math.random() * 30) + "%";
        star.style.top = (40 + Math.random() * 20) + "%";
        game.appendChild(star);
        setTimeout(() => {{ star.remove(); }}, 1000);
    }}

    function react() {{
        isInteracting = true;
        miku.classList.remove("clicked");
        void miku.offsetWidth;
        miku.classList.add("clicked");
        showMessage();
        for (let i = 0; i < 6; i++) {{ setTimeout(createStar, i * 70); }}
        setTimeout(() => {{ isInteracting = false; }}, 700);
    }}

    function moveCharacter(clientX, clientY) {{
        if (isInteracting) return;
        const rect = miku.getBoundingClientRect();
        const x = (clientX - rect.left) / rect.width;
        const y = (clientY - rect.top) / rect.height;
        const rotateY = (x - 0.5) * 18;
        const rotateX = (0.5 - y) * 18;
        miku.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) scale(1.03)`;
    }}

    game.addEventListener("mousemove", (e) => moveCharacter(e.clientX, e.clientY));
    game.addEventListener("mouseleave", () => {{ miku.style.transform = "rotateX(0deg) rotateY(0deg) scale(1)"; }});
    game.addEventListener("touchmove", (e) => moveCharacter(e.touches[0].clientX, e.touches[0].clientY), {{ passive: true }});
    game.addEventListener("touchend", () => {{ miku.style.transform = "rotateX(0deg) rotateY(0deg) scale(1)"; }});
    miku.addEventListener("click", react);
    miku.addEventListener("touchstart", react);
    </script>
    </body>
    </html>
    """
    components.html(miku_html, height=460, scrolling=False)


# ---------------------------------------------------------
# TAB 2: TASKS & ACHIEVEMENTS
# ---------------------------------------------------------
with tab_tasks:
    st.markdown("<div class='section-title'>📝 إضافة مهمة جديدة</div>", unsafe_allow_html=True)
    
    col_input, col_sub = st.columns([2, 1])
    with col_input:
        task_name = st.text_input("عنوان المهمة", placeholder="مثال: حل واجب الفيزياء ص 29 📖", label_visibility="collapsed")
    with col_sub:
        subject = st.selectbox(
            "المادة",
            [
                "📐 رياضيات متقدمة",
                "⚗️ كيمياء",
                "🔬 فيزياء",
                "🧬 أحياء",
                "📚 اللغة العربية",
                "🇬🇧 English",
                "☪️ التربية الإسلامية",
                "💻 تقنية معلومات",
                "🎨 الفنون والمهارات",
                "✨ أخرى"
            ],
            label_visibility="collapsed"
        )

    if st.button("➕ أضيفي المهمة للقائمة", use_container_width=True):
        if task_name.strip():
            st.session_state.tasks.append({
                "name": task_name.strip(),
                "subject": subject,
                "done": False
            })
            st.success("تمت إضافة المهمة بنجاح! 🩵🎀")
            st.rerun()
        else:
            st.warning("رجاءً اكتبي عنوان المهمة أولاً 🥹")

    st.divider()

    st.markdown("<div class='section-title'>📋 المهام الحالية</div>", unsafe_allow_html=True)
    
    active_tasks = [t for t in st.session_state.tasks if not t["done"]]
    
    if not active_tasks:
        st.info("لا توجد مهام معلقة حالياً! ✨ أضيفي مهمتك الأولى وابدئي الإنجاز مع ميكو 🍨")
    else:
        for i, task in enumerate(st.session_state.tasks):
            if not task["done"]:
                col_t, col_b = st.columns([3, 1])
                with col_t:
                    st.write(f"**{task['subject']}** — {task['name']}")
                with col_b:
                    if st.button("✨ إنجاز", key=f"done_{i}", use_container_width=True):
                        st.session_state.tasks[i]["done"] = True
                        st.session_state.xp += 20
                        st.success("أحسنتِ! +20 XP 🩵🎉")
                        st.rerun()

    # Completed Achievements Section
    completed = [t for t in st.session_state.tasks if t["done"]]
    if completed:
        st.divider()
        st.markdown("<div class='section-title'>🏆 لوحة الإنجازات المكتملة</div>", unsafe_allow_html=True)
        for task in completed:
            st.write(f"✅ **{task['subject']}** — ~~{task['name']}~~")


# ---------------------------------------------------------
# TAB 3: ASK MIKU (GEMINI AI CHAT)
# ---------------------------------------------------------
with tab_chat:
    st.markdown("<div class='section-title'>🫧 اسألي ميكو للذكاء الاصطناعي</div>", unsafe_allow_html=True)
    st.caption("ميكو جاهزة لمساعدتك في شرح الدروس، حل الواجبات، أو تقديم نصائح دراسية 🥐🩵")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🩵" if msg["role"] == "assistant" else "🎀"):
            st.markdown(msg["content"])

    # Chat Input
    if user_prompt := st.chat_input("اكتبي سؤالك لميكو هنا..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar="🎀"):
            st.markdown(user_prompt)

        api_key = st.secrets.get("GEMINI_API_KEY")

        with st.chat_message("assistant", avatar="🩵"):
            if not api_key:
                response_text = "⚠️ لم يتم العثور على مفتاح GEMINI_API_KEY في إعدادات Secrets. الرجاء إضافته أولاً لتفعيلي!"
                st.warning(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                with st.spinner("ميكو تفكر بالجواب... 💭✨"):
                    try:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                        
                        system_instruction = "أنتِ ميكو (Miku)، صديقة دراسية لطيفة وذكية جداً. تتحدثين باللغة العربية بأسلوب لطيف ومشجع مع استخدام إيموجيات كيوت (🩵, 🎀, ✨, 🌸). تساعدين في الشرح والحلول بشكل واضح ودقيق."
                        
                        contents = []
                        for m in st.session_state.messages:
                            role = "user" if m["role"] == "user" else "model"
                            contents.append({
                                "role": role,
                                "parts": [{"text": m["content"]}]
                            })

                        payload = {
                            "system_instruction": {
                                "parts": [{"text": system_instruction}]
                            },
                            "contents": contents
                        }

                        res = requests.post(url, json=payload, timeout=15)
                        if res.status_code == 200:
                            data = res.json()
                            response_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        else:
                            response_text = f"حدث خطأ أثناء التواصل مع الذكاء الاصطناعي (رمز الخطأ: {res.status_code}). تأكدي من صحة المفتاح."
                    except Exception as e:
                        response_text = f"عذراً حدث خطأ: {str(e)}"

                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption("🩵 Study with Miku — your cute kawaii study companion 🎀🐾")
