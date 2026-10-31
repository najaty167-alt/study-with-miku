
import streamlit as st
import streamlit.components.v1 as components
import json
import os
import time
import requests
from datetime import datetime, date

# -------------------------
# إعداد الصفحة
# -------------------------
st.set_page_config(
    page_title="Study with Miku",
    page_icon="୨୧",
    layout="wide"
)

DATA_FILE = "miku_data.json"

SUBJECTS = [
    "رياضيات متقدمة",
    "رياضيات أساسية",
    "فيزياء",
    "كيمياء",
    "أحياء",
    "علوم البيئة",
    "اللغة العربية",
    "اللغة الإنجليزية",
    "اللغة الفرنسية",
    "تاريخ",
    "جغرافيا",
    "دراسات اجتماعية",
    "تربية إسلامية",
    "فنون",
    "موسيقى",
    "تقنية",
    "رياضة"
]

# -------------------------
# تحميل وحفظ البيانات
# -------------------------
def load_data():
    default_data = {
        "tasks": [],
        "xp": 0
    }

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                saved = json.load(file)

            default_data["tasks"] = saved.get("tasks", [])
            default_data["xp"] = saved.get("xp", 0)

        except Exception:
            pass

    return default_data


def save_data():
    data = {
        "tasks": st.session_state.tasks,
        "xp": st.session_state.xp
    }

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if "loaded" not in st.session_state:
    saved_data = load_data()
    st.session_state.tasks = saved_data["tasks"]
    st.session_state.xp = saved_data["xp"]
    st.session_state.page = "الرئيسية"
    st.session_state.chat_history = []
    st.session_state.loaded = True


if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# التصميم الوردي
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Baloo 2', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fff7fb, #ffeaf4, #fff0f7);
    color: #70465d;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffdce9, #fff0f6);
    border-right: 2px solid #f8c7dc;
}

h1, h2, h3 {
    color: #bd7098 !important;
}

p, label, span {
    color: #79546a;
}

div.stButton > button {
    background: linear-gradient(135deg, #f6b8d3, #e99fc2);
    color: white;
    border: none;
    border-radius: 18px;
    padding: 10px 22px;
    font-weight: 700;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #df8eb5;
    color: white;
    transform: translateY(-2px);
}

div[data-testid="stForm"] {
    background: #fffafd;
    border: 1px solid #f4c8dc;
    border-radius: 20px;
    padding: 18px;
}

div[data-testid="stMetric"] {
    background: #fffafd;
    border: 1px solid #f4c8dc;
    border-radius: 18px;
    padding: 15px;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stDateInput input {
    border-radius: 13px !important;
    background: #fffafd !important;
}

hr {
    border-color: #f3c5da;
}

.miku-card {
    background: linear-gradient(135deg, #fffafd, #ffe5f0);
    border: 2px solid #f4c2d9;
    border-radius: 25px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 5px 20px #e8a9c522;
}

.miku-face {
    font-size: 75px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# القائمة الجانبية
# -------------------------
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>୨୧ Study with Miku</h1>",
                unsafe_allow_html=True)

    st.markdown("<p style='text-align:center;'>ذاكري معي بكل حب ♡</p>",
                unsafe_allow_html=True)

    st.markdown("---")

    pages = [
        "الرئيسية",
        "المهام الدراسية",
        "ميكو الذكية",
        "جلسة مذاكرة",
        "إنجازاتي"
    ]

    for page in pages:
        if st.button(
            page,
            key="nav_" + page,
            use_container_width=True
        ):
            st.session_state.page = page
            st.rerun()

    st.markdown("---")
    st.markdown("୨୧ لا تنسي أن كل خطوة صغيرة تصنع إنجازًا كبيرًا!")

# -------------------------
# الصفحة الرئيسية
# -------------------------
if st.session_state.page == "الرئيسية":

    st.title("مرحبًا بكِ في Study with Miku ♡")
    st.write("مساحة لطيفة للدراسة وتنظيم مهامك وتحقيق أهدافك.")

    st.markdown("""
    <div class="miku-card">
        <div class="miku-face">🎀</div>
        <h2>أهلًا! أنا ميكو</h2>
        <p>هيا ندرس معًا ونحقق إنجازات جديدة اليوم!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    completed = sum(
        1 for task in st.session_state.tasks
        if task.get("done", False)
    )

    total = len(st.session_state.tasks)

    col1, col2, col3 = st.columns(3)

    col1.metric("⭐ نقاطك", st.session_state.xp)
    col2.metric("📚 مهامك", total)
    col3.metric("🌸 المهام المكتملة", completed)

    st.subheader("إنجازك الدراسي")

    if total > 0:
        progress = completed / total
        st.progress(progress)
        st.write(f"أنجزتِ {completed} من {total} مهام.")
    else:
        st.info("لم تضيفي أي مهمة بعد. ابدئي بإضافة أول مهمة!")

# -------------------------
# صفحة المهام
# -------------------------
elif st.session_state.page == "المهام الدراسية":

    st.title("📚 مهامي الدراسية")
    st.write("رتبي واجباتك وتابعي إنجازاتك.")

    with st.form("add_task_form", clear_on_submit=True):

        task_name = st.text_input("اسم المهمة")

        subject = st.selectbox(
            "المادة",
            SUBJECTS
        )

        priority = st.selectbox(
            "الأولوية",
            ["عالية", "متوسطة", "منخفضة"]
        )

        due_date = st.date_input(
            "موعد التسليم",
            value=date.today()
        )

        submitted = st.form_submit_button("إضافة المهمة 🎀")

        if submitted:
            if task_name.strip():
                st.session_state.tasks.append({
                    "name": task_name.strip(),
                    "subject": subject,
                    "priority": priority,
                    "due": due_date.isoformat(),
                    "done": False
                })

                save_data()
                st.success("تمت إضافة المهمة بنجاح ♡")
                st.rerun()

            else:
                st.warning("اكتبي اسم المهمة أولًا.")

    st.markdown("---")
    st.subheader("قائمة المهام")

    if not st.session_state.tasks:
        st.info("لا توجد مهام حاليًا. استمتعي بوقتك!")

    for index, task in enumerate(st.session_state.tasks):

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### {task['name']}")
                st.write(f"📖 المادة: {task['subject']}")
                st.write(f"⭐ الأولوية: {task['priority']}")
                st.write(f"📅 التسليم: {task['due']}")

                if task.get("done", False):
                    st.success("تم إنجاز هذه المهمة!")

            with col2:

                if not task.get("done", False):

                    if st.button("إنجاز ✓", key=f"done_{index}"):

                        st.session_state.tasks[index]["done"] = True
                        st.session_state.xp += 20

                        save_data()
                        st.success("رائع! حصلتِ على 20 نقطة 🎀")
                        st.rerun()

                else:

                    if st.button("حذف المهمة", key=f"delete_{index}"):

                        st.session_state.tasks.pop(index)
                        save_data()
                        st.rerun()

# -------------------------
# ميكو الذكية - Gemini AI
# -------------------------
elif st.session_state.page == "ميكو الذكية":

    st.title("🎀 تحدثي مع ميكو الذكية")
    st.write("اسألي ميكو عن دروسك أو واجباتك، وستساعدك خطوة بخطوة.")

    st.markdown("""
    <div class="miku-card">
        <div class="miku-face">🌸</div>
        <h3>أنا ميكو، مساعدتك الدراسية!</h3>
        <p>اسأليني عن أي درس وسأشرح لكِ بطريقة سهلة وواضحة.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # قراءة المفتاح من Streamlit Secrets
    api_key = ""

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

    # عرض المحادثة السابقة
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # مسح المحادثة
    if st.button("مسح المحادثة 🧹"):
        st.session_state.chat_history = []
        st.rerun()

    prompt = st.chat_input("اكتبي سؤالك لميكو هنا...")

    if prompt:

        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        if not api_key:

            answer = (
                "لم أجد مفتاح Gemini! 🎀\n\n"
                "تأكدي من إضافة المفتاح في Streamlit Secrets "
                "بالاسم التالي تمامًا:\n\n"
                "`GEMINI_API_KEY`\n\n"
                "لا تضعي المفتاح داخل الكود أو ترسليه لأحد."
            )

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

            with st.chat_message("assistant"):
                st.markdown(answer)

        else:

            with st.chat_message("assistant"):

                with st.spinner("ميكو تفكر في إجابتك... 🌸"):

                    try:

                        url = (
                            "https://generativelanguage.googleapis.com/"
                            "v1beta/models/gemini-2.5-flash:generateContent"
                        )

                        # تجهيز آخر الرسائل مع الحفاظ على ترتيب الأدوار
                        history = st.session_state.chat_history[:-1][-20:]

                        contents = []

                        for item in history:
                            role = (
                                "model"
                                if item["role"] == "assistant"
                                else "user"
                            )

                            # دمج الرسائل المتتالية من الدور نفسه
                            if contents and contents[-1]["role"] == role:
                                contents[-1]["parts"][0]["text"] += (
                                    "\n" + item["content"]
                                )
                            else:
                                contents.append({
                                    "role": role,
                                    "parts": [
                                        {"text": item["content"]}
                                    ]
                                })

                        # إضافة السؤال الحالي
                        if contents and contents[-1]["role"] == "user":
                            contents[-1]["parts"][0]["text"] += (
                                "\n" + prompt
                            )
                        else:
                            contents.append({
                                "role": "user",
                                "parts": [{"text": prompt}]
                            })

                        payload = {
                            "system_instruction": {
                                "parts": [{
                                    "text": (
                                        "أنتِ ميكو، مساعدة دراسية لطيفة "
                                        "تشرح باللغة العربية الواضحة. "
                                        "استخدمي خطوات مرتبة وأمثلة بسيطة "
                                        "ومناسبة لمستوى الطالبة. "
                                        "ساعدي في المواد الدراسية، "
                                        "ولا تخترعي معلومات عند عدم التأكد. "
                                        "إذا كان السؤال باللغة الإنجليزية "
                                        "فيمكنك شرحه بالعربية."
                                    )
                                }]
                            },
                            "contents": contents,
                            "generationConfig": {
                                "temperature": 0.7,
                                "maxOutputTokens": 2048
                            }
                        }

                        response = requests.post(
                            url,
                            headers={
                                "Content-Type": "application/json",
                                "x-goog-api-key": api_key
                            },
                            json=payload,
                            timeout=45
                        )

                        if response.status_code == 200:

                            result = response.json()

                            answer = (
                                result["candidates"][0]
                                ["content"]["parts"][0]["text"]
                            )

                        else:

                            try:
                                error_data = response.json()
                                error_message = error_data.get(
                                    "error", {}
                                ).get("message", "خطأ غير معروف")
                            except Exception:
                                error_message = response.text[:500]

                            answer = (
                                f"لم أتمكن من الاتصال بميكو حاليًا. 🌸\n\n"
                                f"رمز الخطأ: {response.status_code}\n\n"
                                f"تفاصيل الخطأ: {error_message}\n\n"
                                "تحققي من صلاحية المفتاح وإعدادات Gemini "
                                "ثم حاولي مرة أخرى."
                            )

                    except requests.exceptions.Timeout:

                        answer = (
                            "استغرق الاتصال وقتًا طويلًا. "
                            "تأكدي من الإنترنت ثم حاولي مرة أخرى. 🌸"
                        )

                    except requests.exceptions.ConnectionError:

                        answer = (
                            "لم أستطع الاتصال بالخدمة. "
                            "تحققي من اتصال الإنترنت وحاولي مجددًا."
                        )

                    except (KeyError, IndexError, TypeError):

                        answer = (
                            "وصلني رد غير متوقع من Gemini. "
                            "حاولي إرسال السؤال مرة أخرى."
                        )

                    except Exception as error:

                        answer = (
                            "حدث خطأ غير متوقع أثناء تشغيل ميكو.\n\n"
                            f"تفاصيل الخطأ: {str(error)}"
                        )

                st.markdown(answer)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

        st.rerun()

# -------------------------
# جلسة المذاكرة
# -------------------------
elif st.session_state.page == "جلسة مذاكرة":

    st.title("⏰ جلسة مذاكرة مع ميكو")
    st.write("اختاري مدة الدراسة وابدئي جلستك.")

    study_minutes = st.number_input(
        "مدة الدراسة بالدقائق",
        min_value=1,
        max_value=180,
        value=60
    )

    break_minutes = st.number_input(
        "مدة الاستراحة بالدقائق",
        min_value=1,
        max_value=60,
        value=10
    )

    if st.button("ابدئي جلسة المذاكرة 🎀"):

        total_seconds = int(study_minutes * 60)

        components.html(
            f"""
            <div style="
                text-align:center;
                background:#fff0f7;
                border:2px solid #f2b9d2;
                border-radius:25px;
                padding:25px;
                font-family:sans-serif;
                color:#bd7098;
            ">
                <h2>🌸 وقت المذاكرة 🌸</h2>
                <div id="timer" style="
                    font-size:55px;
                    font-weight:bold;
                ">00:00</div>
                <p>بالتوفيق! أنتِ قادرة على الإنجاز ♡</p>
            </div>

            <script>
                let remaining = {total_seconds};
                const timer = document.getElementById("timer");

                function updateTimer() {{
                    let minutes = Math.floor(remaining / 60);
                    let seconds = remaining % 60;

                    timer.textContent =
                        String(minutes).padStart(2, "0") + ":" +
                        String(seconds).padStart(2, "0");

                    if (remaining <= 0) {{
                        timer.textContent = "انتهى الوقت! 🎀";
                        return;
                    }}

                    remaining--;
                    setTimeout(updateTimer, 1000);
                }}

                updateTimer();
            </script>
            """,
            height=230
        )

    st.markdown("---")
    st.subheader("بعد انتهاء المذاكرة")

    st.write(
        f"استمتعي باستراحة مدتها {break_minutes} دقيقة "
        "ثم عودي بنشاط! ♡"
    )

# -------------------------
# صفحة الإنجازات
# -------------------------
elif st.session_state.page == "إنجازاتي":

    st.title("🏆 إنجازاتي")

    xp = st.session_state.xp
    level = (xp // 100) + 1
    progress = (xp % 100) / 100

    st.metric("⭐ مجموع النقاط", xp)
    st.metric("🌸 مستواك الحالي", level)

    st.subheader("التقدم نحو المستوى التالي")
    st.progress(progress)
    st.write(f"{xp % 100} / 100 نقطة")

    completed = sum(
        1 for task in st.session_state.tasks
        if task.get("done", False)
    )

    st.markdown("---")
    st.subheader("شارات الإنجاز")

    achievements = [
        ("🌷", "أول خطوة", completed >= 1),
        ("🎀", "ثلاث مهام مكتملة", completed >= 3),
        ("🌸", "خمس مهام مكتملة", completed >= 5),
        ("👑", "عشر مهام مكتملة", completed >= 10),
        ("⭐", "وصلتِ إلى 100 نقطة", xp >= 100),
        ("💖", "وصلتِ إلى 500 نقطة", xp >= 500)
    ]

    for emoji, title, unlocked in achievements:

        if unlocked:
            st.success(f"{emoji} {title}")
        else:
            st.info(f"🔒 {title}")

    st.markdown("---")
    st.write("استمري، فكل إنجاز يستحق الاحتفال! ୨୧")
