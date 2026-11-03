import streamlit as st
import requests, time, os, uuid, json, html
from datetime import date

st.set_page_config(page_title="Study with Miku", page_icon="୨୧", layout="wide")

# Configure these in Streamlit Secrets:
# SUPABASE_URL = "https://PROJECT.supabase.co"
# SUPABASE_ANON_KEY = "SUPABASE_ANON_KEY"
# GEMINI_API_KEY = "GEMINI_API_KEY"

SUBJECTS = [
    "رياضيات", "رياضيات متقدمة", "إحصاء", "هندسة", "فيزياء", "كيمياء",
    "أحياء", "علوم عامة", "علوم بيئية", "علوم الأرض", "فلك", "لغة عربية",
    "لغة إنجليزية", "لغة فرنسية", "لغة إسبانية", "لغة ألمانية",
    "تربية إسلامية", "حضارة إسلامية", "تاريخ", "جغرافيا",
    "دراسات اجتماعية", "فلسفة", "تقنية معلومات", "حاسوب", "برمجة",
    "ذكاء اصطناعي", "فنون بصرية", "تربية فنية", "موسيقى", "تصميم",
    "تربية رياضية", "مهارات حياتية", "اقتصاد", "إدارة أعمال", "أخرى"
]
SHOP = [
    ("desk", "مكتب ميكو", 25, "🪑"), ("computer", "كمبيوتر", 40, "🖥️"),
    ("chair", "كرسي مريح", 20, "🪑"), ("bookshelf", "رف كتب", 30, "📚"),
    ("plant", "نبتة", 15, "🪴"), ("lamp", "مصباح", 20, "💡"),
    ("rug", "سجادة وردية", 25, "🌸"), ("window", "نافذة سماوية", 35, "🪟")
]
DATA_DEFAULTS = {
    "tasks": [], "xp": 0, "chat_history": [], "completed_sessions": 0,
    "completed_tasks": 0, "inventory": [], "equipped": []
}
for k, v in DATA_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v.copy() if isinstance(v, (list, dict)) else v
for k, v in {
    "auth_token": None, "user_id": None, "user_email": None,
    "data_loaded": False, "page": "الرئيسية", "auth_mode": "تسجيل الدخول",
    "timer_mode": "مذاكرة", "timer_minutes": 25, "timer_running": False,
    "timer_end": None, "timer_paused_remaining": None
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def secret(name):
    try: return st.secrets.get(name, os.environ.get(name, ""))
    except Exception: return os.environ.get(name, "")

SB_URL = secret("SUPABASE_URL").rstrip("/")
SB_KEY = secret("SUPABASE_ANON_KEY")
GEMINI_KEY = secret("GEMINI_API_KEY")

# Original pastel crystal-glass palette; readable dark text and light chat inputs.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Cairo:wght@400;500;600;700;800&display=swap');
:root{--cyan:#b8eff7;--blue:#82d9ec;--lav:#dcd4ff;--pink:#f7d8ed;--dark:#34445d;}
html,body,[class*="css"]{font-family:'Cairo',sans-serif;color:var(--dark)}
.stApp{background:radial-gradient(circle at 10% 5%,#e1faff 0,transparent 30%),radial-gradient(circle at 90% 15%,#eee8ff 0,transparent 30%),linear-gradient(135deg,#f5fdff,#f5f3ff 60%,#fff7fc)}
header[data-testid="stHeader"]{background:transparent}
.block-container{padding-top:1.5rem;padding-bottom:2.5rem;max-width:1300px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#e5faff,#f0edff 70%,#fff0f8);border-left:1px solid white}
section[data-testid="stSidebar"] *{direction:rtl;text-align:right}
h1,h2,h3,p,label{color:var(--dark)}
div[data-testid="stMetric"]{background:#ffffffb0;border:1px solid white;padding:16px;border-radius:22px;box-shadow:0 8px 25px #7cafd019}
div[data-testid="stMetricLabel"]{color:#71839b} div[data-testid="stMetricValue"]{color:#476b8c;font-weight:800}
div.stButton>button{border:1px solid white;border-radius:16px;background:linear-gradient(135deg,#c8f3f9,#dcd6ff 70%,#f7d8ed);color:#344b68;font-weight:700;padding:9px 18px}
div.stButton>button:hover{border-color:#9cdaed;transform:translateY(-1px);box-shadow:0 7px 18px #7bbcd733}
div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea,div[data-testid="stSelectbox"] div,div[data-testid="stDateInput"] input{border-radius:13px!important;background:#ffffffd9!important;color:#34445d!important}
div[data-testid="stTextArea"] textarea{background:#ffffffed!important;color:#34445d!important}
.glass-card{background:#ffffff99;border:1px solid #ffffffed;border-radius:25px;padding:22px;margin:10px 0;box-shadow:0 10px 30px #74a5c31c;backdrop-filter:blur(15px)}
.hero-card{background:linear-gradient(120deg,#c6f4fad1,#e6deffd9 65%,#fae1f1c7);border:1px solid white;border-radius:30px;padding:25px;box-shadow:0 12px 35px #85adcf29}
.miku-title{font-size:28px;font-weight:800;color:#456581}.small-note{color:#78899e;font-size:14px}
.chat-user{background:linear-gradient(120deg,#dff7fc,#e9f7ff);border:1px solid white;border-radius:20px 20px 5px 20px;padding:15px;margin:10px 0;direction:rtl;text-align:right;white-space:pre-wrap;color:#34445d}
.chat-miku{background:linear-gradient(120deg,#eeeaff,#f9eafa);border:1px solid white;border-radius:20px 20px 20px 5px;padding:15px;margin:10px 0;direction:rtl;text-align:right;white-space:pre-wrap;color:#34445d}
.task-card{background:#ffffffc7;border:1px solid white;border-radius:18px;padding:16px;margin:10px 0}
div[data-testid="stProgress"]>div>div{background:linear-gradient(90deg,#9de5f1,#c5b9fa,#f2cce5)}
div[data-testid="stImage"] img{border-radius:50%;border:5px solid rgba(255,255,255,.88);box-shadow:0 10px 28px rgba(125,165,205,.20);object-fit:cover}
footer,#MainMenu{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# ---------- Supabase Auth + per-user persistence ----------
def sb_headers(token=None, prefer=None):
    h={"apikey":SB_KEY,"Authorization":"Bearer "+(token or SB_KEY),"Content-Type":"application/json"}
    if prefer: h["Prefer"]=prefer
    return h

def auth_call(endpoint, payload):
    if not SB_URL or not SB_KEY:
        raise ValueError("أضيفي SUPABASE_URL وSUPABASE_ANON_KEY في Secrets.")
    r=requests.post(f"{SB_URL}/auth/v1/{endpoint}",headers={"apikey":SB_KEY,"Content-Type":"application/json"},json=payload,timeout=25)
    if r.status_code not in (200,201):
        try: msg=r.json().get("msg") or r.json().get("message") or r.json().get("error_description") or r.text
        except Exception: msg=r.text
        raise ValueError(str(msg)[:350])
    return r.json()

def load_data():
    if not st.session_state.user_id: return
    r=requests.get(f"{SB_URL}/rest/v1/miku_user_data",params={"user_id":f"eq.{st.session_state.user_id}","select":"data"},headers=sb_headers(st.session_state.auth_token),timeout=20)
    if r.status_code==200 and r.json():
        stored=r.json()[0].get("data") or {}
        for k in DATA_DEFAULTS:
            if k in stored: st.session_state[k]=stored[k]
    elif r.status_code not in (200,404):
        st.warning("تعذر تحميل البيانات: "+r.text[:200])
    st.session_state.data_loaded=True

def save_data():
    if not st.session_state.user_id or not st.session_state.auth_token: return
    payload={"user_id":st.session_state.user_id,"data":{k:st.session_state.get(k,default) for k,default in DATA_DEFAULTS.items()}}
    try:
        r=requests.post(f"{SB_URL}/rest/v1/miku_user_data",params={"on_conflict":"user_id"},headers=sb_headers(st.session_state.auth_token,"resolution=merge-duplicates,return=minimal"),json=payload,timeout=20)
        if r.status_code not in (200,201,204): st.warning("لم يتم حفظ البيانات: "+r.text[:200])
    except requests.RequestException: st.warning("تعذر الاتصال بقاعدة البيانات.")

def do_logout():
    for k,v in DATA_DEFAULTS.items(): st.session_state[k]=v.copy() if isinstance(v,(list,dict)) else v
    st.session_state.auth_token=None;st.session_state.user_id=None;st.session_state.user_email=None;st.session_state.data_loaded=False
    st.rerun()

# ---------- AI ----------
def normalize_history(history):
    result=[]
    for item in history[-12:]:
        role="model" if item.get("role")=="assistant" else item.get("role")
        txt=str(item.get("text","")).strip()
        if not txt or role not in ("user","model"): continue
        if result and result[-1]["role"]==role: result[-1]["parts"][0]["text"]+="\\n"+txt
        else: result.append({"role":role,"parts":[{"text":txt}]})
    return result

def ask_miku(question):
    if not GEMINI_KEY: return "مفتاح Gemini غير موجود في Secrets (GEMINI_API_KEY)."
    contents=normalize_history(st.session_state.chat_history)
    if not contents or contents[-1]["role"]!="user": contents.append({"role":"user","parts":[{"text":question}]})
    body={"systemInstruction":{"parts":[{"text":"أنتِ ميكو، مساعدة دراسية لطيفة. أجيبي بالعربية الواضحة، واشرحي خطوات مناسبة للطلاب، ولا تختلقي معلومات."}]},"contents":contents,"generationConfig":{"maxOutputTokens":900}}
    # Current primary model; fallback to the stable model for model-availability errors.
    for model in ("gemini-3.8-flash","gemini-2.5-flash"):
        try:
            r=requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",headers={"Content-Type":"application/json","x-goog-api-key":GEMINI_KEY},json=body,timeout=40)
            if r.status_code==200:
                c=r.json().get("candidates",[])
                if not c:return "لم تظهر إجابة هذه المرة. أعيدي إرسال السؤال."
                return "\\n".join(p.get("text","") for p in c[0].get("content",{}).get("parts",[]) if p.get("text")).strip() or "لم يظهر نص الإجابة."
            try: message=r.json().get("error",{}).get("message",r.text)
            except Exception: message=r.text
            if r.status_code not in (404,503): return f"خطأ من Gemini ({r.status_code}): {message[:300]}"
            last_error=message
        except requests.Timeout: return "الاتصال أخذ وقتًا طويلًا؛ جربي مرة أخرى."
        except requests.RequestException: return "تعذر الاتصال بخدمة ميكو. تحققي من الإنترنت."
    return "النموذج غير متاح حاليًا أو عليه ضغط. التفاصيل: "+str(last_error)[:250]

# ---------- Timer functions: declared before page if/elif ----------
def finish_timer():
    st.session_state.timer_running=False
    st.session_state.timer_end=None
    st.session_state.timer_paused_remaining=None
    if st.session_state.timer_mode=="مذاكرة":
        st.session_state.completed_sessions+=1
        st.session_state.xp+=10
        save_data()

def render_timer():
    if st.session_state.timer_running:
        remaining=max(0,int(st.session_state.timer_end-time.time()))
        if remaining==0:
            finish_timer();st.success("انتهت جلسة المذاكرة! +10 XP 🎉");st.balloons();return
    elif st.session_state.timer_paused_remaining is not None:
        remaining=int(st.session_state.timer_paused_remaining)
    else: remaining=int(st.session_state.timer_minutes*60)
    mm,ss=divmod(remaining,60)
    st.markdown(f'<div class="hero-card" style="text-align:center"><div style="font-size:34px">⏳</div><h3>{html.escape(st.session_state.timer_mode)}</h3><div style="font-size:64px;font-weight:800;color:#53799c;direction:ltr">{mm:02d}:{ss:02d}</div><p>ركزي على هدفك 🩵</p></div>',unsafe_allow_html=True)
    if st.session_state.timer_running:
        a,b=st.columns(2)
        with a:
            if st.button("إيقاف مؤقت",key="pause",use_container_width=True):
                st.session_state.timer_paused_remaining=remaining;st.session_state.timer_running=False;st.session_state.timer_end=None;st.rerun()
        with b:
            if st.button("إنهاء",key="end",use_container_width=True):
                st.session_state.timer_running=False;st.session_state.timer_end=None;st.session_state.timer_paused_remaining=None;st.rerun()
    elif st.session_state.timer_paused_remaining is not None:
        a,b=st.columns(2)
        with a:
            if st.button("استئناف ▶",key="resume",use_container_width=True):
                st.session_state.timer_end=time.time()+remaining;st.session_state.timer_running=True;st.session_state.timer_paused_remaining=None;st.rerun()
        with b:
            if st.button("إلغاء",key="cancel",use_container_width=True):
                st.session_state.timer_paused_remaining=None;st.session_state.timer_end=None;st.rerun()
    else:
        a,b=st.columns(2)
        with a:
            if st.button("ابدئي الآن ▶",key="start",use_container_width=True):
                st.session_state.timer_end=time.time()+st.session_state.timer_minutes*60;st.session_state.timer_running=True;st.rerun()
        with b:
            if st.button("إعادة ضبط",key="reset",use_container_width=True): st.rerun()

if hasattr(st,"fragment"):
    @st.fragment(run_every="1s")
    def live_timer(): render_timer()
else:
    def live_timer():
        render_timer()
        st.caption("التحديث التلقائي يتطلب إصدار Streamlit حديثًا.")

# ---------- Login page ----------

  # ---------- Login page ----------
if not st.session_state.auth_token:
    st.markdown(
        '<div class="hero-card" style="text-align:center">'
        '<div class="miku-title">୨୧ Study with Miku ୨୧</div>'
        '<h3>مساحتك الدراسية الصغيرة 🩵</h3>'
        '<p>سجلي دخولك حتى نحفظ مهامك ونقاطك وغرفتك.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    if not SB_URL or not SB_KEY:
        st.error(
            "يلزم إعداد Supabase: SUPABASE_URL وSUPABASE_ANON_KEY في Secrets."
        )

    st.radio(
        "اختاري",
        ["تسجيل الدخول", "إنشاء حساب"],
        horizontal=True,
        key="auth_mode"
    )

    with st.form("auth_form"):
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")

        submit = st.form_submit_button(
            "متابعة 🩵",
            use_container_width=True
        )

        if submit:
            clean_email = email.strip().lower()

            try:
                if not clean_email or not password:
                    st.error("أدخلي البريد وكلمة المرور.")

                elif st.session_state.auth_mode == "إنشاء حساب":
                    data = auth_call(
                        "signup",
                        {
                            "email": clean_email,
                            "password": password
                        }
                    )

                    if data.get("access_token") and data.get("user"):
                        st.session_state.auth_token = data["access_token"]
                        st.session_state.user_id = data["user"]["id"]
                        st.session_state.user_email = clean_email
                        load_data()
                        st.rerun()

                    else:
                        st.success(
                            "تم إنشاء الحساب! أكدي بريدك الإلكتروني من الرسالة "
                            "ثم ارجعي وسجلي الدخول."
                        )

                else:
                    data = auth_call(
                        "token?grant_type=password",
                        {
                            "email": clean_email,
                            "password": password
                        }
                    )

                    user = data.get("user")

                    if not data.get("access_token") or not user:
                        st.error("لم تكتمل عملية تسجيل الدخول. حاولي مرة أخرى.")

                    else:
                        st.session_state.auth_token = data["access_token"]
                        st.session_state.user_id = user["id"]
                        st.session_state.user_email = clean_email

                        load_data()
                        st.rerun()

            except Exception as e:
                error_message = str(e)

                if "Invalid login credentials" in error_message:
                    st.error(
                        "البريد أو كلمة المرور غير صحيحة. "
                        "تأكدي من استخدام نفس بيانات الحساب الذي أنشأتيه."
                    )
                else:
                    st.error("تعذّر تسجيل الدخول: " + error_message)

    st.markdown("---")

    st.markdown("### نسيتِ كلمة المرور؟")

    reset_email = st.text_input(
        "اكتبي بريدك الإلكتروني لاستعادة كلمة المرور",
        key="reset_email"
    )

    if st.button("إرسال رابط استعادة كلمة المرور", use_container_width=True):
        clean_reset_email = reset_email.strip().lower()

        if not clean_reset_email:
            st.warning("اكتبي بريدك الإلكتروني أولًا.")

        elif not SB_URL or not SB_KEY:
            st.error("إعدادات Supabase غير مكتملة.")

        else:
            try:
                response = requests.post(
                    f"{SB_URL}/auth/v1/recover",
                    headers={
                        "apikey": SB_KEY,
                        "Content-Type": "application/json"
                    },
                    json={"email": clean_reset_email},
                    timeout=25
                )

                if response.status_code in (200, 201, 204):
                    st.success(
                        "إذا كان البريد مسجلًا، فسيصلك رابط استعادة كلمة المرور."
                    )
                else:
                    st.error(
                        "تعذّر إرسال الرابط: " + response.text[:250]
                    )

            except requests.RequestException:
                st.error("تعذّر الاتصال بـ Supabase. تحققي من الإنترنت.")

    st.stop()

# ---------- Sidebar and old pastel UI ----------
with st.sidebar:
    st.markdown("<div style='text-align:center;font-size:24px;font-weight:800;color:#54728f'>୨୧ Study with Miku ୨୧</div>",unsafe_allow_html=True)
    st.caption(st.session_state.user_email or "")
    if st.button("تسجيل الخروج",use_container_width=True): do_logout()
    st.markdown("---")
    pages=["الرئيسية","مهامي وواجباتي","اسألي ميكو","جلسة المذاكرة","إنجازاتي","لعبة ميكو"]
    if st.session_state.page not in pages: st.session_state.page="الرئيسية"
    st.radio("القائمة",pages,key="page")
    level,progress=divmod(st.session_state.xp,100);level+=1
    st.markdown(f'<div class="glass-card" style="text-align:center"><div style="font-size:30px">🌷</div><b>مستواك</b><h2>Level {level}</h2><p>{st.session_state.xp} XP</p></div>',unsafe_allow_html=True)

def main_header():
    left,right=st.columns([3,1])
    with left:
        st.markdown('<div class="hero-card"><div class="miku-title">أهلًا بكِ في Study with Miku ୨୧</div><h3>ذاكري معي وخلي إنجازاتك تكبر يومًا بعد يوم!</h3><p>مهامك ونقاطك وجلساتك في مكان واحد 🩵</p></div>',unsafe_allow_html=True)
    with right:
        if os.path.exists("miku.png"): st.image("miku.png",width=190)
        else: st.markdown('<div class="glass-card" style="text-align:center;font-size:70px">🎀</div>',unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#6c86a2;font-weight:700'>ميكو 🩵</p>",unsafe_allow_html=True)

# ---------- Pages ----------
if st.session_state.page=="الرئيسية":
    main_header()
    pending=sum(not t.get("done") for t in st.session_state.tasks)
    c1,c2,c3=st.columns(3);c1.metric("مهام متبقية",pending);c2.metric("XP",st.session_state.xp);c3.metric("جلسات مكتملة",st.session_state.completed_sessions)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="glass-card"><h3>✨ ابدئي إنجازاتك</h3><p>رتبي واجباتك بخطوة بسيطة.</p></div>',unsafe_allow_html=True)
        if st.button("قائمة المهام",use_container_width=True):st.session_state.page="مهامي وواجباتي";st.rerun()
        if st.button("جلسة مذاكرة",use_container_width=True):st.session_state.page="جلسة المذاكرة";st.rerun()
    with c2:
        st.markdown('<div class="glass-card" style="text-align:center"><div style="font-size:42px">🎀</div><h3>ميكو هنا لمساعدتك</h3></div>',unsafe_allow_html=True)
        if st.button("اسألي ميكو",use_container_width=True):st.session_state.page="اسألي ميكو";st.rerun()
    st.markdown("### مهامك القادمة")
    for t in [x for x in st.session_state.tasks if not x.get("done")][:4]:
        st.markdown(f'<div class="task-card"><b>{html.escape(t["title"])}</b><div class="small-note">{html.escape(t["subject"])} · {html.escape(t["priority"])}</div></div>',unsafe_allow_html=True)

elif st.session_state.page=="مهامي وواجباتي":
    st.markdown("# 📚 مهامي وواجباتي")
    with st.expander("＋ إضافة مهمة",expanded=True):
        with st.form("task_form",clear_on_submit=True):
            title=st.text_input("اسم المهمة");subject=st.selectbox("المادة",SUBJECTS);priority=st.selectbox("الأولوية",["عالية","متوسطة","منخفضة"]);due=st.date_input("موعد التسليم",value=None);notes=st.text_area("ملاحظات")
            if st.form_submit_button("إضافة",use_container_width=True):
                if title.strip():
                    st.session_state.tasks.append({"id":str(uuid.uuid4()),"title":title.strip(),"subject":subject,"priority":priority,"date":str(due) if due else "","notes":notes,"done":False});save_data();st.rerun()
                else:st.warning("اكتبي اسم المهمة.")
    for t in list(st.session_state.tasks):
        if t.get("done"):continue
        st.markdown(f'<div class="task-card"><h4>{html.escape(t["title"])}</h4><div class="small-note">{html.escape(t["subject"])} · {html.escape(t["priority"])} · {html.escape(t.get("date") or "بدون موعد")}</div><p>{html.escape(t.get("notes",""))}</p></div>',unsafe_allow_html=True)
        a,b=st.columns(2)
        with a:
            if st.button("✓ اكتملت +20 XP",key="done"+t["id"],use_container_width=True):t["done"]=True;st.session_state.xp+=20;st.session_state.completed_tasks+=1;save_data();st.rerun()
        with b:
            if st.button("حذف",key="del"+t["id"],use_container_width=True):st.session_state.tasks=[x for x in st.session_state.tasks if x["id"]!=t["id"]];save_data();st.rerun()
    st.markdown("### المهام المكتملة")
    for t in [x for x in st.session_state.tasks if x.get("done")]:st.markdown(f'<div class="task-card"><s>{html.escape(t["title"])}</s> ✓</div>',unsafe_allow_html=True)

elif st.session_state.page=="اسألي ميكو":
    st.markdown("# 🎀 اسألي ميكو")
    for m in st.session_state.chat_history:
        cls="chat-user" if m["role"]=="user" else "chat-miku";label="أنتِ 🩵" if m["role"]=="user" else "ميكو 🎀"
        st.markdown(f'<div class="{cls}"><b>{label}</b><br>{html.escape(m["text"]).replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
    with st.form("chat_form",clear_on_submit=True):
        q=st.text_area("اكتبي رسالتك لميكو",placeholder="مثال: اشرحي لي قانون نيوتن الثالث...",height=100)
        if st.form_submit_button("إرسال إلى ميكو ✨",use_container_width=True):
            if q.strip():
                st.session_state.chat_history.append({"role":"user","text":q.strip()})
                with st.spinner("ميكو تفكر... 🩵"): ans=ask_miku(q.strip())
                st.session_state.chat_history.append({"role":"assistant","text":ans});save_data();st.rerun()
            else:st.warning("اكتبي سؤالك.")
    if st.button("مسح المحادثة"):st.session_state.chat_history=[];save_data();st.rerun()

elif st.session_state.page=="جلسة المذاكرة":
    st.markdown("# ⏰ جلسة المذاكرة")
    if not st.session_state.timer_running and st.session_state.timer_paused_remaining is None:
        st.session_state.timer_mode=st.selectbox("نوع الجلسة",["مذاكرة","استراحة"],index=0 if st.session_state.timer_mode=="مذاكرة" else 1,key="mode_select")
        opts=[10,15,20,25,30,45,50,60,90];cur=st.session_state.timer_minutes if st.session_state.timer_minutes in opts else 25
        st.session_state.timer_minutes=st.selectbox("المدة بالدقائق",opts,index=opts.index(cur),key="duration_select")
    live_timer()
    st.markdown(f'<div class="glass-card" style="text-align:center"><h3>🌷 جلسات مكتملة</h3><h2>{st.session_state.completed_sessions}</h2></div>',unsafe_allow_html=True)

elif st.session_state.page=="إنجازاتي":
    st.markdown("# 🏆 إنجازاتي");level,progress=divmod(st.session_state.xp,100);level+=1
    a,b,c=st.columns(3);a.metric("XP",st.session_state.xp);b.metric("المستوى",level);c.metric("مهام مكتملة",st.session_state.completed_tasks)
    st.progress(progress/100);st.caption(f"{progress}/100 XP للمستوى التالي")
    for icon,name,ok in [("🌱","البداية",st.session_state.xp>=10),("📚","أول مهمة",st.session_state.completed_tasks>=1),("⭐","10 مهام",st.session_state.completed_tasks>=10),("⏰","جلسة مذاكرة",st.session_state.completed_sessions>=1),("💎","100 XP",st.session_state.xp>=100),("👑","500 XP",st.session_state.xp>=500)]:
        if ok:st.success(f"{icon} {name} — فتحتي الوسام!")
        else:st.markdown(f'<div class="task-card" style="opacity:.55">{icon} {name} — لم يفتح بعد</div>',unsafe_allow_html=True)

elif st.session_state.page=="لعبة ميكو":
    st.markdown("# 🎮 لعبة ميكو")
    st.markdown('<div class="hero-card"><h3>غرفة ميكو الصغيرة 🩵</h3><p>اجمعي نقاط المذاكرة وافتحي أثاثًا لتزيين الغرفة.</p></div>',unsafe_allow_html=True)
    owned=set(st.session_state.inventory);equipped=set(st.session_state.equipped)
    furniture=" ".join(item[3] for item in SHOP if item[0] in equipped) or "🌸 🪴"
    st.markdown(f'<div style="height:280px;border:2px solid white;border-radius:28px;background:linear-gradient(#dff8ff 0%,#e8e3ff 68%,#f7dff0 69%);display:flex;align-items:center;justify-content:center;flex-direction:column;box-shadow:0 10px 30px #74a5c31c"><div style="font-size:55px">🎀</div><h2>غرفة ميكو</h2><div style="font-size:38px">{furniture}</div><small>معاينة غرفة قابلة للتزيين</small></div>',unsafe_allow_html=True)
    st.markdown(f"### رصيدك: **{st.session_state.xp} XP**")
    cols=st.columns(2)
    for i,(ident,name,cost,emoji) in enumerate(SHOP):
        with cols[i%2]:
            st.markdown(f'<div class="glass-card" style="text-align:center"><div style="font-size:38px">{emoji}</div><h4>{name}</h4><p>{cost} XP</p></div>',unsafe_allow_html=True)
            if ident in owned:
                if ident in equipped:
                    if st.button("إزالة",key="rm"+ident,use_container_width=True):st.session_state.equipped.remove(ident);save_data();st.rerun()
                else:
                    if st.button("وضع في الغرفة",key="put"+ident,use_container_width=True):st.session_state.equipped.append(ident);save_data();st.rerun()
            elif st.button(f"شراء · {cost} XP",key="buy"+ident,use_container_width=True):
                if st.session_state.xp>=cost:st.session_state.xp-=cost;st.session_state.inventory.append(ident);st.session_state.equipped.append(ident);save_data();st.success("تم فتح الأثاث!");st.rerun()
                else:st.warning(f"تحتاجين {cost-st.session_state.xp} XP إضافية.")

# Persist latest changes after page interactions.
save_data()
st.markdown("---")
st.markdown("<div style='text-align:center;color:#8294a8;padding:12px'>୨୧ Study with Miku · خطوة صغيرة كل يوم 🩵 ୨୧</div>",unsafe_allow_html=True)
