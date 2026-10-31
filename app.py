
import os
import time
import base64
from datetime import datetime

import requests
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# STUDY WITH MIKU — soft crystal / glass dashboard
# Optional local files: miku.png, bg.png or bg.jpg
# Optional Streamlit secret: GEMINI_API_KEY
# =========================================================

st.set_page_config(
    page_title="Study with Miku",
    page_icon="🩵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- State ----------
DEFAULTS = {
    "page": "الرئيسية",
    "tasks": [],
    "xp": 0,
    "chat_history": [],
    "timer_mode": "مذاكرة",
    "timer_minutes": 25,
    "break_minutes": 5,
    "timer_end": None,
    "timer_running": False,
    "timer_paused_remaining": None,
    "timer_completed_sessions": 0,
    "task_counter": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------- Helpers ----------

def image_as_data_uri(path):
    if not os.path.exists(path):
        return ""

    ext = os.path.splitext(path)[1].lower()
    mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"

    with open(path, "rb") as file:
        return f"data:{mime};base64,{base64.b64encode(file.read()).decode()}"


miku_uri = image_as_data_uri("miku.png")
background_uri = (
    image_as_data_uri("bg.png")
    or image_as_data_uri("bg.jpg")
)


def go(page):
    st.session_state.page = page
    st.rerun()


def completed_count():
    return sum(
        1 for task in st.session_state.tasks
        if task["done"]
    )


def level_info():
    xp = st.session_state.xp
    return xp // 100 + 1, xp % 100


# ---------- Gemini AI ----------

def ask_miku(message):

    try:
        api_key = st.secrets.get(
            "GEMINI_API_KEY",
            os.getenv("GEMINI_API_KEY", "")
        )
    except Exception:
        api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        return (
            "أنا ميكو 🩵 أحتاج إلى تفعيل مفتاح Gemini أولًا. "
            "أضيفي GEMINI_API_KEY إلى إعدادات Secrets في التطبيق."
        )

    # لا نرسل الرسالة الحالية مرتين
    previous_messages = st.session_state.chat_history[:-1]

    history = []

    for item in previous_messages[-12:]:

        role = (
            "user"
            if item["role"] == "user"
            else "model"
        )

        content = item.get("content", "").strip()

        if not content:
            continue

        history.append({
            "role": role,
            "parts": [{"text": content}]
        })

    # إضافة الرسالة الحالية مرة واحدة فقط
    history.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    payload = {
        "system_instruction": {
            "parts": [{
                "text": (
                    "اسمك ميكو. أنت مساعدة دراسية ذكية ولطيفة. "
                    "تحدثي باللغة العربية الواضحة. "
                    "اشرحي الدروس خطوة بخطوة وبمستوى مناسب للطالب. "
                    "استخدمي أمثلة واضحة عند الحاجة. "
                    "لا تختلقي معلومات، وإذا لم تعرفي الإجابة فقولي ذلك. "
                    "ساعدي في الرياضيات والعلوم واللغات وجميع المواد "
                    "والواجبات وتنظيم المذاكرة. "
                    "كوني مشجعة وهادئة دون مبالغة."
                )
            }]
        },
        "contents": history,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1500
        }
    }

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-2.5-flash:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    # إعادة المحاولة عند أخطاء الاتصال المؤقتة
    for attempt in range(3):

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=45
            )

            if response.status_code == 200:

                data = response.json()

                candidates = data.get("candidates", [])

                if not candidates:
                    return (
                        "وصلني طلبك، لكن Gemini لم يُرجع إجابة. "
                        "جرّبي صياغة السؤال بطريقة أخرى 🩵"
                    )

                parts = candidates[0].get(
                    "content", {}
                ).get("parts", [])

                answer = "\n".join(
                    part.get("text", "")
                    for part in parts
                    if part.get("text")
                )

                return answer or "لم تصلني إجابة نصية. حاولي مرة أخرى."

            # أخطاء مؤقتة: نحاول الاتصال مجددًا
            if response.status_code in (429, 500, 502, 503, 504):
                if attempt < 2:
                    time.sleep(attempt + 1)
                    continue

            try:
                error_data = response.json()
                error_message = (
                    error_data.get("error", {}).get(
                        "message", ""
                    )
                )
            except Exception:
                error_message = ""

            if response.status_code == 503:
                return (
                    "خوادم Gemini مشغولة حاليًا 🩵 "
                    "حاولت الاتصال مجددًا، لكن الخدمة لم تستجب. "
                    "انتظري قليلًا ثم أعيدي إرسال سؤالك."
                )

            if response.status_code == 429:
                return (
                    "وصلنا إلى حد الطلبات المسموح به مؤقتًا. "
                    "انتظري قليلًا ثم حاولي مرة أخرى."
                )

            if response.status_code in (400, 403, 404):
                return (
                    f"تعذّر تنفيذ الطلب (رمز {response.status_code}). "
                    "تحققي من صلاحية المفتاح وإعدادات Gemini. "
                    + error_message
                )

            return (
                f"حدث خطأ في الاتصال (رمز {response.status_code}). "
                + error_message
            )

        except requests.exceptions.Timeout:
            if attempt < 2:
                time.sleep(attempt + 1)
                continue

            return (
                "استغرق الاتصال وقتًا أطول من المعتاد. "
                "تحققي من الإنترنت وحاولي مرة أخرى 🩵"
            )

        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(attempt + 1)
                continue

            return (
                "تعذّر الاتصال بميكو. تحققي من الإنترنت "
                "وحاولي مرة أخرى 🩵"
            )

        except Exception:
            return (
                "حدث خلل غير متوقع. حاولي مرة أخرى بعد قليل 🩵"
            )

    return "تعذّر الاتصال بميكو حاليًا. حاولي مرة أخرى."


# ---------- Styling ----------

bg_rule = (
    f"background-image: linear-gradient(120deg, rgba(239,251,255,.86), rgba(248,246,255,.90)), url('{background_uri}');"
    if background_uri else
    "background-image: radial-gradient(circle at 12% 8%, #d7f8ff 0, transparent 30%), radial-gradient(circle at 90% 12%, #eee3ff 0, transparent 28%), linear-gradient(135deg,#f5fcff,#f5f1ff 55%,#fff8fd);"
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Tajawal:wght@400;500;600;700;800&display=swap');

:root {{
 --ink:#253451;
 --muted:#71819b;
 --cyan:#66d9ed;
 --blue:#8cbcff;
 --lilac:#c6a8ff;
 --pink:#ffcae4;
 --glass:rgba(255,255,255,.68);
}}

html, body, [class*="css"] {{
 font-family:'Tajawal','Baloo 2',sans-serif;
}}

.stApp {{
 {bg_rule}
 background-size:cover;
 background-attachment:fixed;
 color:var(--ink);
}}

header[data-testid="stHeader"] {{
 background:transparent;
}}

footer {{
 visibility:hidden;
}}

.block-container {{
 padding-top:1.35rem;
 padding-bottom:2.5rem;
 max-width:1450px;
}}

[data-testid="stSidebar"] {{
 background:rgba(255,255,255,.62);
 backdrop-filter:blur(24px);
 border-right:1px solid rgba(255,255,255,.8);
}}

[data-testid="stSidebar"] * {{
 color:var(--ink);
}}

h1,h2,h3 {{
 color:var(--ink)!important;
 font-weight:800!important;
}}

p, label, .stMarkdown {{
 color:var(--ink);
}}

div[data-testid="stMetric"] {{
 background:rgba(255,255,255,.62);
 border:1px solid rgba(255,255,255,.95);
 border-radius:22px;
 padding:15px 18px;
 box-shadow:0 12px 30px rgba(86,128,171,.10);
}}

div[data-testid="stMetricLabel"] {{
 color:#6f819d!important;
}}

div[data-testid="stMetricValue"] {{
 color:#34476b!important;
}}

.stButton>button, .stFormSubmitButton>button {{
 border:1px solid rgba(255,255,255,.96)!important;
 border-radius:16px!important;
 background:linear-gradient(135deg,rgba(255,255,255,.95),rgba(224,248,255,.85))!important;
 color:#34476b!important;
 font-weight:800!important;
 min-height:2.7rem;
 box-shadow:0 7px 18px rgba(93,151,190,.13), inset 0 1px 0 white!important;
 transition:all .18s ease!important;
}}

.stButton>button:hover, .stFormSubmitButton>button:hover {{
 transform:translateY(-2px);
 border-color:#8de4f2!important;
 box-shadow:0 12px 24px rgba(93,151,190,.2)!important;
}}

.stTextInput input, .stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stNumberInput input {{
 border-radius:14px!important;
 background:rgba(255,255,255,.82)!important;
}}

div[data-testid="stProgressBar"] > div > div {{
 background:linear-gradient(90deg,#69dbea,#a8baff,#f5b9dd)!important;
}}

.glass-card {{
 background:rgba(255,255,255,.62);
 border:1px solid rgba(255,255,255,.9);
 border-radius:26px;
 padding:22px;
 box-shadow:0 18px 45px rgba(77,116,163,.12);
 backdrop-filter:blur(22px);
 margin-bottom:16px;
}}

.hero {{
 position:relative;
 overflow:hidden;
 padding:30px 30px 26px;
 border-radius:30px;
 background:linear-gradient(125deg,rgba(255,255,255,.82),rgba(224,248,255,.65),rgba(244,232,255,.72));
 border:1px solid rgba(255,255,255,.95);
 box-shadow:0 20px 50px rgba(100,138,180,.15);
}}

.hero:before {{
 content:'';
 position:absolute;
 width:240px;
 height:240px;
 right:-65px;
 top:-95px;
 border-radius:50%;
 background:rgba(130,226,244,.22);
 filter:blur(2px);
}}

.eyebrow {{
 color:#6d94b9;
 font-size:13px;
 letter-spacing:2px;
 font-weight:800;
}}

.hero-title {{
 font-size:clamp(28px,3.4vw,46px);
 line-height:1.15;
 font-weight:800;
 color:#34476b;
 margin:7px 0;
}}

.hero-sub {{
 color:#71819b;
 font-size:16px;
 line-height:1.8;
 max-width:650px;
}}

.pill {{
 display:inline-block;
 border-radius:999px;
 padding:7px 12px;
 background:rgba(255,255,255,.78);
 border:1px solid white;
 color:#6685a8;
 font-size:12px;
 font-weight:800;
 margin:3px 4px 3px 0;
}}

.section-title {{
 font-size:22px;
 font-weight:800;
 margin:8px 0 14px;
 color:#34476b;
}}

.task-row {{
 background:rgba(255,255,255,.68);
 border:1px solid rgba(255,255,255,.95);
 border-radius:18px;
 padding:13px 16px;
 margin-bottom:9px;
}}

.small-muted {{
 color:#7a8aa3;
 font-size:13px;
}}

.miku-orb {{
 width:180px;
 height:180px;
 margin:auto;
 border-radius:50%;
 display:flex;
 align-items:center;
 justify-content:center;
 background:radial-gradient(circle at 35% 25%,#fff 0,#e5fbff 32%,#c8d8ff 68%,#ead7ff 100%);
 border:1px solid rgba(255,255,255,.95);
 box-shadow:0 0 0 10px rgba(255,255,255,.24),0 22px 55px rgba(112,145,208,.22);
 animation:floaty 4s ease-in-out infinite;
 overflow:hidden;
}}

.miku-orb img {{
 width:100%;
 height:100%;
 object-fit:contain;
 filter:drop-shadow(0 12px 14px rgba(83,113,172,.20));
}}

.miku-fallback {{
 font-size:66px;
 filter:drop-shadow(0 8px 8px rgba(94,131,177,.18));
}}

@keyframes floaty {{
 0%,100% {{transform:translateY(0) rotate(-1deg)}}
 50% {{transform:translateY(-9px) rotate(1deg)}}
}}

div[data-testid="stChatMessage"] {{
 background:rgba(255,255,255,.62);
 border:1px solid rgba(255,255,255,.8);
 border-radius:18px;
}}

hr {{
 border-color:rgba(155,192,224,.3);
}}
</style>
""", unsafe_allow_html=True)


# ---------- Sidebar navigation ----------

with st.sidebar:

    st.markdown(
        "<div style='text-align:center;padding:10px 0 18px'>",
        unsafe_allow_html=True
    )

    if miku_uri:
        st.markdown(
            f"<img src='{miku_uri}' style='width:92px;height:92px;object-fit:contain;filter:drop-shadow(0 8px 12px #a8d8ed)'/>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='font-size:54px'>🩵</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div style='font-size:22px;font-weight:800;color:#34476b'>Study with Miku</div><div class='small-muted'>مساحة مذاكرتك اللطيفة</div></div>",
        unsafe_allow_html=True
    )

    st.divider()

    pages = [
        ("🏠", "الرئيسية"),
        ("🗂️", "مهامي وواجباتي"),
        ("💬", "اسألي ميكو"),
        ("⏳", "جلسة المذاكرة"),
        ("🏆", "إنجازاتي"),
    ]

    for icon, label in pages:
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{label}",
            use_container_width=True
        ):
            go(label)

    st.divider()

    level, level_xp = level_info()

    st.markdown(f"**المستوى {level}**")
    st.progress(level_xp / 100)

    st.caption(
        f"✨ {st.session_state.xp} XP · {level_xp}/100 للمستوى التالي"
    )

    st.caption("صمّمي يومك على مهلك 🩵")


# ---------- Timer display fragment ----------
# يحدث المؤقت وحده كل ثانية دون إعادة تشغيل بقية التطبيق.

@st.fragment(run_every=1)
def timer_display():

    st.markdown(
        "<div class='glass-card' style='text-align:center;padding:28px 18px'>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='eyebrow'>TIME TO FOCUS</div>",
        unsafe_allow_html=True
    )

    if (
        st.session_state.timer_running
        and st.session_state.timer_end
    ):
        remaining = max(
            0,
            int(st.session_state.timer_end - time.time())
        )

    elif st.session_state.timer_paused_remaining is not None:
        remaining = max(
            0,
            int(st.session_state.timer_paused_remaining)
        )

    else:
        current_minutes = (
            st.session_state.timer_minutes
            if st.session_state.timer_mode == "مذاكرة"
            else st.session_state.break_minutes
        )

        remaining = int(current_minutes * 60)

    mins, secs = divmod(remaining, 60)

    st.markdown(
        f"<div style='font-size:clamp(46px,6vw,72px);font-weight:800;letter-spacing:3px;color:#536b9a;margin:10px 0'>{mins:02d}:{secs:02d}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='pill'>{'📚 وقت المذاكرة' if st.session_state.timer_mode == 'مذاكرة' else '🌿 وقت الاستراحة'}</div>",
        unsafe_allow_html=True
    )

    st.write("")

    st.metric(
        "جلسات مكتملة",
        st.session_state.timer_completed_sessions
    )

    # إنهاء الجلسة مرة واحدة فقط
    if (
        st.session_state.timer_running
        and remaining == 0
    ):

        st.session_state.timer_running = False
        st.session_state.timer_end = None
        st.session_state.timer_paused_remaining = None

        if st.session_state.timer_mode == "مذاكرة":

            st.session_state.timer_completed_sessions += 1
            st.session_state.xp += 10

            st.success(
                "انتهت جلسة التركيز! حصلتِ على 10 XP 🎉"
            )

        else:
            st.success(
                "انتهت الاستراحة، تقدرين تبدئين من جديد 🩵"
            )

    elif st.session_state.timer_running:
        st.info("المؤقت يعمل — يمكنك الانتقال بين الصفحات.")

    else:
        st.caption("ابدئي المؤقت عندما تكونين جاهزة.")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Header ----------

level, level_xp = level_info()
page = st.session_state.page


# =========================================================
# HOME
# =========================================================

if page == "الرئيسية":

    left, right = st.columns(
        [1.55, 1],
        gap="large"
    )

    with left:

        st.markdown(f"""
        <div class="hero">
          <div class="eyebrow">YOUR COZY STUDY SPACE ✦</div>
          <div class="hero-title">أهلًا بعودتك! 🩵<br>خلّينا ننجز شيئًا جميلًا.</div>
          <div class="hero-sub">كل خطوة صغيرة تقرّبك من هدفك. رتّبي واجباتك، ابدئي جلسة تركيز، وخلي ميكو تساعدك في الطريق.</div>
          <span class="pill">✧ خطوة بخطوة</span>
          <span class="pill">♡ إنجاز بلا ضغط</span>
          <span class="pill">✦ {datetime.now().strftime('%d / %m / %Y')}</span>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "المهام الكلية",
            len(st.session_state.tasks)
        )

        m2.metric(
            "المهام المنجزة",
            completed_count()
        )

        m3.metric(
            "نقاط الخبرة",
            st.session_state.xp
        )

        st.markdown(
            "<div class='section-title'>✨ اختصارات سريعة</div>",
            unsafe_allow_html=True
        )

        q1, q2, q3 = st.columns(3)

        with q1:
            if st.button("＋ إضافة واجب", use_container_width=True):
                go("مهامي وواجباتي")

        with q2:
            if st.button("⏳ ابدئي المذاكرة", use_container_width=True):
                go("جلسة المذاكرة")

        with q3:
            if st.button("💬 اسألي ميكو", use_container_width=True):
                go("اسألي ميكو")

        st.markdown(
            "<div class='section-title'>📌 أقرب المهام</div>",
            unsafe_allow_html=True
        )

        pending = [
            t for t in st.session_state.tasks
            if not t["done"]
        ]

        if pending:

            for task in pending[:4]:

                st.markdown(
                    f"<div class='task-row'><b>{task['subject']}</b>　{task['name']}<div class='small-muted'>الأولوية: {task['priority']} · {task['due'] or 'بدون موعد محدد'}</div></div>",
                    unsafe_allow_html=True
                )

        else:
            st.info(
                "ما عندك مهام معلّقة الآن. أضيفي أول واجب من صفحة «مهامي وواجباتي» 🌷"
            )

    with right:

        st.markdown(
            "<div class='glass-card' style='text-align:center'>",
            unsafe_allow_html=True
        )

        if miku_uri:

            st.markdown(
                f"<div class='miku-orb'><img src='{miku_uri}' alt='Miku'></div>",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                "<div class='miku-orb'><div class='miku-fallback'>🩵</div></div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "<h3 style='margin:18px 0 2px'>ميكو هنا معك!</h3><div class='small-muted'>رفيقتك في الدراسة والتنظيم</div>",
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            "<div style='background:rgba(226,248,255,.72);padding:14px;border-radius:18px;text-align:right;line-height:1.9'>«مو لازم تخلصين كل شيء مرة وحدة. اختاري مهمة واحدة، ونبدأ فيها مع بعض.»</div>",
            unsafe_allow_html=True
        )

        if st.button("تحدثي مع ميكو 🕊️", use_container_width=True):
            go("اسألي ميكو")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            "<div class='glass-card'><div class='section-title'>🌱 تقدّمك اليوم</div>",
            unsafe_allow_html=True
        )

        total = len(st.session_state.tasks)
        done = completed_count()

        progress = done / total if total else 0

        st.progress(progress)

        st.write(
            f"أنجزتِ **{done}** من أصل **{total}** مهمة."
        )

        st.caption("كل مهمة مكتملة تمنحك 25 XP.")

        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TASKS
# =========================================================

elif page == "مهامي وواجباتي":

    st.markdown(
        "<div class='hero'><div class='eyebrow'>PLAN · PRIORITIZE · COMPLETE</div><div class='hero-title'>مهامي وواجباتي 🗂️</div><div class='hero-sub'>اجمعي واجباتك في مكان واحد، وحددي المادة والأولوية والموعد، ثم علّمي عليها عند الإنجاز.</div></div>",
        unsafe_allow_html=True
    )

    st.write("")

    with st.container(border=True):

        st.markdown(
            "<div class='section-title'>＋ إضافة مهمة جديدة</div>",
            unsafe_allow_html=True
        )

        with st.form("add_task_form", clear_on_submit=True):

            name = st.text_input(
                "اسم الواجب أو المهمة",
                placeholder="مثال: حل أسئلة الفيزياء صفحة ٢٩"
            )

            c1, c2 = st.columns(2)

            with c1:

                subject_options = [
                    "رياضيات",
                    "رياضيات متقدمة",
                    "إحصاء",
                    "هندسة",
                    "فيزياء",
                    "كيمياء",
                    "أحياء",
                    "علوم عامة",
                    "علوم بيئية",
                    "علوم الأرض",
                    "فلك",
                    "لغة عربية",
                    "لغة إنجليزية",
                    "لغة فرنسية",
                    "لغة إسبانية",
                    "لغة ألمانية",
                    "تربية إسلامية",
                    "حضارة إسلامية",
                    "تاريخ",
                    "جغرافيا",
                    "دراسات اجتماعية",
                    "فلسفة",
                    "تقنية المعلومات",
                    "حاسوب",
                    "برمجة",
                    "ذكاء اصطناعي",
                    "فنون تشكيلية",
                    "تربية فنية",
                    "موسيقى",
                    "تصميم",
                    "تربية رياضية",
                    "مهارات حياتية",
                    "اقتصاد",
                    "إدارة أعمال",
                    "أخرى"
                ]

                subject = st.selectbox(
                    "المادة",
                    subject_options
                )

                priority = st.selectbox(
                    "الأولوية",
                    ["عالية 🔴", "متوسطة 🟡", "منخفضة 🟢"]
                )

            with c2:

                due = st.date_input(
                    "موعد التسليم (اختياري)",
                    value=None
                )

                note = st.text_input(
                    "ملاحظة (اختيارية)",
                    placeholder="مثل: مراجعة القانون قبل الحل"
                )

            submitted = st.form_submit_button(
                "حفظ المهمة ✨",
                use_container_width=True
            )

            if submitted:

                if name.strip():

                    st.session_state.tasks.append({
                        "id": int(time.time() * 1000),
                        "name": name.strip(),
                        "subject": subject,
                        "priority": priority,
                        "due": due.strftime("%d/%m/%Y") if due else "",
                        "note": note.strip(),
                        "done": False,
                    })

                    st.success("انضافت المهمة إلى قائمتك 🩵")
                    st.rerun()

                else:
                    st.warning("اكتبي اسم المهمة أولًا.")

    st.write("")

    filter_choice = st.radio(
        "عرض المهام",
        ["الكل", "المعلّقة", "المنجزة"],
        horizontal=True
    )

    tasks = st.session_state.tasks

    if filter_choice == "المعلّقة":
        tasks = [t for t in tasks if not t["done"]]

    elif filter_choice == "المنجزة":
        tasks = [t for t in tasks if t["done"]]

    if not tasks:
        st.info(
            "القائمة فاضية حاليًا — أضيفي مهمة من النموذج أعلاه."
        )

    for task in tasks:

        with st.container(border=True):

            a, b, c = st.columns([0.12, 0.68, 0.2])

            with a:
                st.write("✅" if task["done"] else "📘")

            with b:

                title = (
                    f"~~{task['name']}~~"
                    if task["done"]
                    else task["name"]
                )

                st.markdown(f"**{title}**")

                st.caption(
                    f"{task['subject']} · {task['priority']} · {task['due'] or 'بدون موعد'}"
                )

                if task.get("note"):
                    st.caption(f"ملاحظة: {task['note']}")

            with c:

                if not task["done"]:

                    if st.button(
                        "تم الإنجاز +25 XP",
                        key=f"complete_{task['id']}",
                        use_container_width=True
                    ):

                        for item in st.session_state.tasks:

                            if (
                                item["id"] == task["id"]
                                and not item["done"]
                            ):

                                item["done"] = True
                                st.session_state.xp += 25
                                break

                        st.toast("رائعة! حصلتِ على 25 XP ✨")
                        st.rerun()

                else:

                    if st.button(
                        "إرجاع للمعلّقة",
                        key=f"undo_{task['id']}",
                        use_container_width=True
                    ):

                        for item in st.session_state.tasks:

                            if item["id"] == task["id"]:

                                item["done"] = False

                                st.session_state.xp = max(
                                    0,
                                    st.session_state.xp - 25
                                )

                                break

                        st.rerun()

                    if st.button(
                        "حذف",
                        key=f"delete_{task['id']}",
                        use_container_width=True
                    ):

                        st.session_state.tasks = [
                            x for x in st.session_state.tasks
                            if x["id"] != task["id"]
                        ]

                        st.rerun()


# =========================================================
# ASK MIKU
# =========================================================

elif page == "اسألي ميكو":

    st.markdown(
        "<div class='hero'><div class='eyebrow'>YOUR STUDY COMPANION</div><div class='hero-title'>اسألي ميكو 💬</div><div class='hero-sub'>اسألي عن درس، اطلبي شرحًا خطوة بخطوة، أو رتّبي خطة مذاكرة.</div></div>",
        unsafe_allow_html=True
    )

    st.write("")

    for msg in st.session_state.chat_history:

        with st.chat_message(
            msg["role"],
            avatar="🩵" if msg["role"] == "assistant" else "🌷"
        ):

            st.markdown(msg["content"])

    prompt = st.chat_input(
        "اكتبي سؤالك لميكو هنا..."
    )

    if prompt:

        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        with st.spinner("ميكو تفكر في إجابة مناسبة..."):

            answer = ask_miku(prompt)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "مسح المحادثة",
            use_container_width=True
        ):

            st.session_state.chat_history = []
            st.rerun()

    with c2:

        st.caption(
            "تأكدي من إعداد GEMINI_API_KEY في Secrets لتفعيل الردود الذكية."
        )


# =========================================================
# STUDY TIMER
# =========================================================

elif page == "جلسة المذاكرة":

    st.markdown(
        "<div class='hero'><div class='eyebrow'>FOCUS · REST · REPEAT</div><div class='hero-title'>جلسة المذاكرة ⏳</div><div class='hero-sub'>اختاري مدة التركيز والاستراحة. ابدئي المؤقت وخذي استراحة قصيرة بعد انتهاء الجلسة.</div></div>",
        unsafe_allow_html=True
    )

    st.write("")

    left, right = st.columns(
        [1.15, 0.85],
        gap="large"
    )

    with left:

        with st.container(border=True):

            st.markdown(
                "<div class='section-title'>إعداد الجلسة</div>",
                unsafe_allow_html=True
            )

            study_min = st.number_input(
                "مدة المذاكرة بالدقائق",
                min_value=1,
                max_value=180,
                value=int(st.session_state.timer_minutes),
                step=5
            )

            break_min = st.number_input(
                "مدة الاستراحة بالدقائق",
                min_value=1,
                max_value=60,
                value=int(st.session_state.break_minutes),
                step=1
            )

            mode = st.radio(
                "وضع الجلسة",
                ["مذاكرة", "استراحة"],
                horizontal=True,
                index=(
                    0
                    if st.session_state.timer_mode == "مذاكرة"
                    else 1
                )
            )

            st.session_state.timer_minutes = int(study_min)
            st.session_state.break_minutes = int(break_min)
            st.session_state.timer_mode = mode

            if st.button(
                "بدء / إعادة ضبط المؤقت",
                use_container_width=True
            ):

                mins = (
                    study_min
                    if mode == "مذاكرة"
                    else break_min
                )

                st.session_state.timer_end = (
                    time.time() + int(mins) * 60
                )

                st.session_state.timer_running = True
                st.session_state.timer_paused_remaining = None

                st.rerun()

            p1, p2 = st.columns(2)

            with p1:

                if st.button(
                    "إيقاف مؤقت",
                    use_container_width=True
                ):

                    if (
                        st.session_state.timer_running
                        and st.session_state.timer_end
                    ):

                        st.session_state.timer_paused_remaining = max(
                            0,
                            st.session_state.timer_end - time.time()
                        )

                        st.session_state.timer_running = False
                        st.rerun()

            with p2:

                if st.button(
                    "استئناف",
                    use_container_width=True
                ):

                    if (
                        not st.session_state.timer_running
                        and st.session_state.timer_paused_remaining is not None
                    ):

                        st.session_state.timer_end = (
                            time.time()
                            + st.session_state.timer_paused_remaining
                        )

                        st.session_state.timer_running = True
                        st.session_state.timer_paused_remaining = None

                        st.rerun()

            if st.button(
                "إنهاء الجلسة",
                use_container_width=True
            ):

                st.session_state.timer_running = False
                st.session_state.timer_end = None
                st.session_state.timer_paused_remaining = None

                st.rerun()

    with right:

        timer_display()


# =========================================================
# ACHIEVEMENTS
# =========================================================

elif page == "إنجازاتي":

    st.markdown(
        "<div class='hero'><div class='eyebrow'>EVERY LITTLE STEP COUNTS</div><div class='hero-title'>إنجازاتك 🏆</div><div class='hero-sub'>شاهدي كيف يتراكم تعبك الجميل إلى نقاط وخطوات واضحة.</div></div>",
        unsafe_allow_html=True
    )

    st.write("")

    level, level_xp = level_info()

    a, b, c = st.columns(3)

    a.metric(
        "نقاط الخبرة XP",
        st.session_state.xp
    )

    b.metric(
        "المستوى الحالي",
        level
    )

    c.metric(
        "مهام مكتملة",
        completed_count()
    )

    st.markdown(
        "<div class='glass-card'>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='section-title'>المستوى {level}</div>",
        unsafe_allow_html=True
    )

    st.progress(level_xp / 100)

    st.caption(
        f"باقي {100 - level_xp} XP للوصول إلى المستوى التالي."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='glass-card'><div class='section-title'>🌟 كيف تجمعين النقاط؟</div><p>• إكمال واجب: 25 XP</p><p>• إنهاء جلسة مذاكرة: 10 XP</p><p>• كلما واصلتِ، ارتفع مستواك!</p></div>",
        unsafe_allow_html=True
    )


# ---------- Footer ----------

st.markdown(
    "<div style='text-align:center;color:#8798b2;font-size:12px;padding:20px 0 0'>Made with 🩵 for your study journey · Study with Miku</div>",
    unsafe_allow_html=True
)
