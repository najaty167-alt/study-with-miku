import streamlit as st
import requests, time, os, uuid, json, html
from datetime import date

st.set_page_config(page_title="Study with Miku 🎀", page_icon="୨୧", layout="wide")

SUBJECTS = [
    "رياضيات متقدمة", "فيزياء", "كيمياء", "أحياء", "لغة عربية",
    "لغة إنجليزية", "دراسات اجتماعية", "تربية إسلامية", "تقنية معلومات", "أخرى"
]

DATA_DEFAULTS = {
    "tasks": [], "xp": 0, "chat_history": [], "completed_sessions": 0,
    "completed_tasks": 0, "notes": []
}

for k, v in DATA_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v.copy() if isinstance(v, (list, dict)) else v

for k, v in {
    "logged_in": False, "user_email": "", "page": "الرئيسية",
    "timer_mode": "مذاكرة", "timer_minutes": 25, "timer_running": False,
    "timer_end": None, "timer_paused_remaining": None
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def secret(name):
    try: return st.secrets.get(name, os.environ.get(name, ""))
    except Exception: return os.environ.get(name, "")

GEMINI_KEY = secret("GEMINI_API_KEY")

# ==================================================
# 🩷 تصميم الثيم الوردي الأنيق
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=Tajawal:wght@400;500;700;800&display=swap');
:root{--pink:#f3a8ca;--dark-pink:#d96e9d;--light-pink:#fff0f6;--text:#765466;}
html,body,[class*="css"]{font-family:'Tajawal',sans-serif;color:var(--text)}
.stApp{background:radial-gradient(circle at 10% 5%,#ffe4ef 0,transparent 40%),radial-gradient(circle at 90% 80%,#f0e7ff 0,transparent 40%),#fffafd}
header[data-testid="stHeader"]{background:rgba(255,250,253,0.75)}
.block-container{padding-top:1.8rem;padding-bottom:3rem;max-width:1200px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#ffe5f0,#fff6fa 55%,#f3ebff);border-right:2px solid #f8d4e5}
section[data-testid="stSidebar"] *{direction:rtl;text-align:right}
div.stButton>button{background:linear-gradient(135deg,#f5b5d2,#e99fc2);color:white !important;border:1px solid #efc0d7;border-radius:16px;font-weight:700;padding:10px 20px;box-shadow:0 4px 12px rgba(221,131,174,.14)}
div.stButton>button:hover{background:linear-gradient(135deg,#eaa0c1,#d982aa);transform:translateY(-2px)}
.miku-header{text-align:center;padding:25px;margin-bottom:20px;border-radius:28px;background:rgba(255,255,255,0.85);border:2px solid #f8d7e7;box-shadow:0 10px 35px rgba(219,143,180,0.13)}
.miku-header h1{color:#dc83ac;font-family:'Quicksand',sans-serif;font-size:36px;font-weight:700;margin:0}
.glass-card{background:rgba(255,255,255,0.88);border:1.5px solid #f7d5e5;border-radius:24px;padding:22px;margin:10px 0;box-shadow:0 7px 25px rgba(218,147,183,0.10)}
.timer-display{font-family:'Quicksand',sans-serif;font-size:75px;font-weight:700;color:#d86e9e;text-align:center;margin:15px 0;}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# ---------- AI Chat Function ----------
def ask_miku(question):
    if not GEMINI_KEY: return "مفتاح Gemini غير موجود في Secrets (GEMINI_API_KEY)."
    body={"system_instruction":{"parts":[{"text":"أنتِ ميكو، مساعدة دراسية لطيفة ومرحة تتحدث بالعربية بأسلوب مشجع ومناسب لطالبة في المرحلة الثانوية. اشرحي بوضوح وبخطوات مرتبة."}]},"contents":[{"role":"user","parts":[{"text":question}]}]}
    try:
        r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}", headers={"Content-Type": "application/json"}, json=body, timeout=30)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"عذراً، حدث خطأ في الرد (رمز {r.status_code})."
    except Exception as e:
        return f"تعذّر الاتصال بميكو: {e}"

# ---------- شاشة تسجيل الدخول السريعة والناعمة ----------
if not st.session_state.logged_in:
    st.markdown("""
    <div class="miku-header" style="max-width:600px; margin: 50px auto;">
        <div style="font-size:50px;">🎀🐰</div>
        <h1>Study with Miku</h1>
        <p style="color:#a8809a; font-size:16px;">مساحتك الدراسية الوردية المتكاملة ♡</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        name_input = st.text_input("اسمك الكريم 🌸", placeholder="نجاة")
        if st.button("✨ ابدئي رحلة الإنجاز", use_container_width=True):
            if name_input.strip():
                st.session_state.logged_in = True
                st.session_state.user_email = name_input.strip()
                st.rerun()
            else:
                st.warning("اكتبي اسمك من فضلكِ! 🩷")
    st.stop()

# ==================================================
# 🎀 القائمة الجانبية (Sidebar)
# ==================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:15px 0;">
        <div style="font-size:55px;">🎀🐰</div>
        <div style="font-size:20px;font-weight:800;color:#d982aa;">Study with Miku</div>
        <div style="font-size:13px;color:#ac8199;">مرحباً بكِ، {} 🩵</div>
    </div>
    """.format(st.session_state.user_email), unsafe_allow_html=True)
    
    st.markdown("---")
    pages = {
        "🏠 الرئيسية": "الرئيسية",
        "📚 واجباتي": "الواجبات",
        "🤖 اسألي ميكو": "ميكو الذكية",
        "⏰ جلسة المذاكرة": "المؤقت",
        "📝 ملاحظاتي وتلخيصي": "الملاحظات",
        "🏆 إنجازاتي": "الإنجازات"
    }
    
    for label, page_name in pages.items():
        if st.button(label, key="nav_" + page_name, use_container_width=True):
            st.session_state.page = page_name
            st.rerun()
            
    st.markdown("---")
    level = st.session_state.xp // 100 + 1
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;padding:12px;">
        <div>👑 Level {level}</div>
        <div style="color:#b27c9c;font-size:14px;">{st.session_state.xp} XP</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 تسجيل الخروج", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ==================================================
# 🏠 الرئيسية (Home)
# ==================================================
if st.session_state.page == "الرئيسية":
    st.markdown("""
    <div class="miku-header">
        <h1>Study with Miku 🎀</h1>
        <p>كل يوم إنجاز جديد يقربك من هدفك ♡</p>
    </div>
    """, unsafe_allow_html=True)
    
    total = len(st.session_state.tasks)
    finished = sum(1 for t in st.session_state.tasks if t["done"])
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("كل المهام", total)
    with c2: st.metric("المنجزة", finished)
    with c3: st.metric("نقاط الخبرة", f"{st.session_state.xp} XP")
    with c4: st.metric("جلسات المذاكرة", st.session_state.completed_sessions)
    
    st.markdown("### 🌸 نظرة سريعة على يومك")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("＋ أضيفي واجب جديد", use_container_width=True):
            st.session_state.page = "الواجبات"; st.rerun()
    with col2:
        if st.button("⏰ ابدئي مؤقت المذاكرة", use_container_width=True):
            st.session_state.page = "المؤقت"; st.rerun()

# ==================================================
# 📚 الواجبات والمهام
# ==================================================
elif st.session_state.page == "الواجبات":
    st.markdown("# 📚 مهامي وواجباتي")
    
    with st.form("task_form", clear_on_submit=True):
        t_title = st.text_input("عنوان المهمة", placeholder="مثال: حل واجب الفيزياء")
        t_sub = st.selectbox("المادة", SUBJECTS)
        t_prio = st.selectbox("الأولوية", ["عالية", "متوسطة", "منخفضة"])
        submitted = st.form_submit_button("🎀 حفظ المهمة", use_container_width=True)
        
        if submitted and t_title.strip():
            st.session_state.tasks.append({"id": str(uuid.uuid4()), "title": t_title.strip(), "subject": t_sub, "priority": t_prio, "done": False})
            st.success("تمت الإضافة بنجاح! 🌸")
            st.rerun()

    st.markdown("### قائمة المهام")
    for task in st.session_state.tasks:
        if not task["done"]:
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**🎀 {task['title']}** — <small>{task['subject']} ({task['priority']})</small>", unsafe_allow_html=True)
                with c2:
                    if st.button("✓ تم", key="finish_"+task["id"]):
                        task["done"] = True
                        st.session_state.xp += 20
                        st.session_state.completed_tasks += 1
                        st.rerun()

# ==================================================
# 🤖 اسألي ميكو (AI Chat)
# ==================================================
elif st.session_state.page == "ميكو الذكية":
    st.markdown("# 🤖 اسألي ميكو")
    st.markdown("ميكو هنا لمساعدتك في شرح المسائل، تلخيص الدروس، والإجابة عن أي استفسار دراسي! 🩷")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("اكتبي سؤالك الدراسي هنا... 🎀"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.spinner("ميكو تفكر في الإجابة... 🩷"):
            reply = ask_miku(prompt)
            
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"): st.markdown(reply)

# ==================================================
# ⏰ المؤقت (Study Timer with Miku Loops)
# ==================================================
elif st.session_state.page == "المؤقت":
    st.markdown("# ⏰ جلسة المذاكرة والتركيز")
    
    # اختيار وضع المؤقت ومدته
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        mode = st.radio("نوع الجلسة", ["مذاكرة", "استراحة"], horizontal=True)
    with col_m2:
        minutes = st.selectbox("المدة (بالدقائق)", [10, 15, 20, 25, 30, 45, 50, 60], index=3)

    # عرض أنيميشن أو فيديو ميكو التفاعلي حسب الحالة
    if mode == "مذاكرة":
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:60px;">🎧📚💻</div>
            <h3 style="color:#d982aa;">ميكو تذاكر معك بتركيز!</h3>
            <p style="color:#886078;">ركزي الآن، وكل دقيقة تقربك من تفوقك 🩷</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:60px;">☕📖🌸</div>
            <h3 style="color:#d982aa;">وقت الاستراحة والتشلّي!</h3>
            <p style="color:#886078;">خذي نفساً عميقاً واقراي كتاباً مفضلاً ☕</p>
        </div>
        """, unsafe_allow_html=True)

    # أزرار تحكم المؤقت
    if "timer_active" not in st.session_state:
        st.session_state.timer_active = False
        st.session_state.time_left = minutes * 60

    c_b1, c_b2 = st.columns(2)
    with c_b1:
        if st.button("▶ ابدئي المؤقت", use_container_width=True):
            st.session_state.timer_active = True
            st.session_state.time_left = minutes * 60
    with c_b2:
        if st.button("⏹ إيقاف", use_container_width=True):
            st.session_state.timer_active = False

    # عرض العداد التنازلي البارز في منتصف الصفحة
    mm, ss = divmod(st.session_state.time_left, 60)
    st.markdown(f'<div class="timer-display">{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)
    
    if st.session_state.timer_active and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()
    elif st.session_state.timer_active and st.session_state.time_left == 0:
        st.session_state.timer_active = False
        if mode == "مذاكرة":
            st.session_state.completed_sessions += 1
            st.session_state.xp += 15
        st.balloons()
        st.success("انتهت الجلسة بنجاح! رائع جداً 🎉")

# ==================================================
# 📝 ملاحظاتي وتلخيصي (Notes Feature)
# ==================================================
elif st.session_state.page == "الملاحظات":
    st.markdown("# 📝 ملاحظات وتلخيص الدروس")
    st.markdown("دوني هنا أفكارك، قوانين الفيزياء والرياضيات، أو ملخصات سريعة لكل مادة! 🌸")
    
    with st.form("note_form", clear_on_submit=True):
        n_title = st.text_input("عنوان الملاحظة أو الدرس", placeholder="مثال: ملخص قوانين الحركة في الفيزياء")
        n_content = st.text_area("اكتبي تلخيصك أو ملاحظاتك هنا...", height=150)
        n_submit = st.form_submit_button("💾 حفظ الملاحظة", use_container_width=True)
        
        if n_submit and n_title.strip():
            st.session_state.notes.append({"title": n_title.strip(), "content": n_content.strip()})
            st.success("تم حفظ الملاحظة بنجاح! 🩷")
            st.rerun()
            
    st.markdown("### 📂 ملاحظاتك المحفوظة")
    if not st.session_state.notes:
        st.info("لا توجد ملاحظات مضافة حتى الآن. ابدئي بتدوين ملخصاتك! 🌷")
    else:
        for i, note in enumerate(st.session_state.notes):
            with st.expander(f"📌 {note['title']}"):
                st.write(note['content'])

# ==================================================
# 🏆 الإنجازات (Achievements)
# ==================================================
elif st.session_state.page == "الإنجازات":
    st.markdown("# 🏆 إنجازاتك الدراسية")
    level = st.session_state.xp // 100 + 1
    
    c1, c2, c3 = st.columns(3)
    c1.metric("المستوى الحالي", f"Level {level}")
    c2.metric("نقاط الخبرة", f"{st.session_state.xp} XP")
    c3.metric("الجلسات المكتملة", st.session_state.completed_sessions)
    
    st.progress((st.session_state.xp % 100) / 100)
    st.caption("مستوى التقدم للمستوى التالي ♡")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#c69ab2;padding:15px;'>୨୧ Study with Miku · جاهز لتألقك يوم الخميس 🩵 ୨୧</div>", unsafe_allow_html=True)
