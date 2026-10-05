import streamlit as st
import streamlit.components.v1 as components
import base64
=========================================================
PAGE SETTINGS
=========================================================
st.set_page_config(
    page_title="Study with Miku 🩵",
    page_icon="🎀",
    layout="centered"
)
=========================================================
SESSION STATE
=========================================================
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
=========================================================
LOAD MIKU IMAGE
=========================================================
try:
    with open("miku.png", "rb") as image_file:
        miku_base64 = base64.b64encode(
            image_file.read()
        ).decode("utf-8")
except FileNotFoundError:
    st.error("لم يتم العثور على miku.png داخل المشروع.")
    st.stop()
=========================================================
APP STYLE
=========================================================
st.markdown(
    """
    </p>
<pre><code>.stApp {
    background:
        radial-gradient(circle at top, #e8fbff 0%, #ffffff 45%);
}

.main-title {
    text-align: center;
    padding: 20px;
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        #e8fbff,
        #ffffff
    );
    border: 2px solid #c8f2f7;
    box-shadow: 0 10px 30px rgba(83, 205, 220, 0.12);
    margin-bottom: 15px;
}

.main-title h1 {
    color: #39b8c7;
    margin-bottom: 8px;
    font-size: 42px;
}

.main-title p {
    color: #4b909a;
    font-size: 18px;
    margin: 0;
}

.section-title {
    color: #39aebb;
}

&lt;/style&gt;
&quot;&quot;&quot;,
unsafe_allow_html=True
</code></pre>
<p>)</p>
<h1>=========================================================</h1>
<h1>HEADER</h1>
<h1>=========================================================</h1>
<p>st.markdown(
    &quot;&quot;&quot;
    <div class="main-title">
        <h1>🎀 Study with Miku 🩵</h1>
        <p>✨ ذاكري معي وخلي إنجازاتك تكبر يومًا بعد يوم</p>
    </div>
    &quot;&quot;&quot;,
    unsafe_allow_html=True
)</p>
<h1>=========================================================</h1>
<h1>INTERACTIVE MIKU</h1>
<h1>=========================================================</h1>
<p>miku_html = f&quot;&quot;&quot;
<!DOCTYPE html></p>
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
    background: radial-gradient(
        circle,
        rgba(73, 220, 238, 0.28),
        rgba(73, 220, 238, 0.05),
        transparent
    );
    filter: blur(12px);
    animation: glow 3s ease-in-out infinite;
}}

@keyframes glow {{
    0%, 100% {{
        transform: scale(1);
        opacity: 0.75;
    }}

    50% {{
        transform: scale(1.12);
        opacity: 1;
    }}
}}

.character {{
    width: min(320px, 75vw);
    max-height: 390px;
    object-fit: cover;

    border-radius: 30px;

    position: relative;
    z-index: 5;

    cursor: pointer;

    user-select: none;
    -webkit-user-drag: none;

    box-shadow:
        0 20px 45px rgba(0, 190, 220, 0.25);

    transition:
        transform 0.15s ease-out,
        box-shadow 0.2s ease;

    animation: float 3.5s ease-in-out infinite;
}}

@keyframes float {{
    0%, 100% {{
        margin-top: 0;
    }}

    50% {{
        margin-top: -12px;
    }}
}}

.character:hover {{
    box-shadow:
        0 25px 55px rgba(0, 200, 230, 0.40);
}}

.character.clicked {{
    animation:
        happyBounce 0.65s ease,
        float 3.5s ease-in-out infinite;
}}

@keyframes happyBounce {{
    0% {{
        transform: scale(1);
    }}

    30% {{
        transform: scale(1.08) rotate(-3deg);
    }}

    55% {{
        transform: scale(0.97) rotate(3deg);
    }}

    75% {{
        transform: scale(1.04) rotate(-2deg);
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
        0 8px 22px rgba(0, 180, 210, 0.16);

    font-size: 16px;
    font-weight: bold;

    opacity: 0;
    transform: scale(0.7);

    transition:
        opacity 0.25s ease,
        transform 0.25s ease;
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

    animation: popStar 1s ease forwards;
}}

@keyframes popStar {{
    0% {{
        opacity: 0;
        transform: scale(0) rotate(0deg);
    }}

    40% {{
        opacity: 1;
        transform: scale(1.3) rotate(90deg);
    }}

    100% {{
        opacity: 0;
        transform: translateY(-80px)
                   scale(0.3)
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


<div class="glow"></div>

<div class="speech" id="speech">
    🩵 هييي! ضغطتي عليّ! 🎀
</div>

<img
    src="data:image/png;base64,{miku_base64}"
    class="character"
    id="miku"
    alt="Miku"
>

<div class="hint">
    🎀 اضغطي على ميكو أو حركي إصبعك عليها 🩵
</div>


const game = document.getElementById("game");
const miku = document.getElementById("miku");
const speech = document.getElementById("speech");

let isInteracting = false;

function showMessage() {{

    speech.classList.add("show");

    setTimeout(() => {{
        speech.classList.remove("show");
    }}, 1800);
}}

function createStar() {{

    const star = document.createElement("div");

    const stars = ["✨", "⭐", "🩵", "🎀"];

    star.className = "star";
    star.textContent =
        stars[Math.floor(Math.random() * stars.length)];

    star.style.left =
        (35 + Math.random() * 30) + "%";

    star.style.top =
        (40 + Math.random() * 20) + "%";

    game.appendChild(star);

    setTimeout(() => {{
        star.remove();
    }}, 1000);
}}

function react() {{

    isInteracting = true;

    miku.classList.remove("clicked");

    void miku.offsetWidth;

    miku.classList.add("clicked");

    showMessage();

    for (let i = 0; i < 6; i++) {{
        setTimeout(createStar, i * 70);
    }}

    setTimeout(() => {{
        isInteracting = false;
    }}, 700);
}}

function moveCharacter(clientX, clientY) {{

    if (isInteracting) return;

    const rect = miku.getBoundingClientRect();

    const x =
        (clientX - rect.left) /
        rect.width;

    const y =
        (clientY - rect.top) /
        rect.height;

    const rotateY =
        (x - 0.5) * 18;

    const rotateX =
        (0.5 - y) * 18;

    miku.style.transform =
        `rotateX(${{rotateX}}deg)
         rotateY(${{rotateY}}deg)
         scale(1.03)`;
}}

// Mouse
game.addEventListener("mousemove", (event) => {{
    moveCharacter(event.clientX, event.clientY);
}});

game.addEventListener("mouseleave", () => {{

    miku.style.transform =
        "rotateX(0deg) rotateY(0deg) scale(1)";
}});

// Touch
game.addEventListener(
    "touchmove",
    (event) => {{

        const touch = event.touches[0];

        moveCharacter(
            touch.clientX,
            touch.clientY
        );

    }},
    {{ passive: true }}
);

game.addEventListener(
    "touchend",
    () => {{

        miku.style.transform =
            "rotateX(0deg) rotateY(0deg) scale(1)";
    }}
);

// Click
miku.addEventListener("click", () => {{
    react();
}});

// Touch
miku.addEventListener("touchstart", () => {{
    react();
}});




"""


components.html(
    miku_html,
    height=520,
    scrolling=False
)
=========================================================
XP / LEVEL
=========================================================
level = (st.session_state.xp // 100) + 1
st.markdown("
🌱 تقدمك
",
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "⭐ XP",
        st.session_state.xp
    )
with col2:
    st.metric(
        "🎀 المستوى",
        level
    )
st.divider()
=========================================================
ADD TASK
=========================================================
st.markdown(
    "
📝 أضيفي مهمة
",
    unsafe_allow_html=True
)
task_name = st.text_input(
    "اسم المهمة",
    placeholder="مثال: حل واجب الفيزياء ص 29"
)
subject = st.selectbox(
    "المادة",
    [
        "📐 رياضيات",
        "⚗️ كيمياء",
        "🔬 فيزياء",
        "📚 عربي",
        "🇬🇧 إنجليزي",
        "☪️ إسلامية",
        "🌍 اجتماعيات",
        "🔬 علوم",
        "✨ أخرى"
    ]
)
if st.button(
    "🎀 أضيفي المهمة",
    use_container_width=True
):
if task_name.strip():

    st.session_state.tasks.append(
        {
            "name": task_name.strip(),
            "subject": subject,
            "done": False
        }
    )

    st.success(
        "تمت إضافة المهمة! 🩵🎀"
    )

    st.rerun()

else:

    st.warning(
        "اكتبي اسم المهمة أولًا 🥹"
    )

st.divider()
=========================================================
TODAY TASKS
=========================================================
st.markdown(
    "
📚 مهامي اليوم
",
    unsafe_allow_html=True
)
if not st.session_state.tasks:
st.info(
    "ما عندك مهام حاليًا ✨ "
    "أضيفي أول مهمة وابدئي مع ميكو! 🎀"
)

else:
for i, task in enumerate(
    st.session_state.tasks
):

    if not task["done"]:

        st.write(
            f"**{task['subject']}** — "
            f"{task['name']}"
        )

        if st.button(
            "✅ خلصت المهمة",
            key=f"done_{i}",
            use_container_width=True
        ):

            st.session_state.tasks[i]["done"] = True
            st.session_state.xp += 20

            st.success(
                "ميكو فخورة فيك! 🩵 +20 XP 🎀"
            )

            st.rerun()

=========================================================
COMPLETED TASKS
=========================================================
completed = [
    task
    for task in st.session_state.tasks
    if task["done"]
]
if completed:
st.divider()

st.markdown(
    "<h2 class='section-title'>🏆 إنجازاتك</h2>",
    unsafe_allow_html=True
)

for task in completed:

    st.write(
        f"✅ {task['subject']} — "
        f"{task['name']}"
    )

=========================================================
FOOTER
=========================================================
st.divider()
st.caption(
    "🩵 Study with Miku — your cute study companion 🎀"
)
