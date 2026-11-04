import streamlit as st
import streamlit.components.v1 as components
import requests
import time
import os
import uuid
from datetime import date, datetime

==========================================

إعداد الصفحة

==========================================

st.set_page_config(
page_title="Study with Miku",
page_icon="୨୧",
layout="wide",
initial_sidebar_state="expanded"
)

==========================================

تهيئة البيانات

==========================================

DEFAULTS = {
"tasks": [],
"xp": 0,
"chat_history": [],
"page": "الرئيسية",
"timer_mode": "مذاكرة",
"timer_minutes": 25,
"timer_running": False,
"timer_end": None,
"timer_paused_remaining": None,
"completed_sessions": 0,
"completed_tasks": 0,
"api_error": ""
}

for key, value in DEFAULTS.items():
if key not in st.session_state:
st.session_state[key] = value

SUBJECTS = [
"رياضيات متقدمة",
"رياضيات أساسية",
"فيزياء",
"كيمياء",
"أحياء",
"علوم البيئة",
"عربي",
"إنجليزي",
"فرنسي",
"تاريخ",
"جغرافيا",
"دراسات",
"إسلامية",
"فنون",
"موسيقى",
"تقنية",
"رياضة"
]

==========================================

التصميم

==========================================

st.markdown("""

<style>  
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Cairo:wght@400;500;600;700;800&display=swap');  
  
:root {  
    --cyan: #b8eff7;  
    --blue: #82d9ec;  
    --lavender: #dcd4ff;  
    --dark: #34445d;  
    --muted: #73839b;  
    --white: #ffffff;  
}  
  
html, body, [class*="css"] {  
    font-family: 'Cairo', sans-serif;  
    color: var(--dark);  
}  
  
.stApp {  
    background:  
        radial-gradient(circle at 10% 5%, #e1faff 0, transparent 30%),  
        radial-gradient(circle at 90% 15%, #eee8ff 0, transparent 30%),  
        linear-gradient(135deg, #f5fdff, #f5f3ff 60%, #f8fcff);  
}  
  
header[data-testid="stHeader"] {  
    background: transparent;  
}  
  
.block-container {  
    padding-top: 2rem;  
    padding-bottom: 3rem;  
    max-width: 1200px;  
}  
  
section[data-testid="stSidebar"] {  
    background: linear-gradient(180deg, #e5faff, #f0edff);  
    border-left: 1px solid rgba(255,255,255,.8);  
}  
  
section[data-testid="stSidebar"] * {  
    direction: rtl;  
    text-align: right;  
}  
  
h1, h2, h3, p, label {  
    color: var(--dark);  
}  
  
h1 {  
    font-weight: 800;  
}  
  
div[data-testid="stMetric"] {  
    background: rgba(255,255,255,.65);  
    border: 1px solid rgba(255,255,255,.9);  
    padding: 18px;  
    border-radius: 22px;  
    box-shadow: 0 8px 25px rgba(124, 175, 205, .10);  
}  
  
div[data-testid="stMetricLabel"] {  
    color: #71839b;  
}  
  
div[data-testid="stMetricValue"] {  
    color: #476b8c;  
    font-weight: 800;  
}  
  
div.stButton > button {  
    border: 1px solid rgba(255,255,255,.9);  
    border-radius: 16px;  
    background: linear-gradient(135deg, #c8f3f9, #dcd6ff);  
    color: #344b68;  
    font-weight: 700;  
    padding: 9px 20px;  
    transition: .2s;  
}  
  
div.stButton > button:hover {  
    border-color: #9cdaed;  
    transform: translateY(-2px);  
    box-shadow: 0 7px 18px rgba(123, 188, 215, .2);  
}  
  
div[data-testid="stTextInput"] input,  
div[data-testid="stTextArea"] textarea,  
div[data-testid="stSelectbox"] div,  
div[data-testid="stDateInput"] input {  
    border-radius: 13px;  
}  
  
.glass-card {  
    background: rgba(255,255,255,.60);  
    border: 1px solid rgba(255,255,255,.95);  
    border-radius: 25px;  
    padding: 23px;  
    margin: 12px 0;  
    box-shadow: 0 10px 30px rgba(116, 165, 195, .11);  
    backdrop-filter: blur(15px);  
}  
  
.hero-card {  
    background: linear-gradient(120deg,  
        rgba(198,244,250,.82),  
        rgba(230,222,255,.85));  
    border: 1px solid white;  
    border-radius: 30px;  
    padding: 28px;  
    box-shadow: 0 12px 35px rgba(133,173,207,.16);  
}  
  
.small-note {  
    color: #78899e;  
    font-size: 14px;  
}  
  
.miku-title {  
    font-size: 29px;  
    font-weight: 800;  
    color: #456581;  
}  
  
.chat-user {  
    background: #dff7fc;  
    border-radius: 20px 20px 5px 20px;  
    padding: 15px;  
    margin: 10px 0;  
    direction: rtl;  
    text-align: right;  
}  
  
.chat-miku {  
    background: #eeeaff;  
    border-radius: 20px 20px 20px 5px;  
    padding: 15px;  
    margin: 10px 0;  
    direction: rtl;  
    text-align: right;  
}  
  
.task-card {  
    background: rgba(255,255,255,.78);  
    border: 1px solid #ffffff;  
    border-radius: 18px;  
    padding: 16px;  
    margin: 10px 0;  
}  
  
div[data-testid="stProgress"] > div > div {  
    background: linear-gradient(90deg, #9de5f1, #c5b9fa);  
}  
  
footer {  
    visibility: hidden;  
}  
  
#MainMenu {  
    visibility: hidden;  
}  
</style>  """, unsafe_allow_html=True)

==========================================

دوال مساعدة

==========================================

def level_info(xp):
level = xp // 100 + 1
current = xp % 100
return level, current

def add_xp(amount):
st.session_state.xp += amount

def get_api_key():
try:
return st.secrets["GEMINI_API_KEY"]
except Exception:
return os.environ.get("GEMINI_API_KEY", "")

def clean_chat_history(history):
"""
تجهيز سجل المحادثة بحيث تتناوب أدوار user و model.
"""
cleaned = []

for item in history[-12:]:  
    role = item.get("role")  
    message = str(item.get("text", "")).strip()  

    if not message:  
        continue  

    if role == "assistant":  
        role = "model"  

    if role not in ("user", "model"):  
        continue  

    if cleaned and cleaned[-1]["role"] == role:  
        cleaned[-1]["parts"][0]["text"] += "\n" + message  
    else:  
        cleaned.append({  
            "role": role,  
            "parts": [{"text": message}]  
        })  

return cleaned

==========================================

ذكاء ميكو الاصطناعي

==========================================

def ask_miku(question):
api_key = get_api_key()

if not api_key:  
    return (  
        "ما حصلت مفتاح Gemini API! 🩵\n\n"  
        "أضيفي GEMINI_API_KEY في Streamlit Secrets "  
        "حتى أقدر أجاوبك."  
    )  

system_instruction = """

أنتِ ميكو، مساعدة دراسية لطيفة وذكية.
تحدثي باللغة العربية الواضحة ما لم يطلب المستخدم لغة أخرى.
اشرحي الدروس بطريقة سهلة ومنظمة ومناسبة للطلاب.
قسمي الحلول إلى خطوات مرقمة عند الحاجة.
لا تختلقي معلومات، وإذا لم تعرفي شيئاً فقولي ذلك بوضوح.
اجعلي الإجابات واضحة ومفيدة وغير طويلة بلا داعٍ.
"""

contents = clean_chat_history(  
    st.session_state.chat_history  
)  

# ضمان أن آخر رسالة هي رسالة المستخدم  
if not contents or contents[-1]["role"] != "user":  
    contents.append({  
        "role": "user",  
        "parts": [{"text": question}]  
    })  

url = (  
    "https://generativelanguage.googleapis.com/"  
    "v1beta/models/gemini-3.8-flash:generateContent"  
)  

headers = {  
    "Content-Type": "application/json",  
    "x-goog-api-key": api_key  
}  

payload = {  
    "systemInstruction": {  
        "parts": [{"text": system_instruction}]  
    },  
    "contents": contents,  
    "generationConfig": {  
        "maxOutputTokens": 900  
    }  
}  

try:  
    response = requests.post(  
        url,  
        headers=headers,  
        json=payload,  
        timeout=40  
    )  

    if response.status_code != 200:  
        try:  
            error_data = response.json()  
            error_message = (  
                error_data.get("error", {})  
                .get("message", "حدث خطأ غير معروف.")  
            )  
        except Exception:  
            error_message = response.text[:300]  

        return (  
            "واجهت مشكلة في الاتصال بالذكاء الاصطناعي.\n\n"  
            + str(error_message)  
        )  

    data = response.json()  

    candidates = data.get("candidates", [])  

    if not candidates:  
        return "ما قدرت أجهز إجابة هذه المرة. جربي صياغة السؤال مرة ثانية."  

    parts = candidates[0].get("content", {}).get("parts", [])  

    answer = "\n".join(  
        part.get("text", "")  
        for part in parts  
        if part.get("text")  
    ).strip()  

    if not answer:  
        return "وصلني سؤالك، لكن ما ظهر لي نص الإجابة. جربي مرة ثانية."  

    return answer  

except requests.Timeout:  
    return "الاتصال أخذ وقتًا طويلًا. جربي مرة ثانية بعد قليل. 🩵"  

except requests.RequestException:  
    return "تعذر الاتصال بالإنترنت أو بخدمة ميكو. تحققي من الاتصال وجربي مجددًا."  

except Exception as error:  
    return f"حدث خطأ غير متوقع: {str(error)[:200]}"

==========================================

القائمة الجانبية

==========================================

with st.sidebar:
st.markdown(
"<div style='text-align:center;font-size:24px;font-weight:800;color:#54728f'>"
"୨୧ Study with Miku ୨୧"
"</div>",
unsafe_allow_html=True
)

st.markdown("---")  

pages = [  
    "الرئيسية",  
    "مهامي وواجباتي",  
    "اسألي ميكو",  
    "جلسة المذاكرة",  
    "إنجازاتي"  
]  

selected_page = st.radio(  
    "القائمة",  
    pages,  
    index=pages.index(st.session_state.page)  
    if st.session_state.page in pages else 0  
)  

st.session_state.page = selected_page  

st.markdown("---")  

level, progress = level_info(st.session_state.xp)  

st.markdown(  
    f"""  
    <div class="glass-card" style="text-align:center">  
        <div style="font-size:30px">🌷</div>  
        <b>مستواك الحالي</b>  
        <h2 style="color:#6485aa">Level {level}</h2>  
        <p>{st.session_state.xp} XP</p>  
    </div>  
    """,  
    unsafe_allow_html=True  
)  

st.caption("ذاكري بهدوء، وكل خطوة تقربك من هدفك 🩵")

==========================================

الصفحة الرئيسية

==========================================

if st.session_state.page == "الرئيسية":

st.markdown("""  
<div class="hero-card">  
    <div class="miku-title">أهلًا بكِ في Study with Miku ୨୧</div>  
    <h3>رحلتك الدراسية تبدأ بخطوة صغيرة!</h3>  
    <p>ذاكري معي، أنجزي مهامك، واجمعي النقاط يومًا بعد يوم.</p>  
</div>  
""", unsafe_allow_html=True)  

st.write("")  

col1, col2, col3 = st.columns(3)  

pending = sum(  
    1 for task in st.session_state.tasks  
    if not task.get("done", False)  
)  

with col1:  
    st.metric("المهام المتبقية", pending)  

with col2:  
    st.metric("النقاط المكتسبة", st.session_state.xp)  

with col3:  
    st.metric(  
        "جلسات المذاكرة",  
        st.session_state.completed_sessions  
    )  

st.write("")  

left, right = st.columns([1.3, 1])  

with left:  
    st.markdown(  
        '<div class="glass-card">'  
        '<h3>✨ ابدئي إنجازاتك</h3>'  
        '<p>رتبي واجباتك وحددي أول مهمة تريدين إنجازها.</p>'  
        '</div>',  
        unsafe_allow_html=True  
    )  

    if st.button("افتحي قائمة المهام", use_container_width=True):  
        st.session_state.page = "مهامي وواجباتي"  
        st.rerun()  

    if st.button("ابدئي جلسة مذاكرة", use_container_width=True):  
        st.session_state.page = "جلسة المذاكرة"  
        st.rerun()  

with right:  
    st.markdown(  
        '<div class="glass-card" style="text-align:center">'  
        '<div style="font-size:48px">🎀</div>'  
        '<h3>ميكو هنا لمساعدتك!</h3>'  
        '<p>اسأليها عن أي درس أو سؤال دراسي.</p>'  
        '</div>',  
        unsafe_allow_html=True  
    )  

    if st.button("تحدثي مع ميكو", use_container_width=True):  
        st.session_state.page = "اسألي ميكو"  
        st.rerun()  

st.markdown("### 📌 مهامك القادمة")  

upcoming = [  
    task for task in st.session_state.tasks  
    if not task.get("done", False)  
][:4]  

if upcoming:  
    for task in upcoming:  
        st.markdown(  
            f"""  
            <div class="task-card">  
                <b>{task['title']}</b>  
                <div class="small-note">  
                    {task['subject']} · {task['priority']}  
                </div>  
            </div>  
            """,  
            unsafe_allow_html=True  
        )  
else:  
    st.info("لا توجد مهام معلقة حاليًا. أضيفي مهمة جديدة!")

==========================================

صفحة المهام والواجبات

==========================================

elif st.session_state.page == "مهامي وواجباتي":

st.markdown("# 📚 مهامي وواجباتي")  
st.caption("كل مهمة تنجزينها تمنحكِ 20 نقطة XP.")  

with st.expander("＋ إضافة مهمة جديدة", expanded=True):  

    with st.form("new_task_form", clear_on_submit=True):  

        task_title = st.text_input(  
            "اسم المهمة",  
            placeholder="مثال: حل أسئلة الفيزياء"  
        )  

        task_subject = st.selectbox(  
            "المادة",  
            SUBJECTS  
        )  

        task_priority = st.selectbox(  
            "الأولوية",  
            ["عالية", "متوسطة", "منخفضة"]  
        )  

        task_date = st.date_input(  
            "موعد التسليم",  
            value=None  
        )  

        task_notes = st.text_area(  
            "ملاحظات إضافية",  
            placeholder="اكتبي أي تفاصيل..."  
        )  

        submitted = st.form_submit_button(  
            "إضافة المهمة",  
            use_container_width=True  
        )  

        if submitted:  
            if task_title.strip():  
                st.session_state.tasks.append({  
                    "id": str(uuid.uuid4()),  
                    "title": task_title.strip(),  
                    "subject": task_subject,  
                    "priority": task_priority,  
                    "date": str(task_date) if task_date else "",  
                    "notes": task_notes,  
                    "done": False  
                })  

                st.success("تمت إضافة المهمة بنجاح! 🎀")  
                st.rerun()  
            else:  
                st.warning("اكتبي اسم المهمة أولًا.")  

st.markdown("### مهامك الحالية")  

if not st.session_state.tasks:  
    st.info("لم تضيفي أي مهمة بعد.")  

for task in st.session_state.tasks:  

    if task.get("done", False):  
        continue  

    with st.container():  
        st.markdown(  
            f"""  
            <div class="task-card">  
                <h4>{task['title']}</h4>  
                <p class="small-note">  
                    📘 {task['subject']} |  
                    ⭐ الأولوية: {task['priority']}  
                </p>  
                <p class="small-note">  
                    📅 {task.get('date') or 'لم يحدد موعد'}  
                </p>  
                <p>{task.get('notes', '')}</p>  
            </div>  
            """,  
            unsafe_allow_html=True  
        )  

        col1, col2 = st.columns(2)  

        with col1:  
            if st.button(  
                "✓ أنجزت المهمة +20 XP",  
                key="done_" + task["id"],  
                use_container_width=True  
            ):  
                task["done"] = True  
                add_xp(20)  
                st.session_state.completed_tasks += 1  
                st.success("أحسنتِ! حصلتِ على 20 نقطة 🎉")  
                st.rerun()  

        with col2:  
            if st.button(  
                "حذف المهمة",  
                key="delete_" + task["id"],  
                use_container_width=True  
            ):  
                st.session_state.tasks = [  
                    t for t in st.session_state.tasks  
                    if t["id"] != task["id"]  
                ]  
                st.rerun()  

st.markdown("---")  
st.markdown("### 🌸 المهام المكتملة")  

completed = [  
    task for task in st.session_state.tasks  
    if task.get("done", False)  
]  

if completed:  
    for task in completed:  
        st.markdown(  
            f"""  
            <div class="task-card">  
                <s>{task['title']}</s>  
                <span style="color:#65a99b"> ✓ مكتملة</span>  
                <div class="small-note">{task['subject']}</div>  
            </div>  
            """,  
            unsafe_allow_html=True  
        )  
else:  
    st.caption("ستظهر مهامك المكتملة هنا.")

==========================================

صفحة المحادثة مع ميكو

==========================================

elif st.session_state.page == "اسألي ميكو":

st.markdown("# 🎀 اسألي ميكو")  
st.caption("مساعدتك الدراسية الذكية موجودة هنا.")  

st.markdown(  
    """  
    <div class="hero-card">  
        <h3>مرحبًا! أنا ميكو 🩵</h3>  
        <p>أرسلي سؤالك، وسأساعدك على فهمه خطوة بخطوة.</p>  
    </div>  
    """,  
    unsafe_allow_html=True  
)  

st.write("")  

for message in st.session_state.chat_history:  

    if message["role"] == "user":  
        st.markdown(  
            f'<div class="chat-user">🩵 <b>أنتِ</b><br>{message["text"]}</div>',  
            unsafe_allow_html=True  
        )  
    elif message["role"] == "assistant":  
        safe_text = (  
            message["text"]  
            .replace("&", "&amp;")  
            .replace("<", "&lt;")  
            .replace(">", "&gt;")  
            .replace("\n", "<br>")  
        )  

        st.markdown(  
            f'<div class="chat-miku">🎀 <b>ميكو</b><br>{safe_text}</div>',  
            unsafe_allow_html=True  
        )  

with st.form("chat_form", clear_on_submit=True):  

    user_question = st.text_area(  
        "اكتبي رسالتك لميكو",  
        placeholder="مثال: اشرحي لي قانون نيوتن الثالث...",  
        height=100  
    )  

    send = st.form_submit_button(  
        "إرسال إلى ميكو ✨",  
        use_container_width=True  
    )  

    if send:  

        if user_question.strip():  

            question = user_question.strip()  

            st.session_state.chat_history.append({  
                "role": "user",  
                "text": question  
            })  

            with st.spinner("ميكو تفكر في إجابتك... 🩵"):  
                answer = ask_miku(question)  

            st.session_state.chat_history.append({  
                "role": "assistant",  
                "text": answer  
            })  

            st.rerun()  

        else:  
            st.warning("اكتبي سؤالك أولًا.")  

if st.button("مسح المحادثة"):  
    st.session_state.chat_history = []  
    st.rerun()

==========================================

المؤقت

==========================================

def finish_timer():
st.session_state.timer_running = False
st.session_state.timer_end = None
st.session_state.timer_paused_remaining = None

if st.session_state.timer_mode == "مذاكرة":  
    st.session_state.completed_sessions += 1  
    add_xp(10)

def show_timer_panel():

if st.session_state.timer_running:  

    remaining = max(  
        0,  
        int(st.session_state.timer_end - time.time())  
    )  

    if remaining <= 0:  
        finish_timer()  
        st.success("انتهت الجلسة! أحسنتِ، حصلتِ على 10 نقاط XP 🎉")  
        return  

elif st.session_state.timer_paused_remaining is not None:  
    remaining = st.session_state.timer_paused_remaining  

else:  
    remaining = st.session_state.timer_minutes * 60  

minutes, seconds = divmod(remaining, 60)  

st.markdown(  
    f"""  
    <div class="hero-card" style="text-align:center;padding:35px">  
        <div style="font-size:35px">⏳</div>  
        <h3>{st.session_state.timer_mode}</h3>  
        <div style="  
            font-size:65px;  
            font-weight:800;  
            color:#53799c;  
            direction:ltr;  
        ">{minutes:02d}:{seconds:02d}</div>  
        <p>خذي وقتك وركزي على هدفك 🩵</p>  
    </div>  
    """,  
    unsafe_allow_html=True  
)  

if st.session_state.timer_running:  
    col1, col2 = st.columns(2)  

    with col1:  
        if st.button("إيقاف مؤقت", use_container_width=True):  
            st.session_state.timer_paused_remaining = remaining  
            st.session_state.timer_running = False  
            st.session_state.timer_end = None  
            st.rerun()  

    with col2:  
        if st.button("إنهاء الجلسة", use_container_width=True):  
            st.session_state.timer_running = False  
            st.session_state.timer_end = None  
            st.session_state.timer_paused_remaining = None  
            st.rerun()  

elif st.session_state.timer_paused_remaining is not None:  

    if st.button("استئناف الجلسة", use_container_width=True):  
        st.session_state.timer_end = (  
            time.time() + st.session_state.timer_paused_remaining  
        )  
        st.session_state.timer_running = True  
        st.session_state.timer_paused_remaining = None  
        st.rerun()  

else:  

    col1, col2 = st.columns(2)  

    with col1:  
        if st.button("ابدئي الآن ▶", use_container_width=True):  
            st.session_state.timer_end = (  
                time.time() + st.session_state.timer_minutes * 60  
            )  
            st.session_state.timer_running = True  
            st.rerun()  

    with col2:  
        if st.button("إعادة ضبط", use_container_width=True):  
            st.session_state.timer_paused_remaining = None  
            st.rerun()

استخدام fragment لتحديث المؤقت دون إعادة تحميل التطبيق كله

if hasattr(st, "fragment"):

@st.fragment(run_every="1s")  
def live_timer():  
    show_timer_panel()

else:

def live_timer():  
    show_timer_panel()  
    st.caption(  
        "إذا لم يتحدث المؤقت تلقائيًا، حدّثي الصفحة."  
    )

==========================================

صفحة جلسة المذاكرة

==========================================

elif st.session_state.page == "جلسة المذاكرة":

st.markdown("# ⏰ جلسة المذاكرة")  
st.caption("قسمي وقتك بين التركيز والراحة.")  

if not st.session_state.timer_running and (  
    st.session_state.timer_paused_remaining is None  
):  

    mode = st.selectbox(  
        "اختاري نوع الجلسة",  
        ["مذاكرة", "استراحة"]  
    )  

    duration = st.selectbox(  
        "مدة الجلسة بالدقائق",  
        [10, 15, 20, 25, 30, 45, 50, 60, 90]  
    )  

    if (  
        mode != st.session_state.timer_mode  
        or duration != st.session_state.timer_minutes  
    ):  
        st.session_state.timer_mode = mode  
        st.session_state.timer_minutes = duration  

live_timer()  

st.markdown("---")  

st.markdown(  
    f"""  
    <div class="glass-card" style="text-align:center">  
        <h3>🌷 إنجازات جلساتك</h3>  
        <h2 style="color:#6789aa">  
            {st.session_state.completed_sessions}  
        </h2>  
        <p>جلسة مذاكرة مكتملة</p>  
    </div>  
    """,  
    unsafe_allow_html=True  
)

==========================================

صفحة الإنجازات

==========================================

elif st.session_state.page == "إنجازاتي":

st.markdown("# 🏆 إنجازاتي")  
st.caption("كل نقطة جمعتها دليل على تقدمك!")  

level, progress = level_info(st.session_state.xp)  

col1, col2, col3 = st.columns(3)  

with col1:  
    st.metric("مجموع XP", st.session_state.xp)  

with col2:  
    st.metric("المستوى", level)  

with col3:  
    st.metric(  
        "مهام مكتملة",  
        st.session_state.completed_tasks  
    )  

st.markdown("### تقدمك نحو المستوى التالي")  

st.progress(progress / 100)  

st.caption(f"{progress} / 100 XP")  

st.markdown("---")  
st.markdown("### 🎀 أوسمتك")  

achievements = [  
    (  
        "🌱",  
        "البداية الجميلة",  
        st.session_state.xp >= 10  
    ),  
    (  
        "📚",  
        "أول إنجاز",  
        st.session_state.completed_tasks >= 1  
    ),  
    (  
        "⭐",  
        "عشر مهام",  
        st.session_state.completed_tasks >= 10  
    ),  
    (  
        "⏰",  
        "أول جلسة مذاكرة",  
        st.session_state.completed_sessions >= 1  
    ),  
    (  
        "💎",  
        "مئة نقطة",  
        st.session_state.xp >= 100  
    ),  
    (  
        "👑",  
        "خمسمئة نقطة",  
        st.session_state.xp >= 500  
    )  
]  

for emoji, title, unlocked in achievements:  

    if unlocked:  
        st.success(f"{emoji} {title} — تم فتح الوسام!")  
    else:  
        st.markdown(  
            f'<div class="task-card" style="opacity:.55">'  
            f'{emoji} {title} — لم يفتح بعد'  
            f'</div>',  
            unsafe_allow_html=True  
        )

==========================================

التذييل

==========================================

st.markdown("---")

st.markdown(
"""
<div style="text-align:center;color:#8294a8;padding:15px">
୨୧ Made with love for your study journey ୨୧
<br>
Study with Miku 🩵
</div>
""",
unsafe_allow_html=True
)
