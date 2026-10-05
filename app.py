import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components

# =========================================================
# 1. إعدادات الصفحة
# =========================================================
st.set_page_config(
    page_title="Study with Miku 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# الربط بمفتاح الذكاء الاصطناعي من Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# تهيئة النقاط والمهام في ذاكرة الجلسة
if "points" not in st.session_state:
    st.session_state.points = 10
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# روابط صور وأنيميشن ميكو المتحركة (تم تحديثها لتناسب ميكو بالشعر الأزرق)
MIKU_GIF_URL = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjM0NTY3ODkwMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L2X6i84z1bUaI/giphy.gif" # صورة ميكو متحركة
MIKU_STUDY_GIF = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIzNDU2Nzg5MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KzDqC8LvCXhxigzxLp/giphy.gif" # صورة ميكو تدرس

# =========================================================
# 2. تنسيقات الـ CSS والتصميم (تم تعديل الألوان لألوان ميكو)
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }
    
    .stApp {
        background-color: #e0f7fa; /* لون خلفية أزرق فاتح جداً */
    }
    
    /* الهيدر الرئيسي */
    .main-header {
        background: linear-gradient(135deg, #39c5bb 0%, #b2ebf2 100%); /* تدرج ألوان ميكو */
        padding: 25px;
        border-radius: 25px;
        text-align: center;
        color: #fff;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* بطاقات الميكو اللطيفة */
    .miku-card {
        background-color: #ffffff;
        border: 2px solid #39c5bb;
        border-radius: 20px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 4px 15px rgba(57, 197, 187, 0.2);
    }
    
    /* مؤشر النقاط */
    .points-badge {
        background-color: #ff4081; /* لون وردي للتباين */
        color: white;
        padding: 8px 18px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        font-size: 16px;
        box-shadow: 0 3px 10px rgba(255, 64, 129, 0.3);
    }
    
    /* أزرار مخصصة */
    .stButton>button {
        background-color: #39c5bb;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #26a69a;
        box-shadow: 0 4px 10px rgba(57, 197, 187, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. القائمة الجانبية (Sidebar) مع ميكو المتحركة
# =========================================================
st.sidebar.image(MIKU_GIF_URL, caption="ميكو جاهزة للمذاكرة! ♡", use_container_width=True)

st.sidebar.title("こんにちは ♡")
st.sidebar.markdown(f"<div class='points-badge'>🏆 نقاطكِ: {st.session_state.points} نقطة</div>", unsafe_allow_html=True)
st.sidebar.write("")

menu = st.sidebar.radio(
    "🌸 خيارات التطبيق:",
    ["الرئيسية", "دراسة مع ميكو ♡", "حل الواجبات", "اسألي ميكو ୨୧", "جلسة مذاكرة ⏱️", "إنجازاتي 🏆"]
)

# =========================================================
# 4. الهيدر الموحد
# =========================================================
st.markdown("""
<div class="main-header">
    <h1>Study with Miku 🌸</h1>
    <p>مساعدتكِ الذكية والمرحة للمذاكرة والتفوق!</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 5. محتوى الصفحات
# =========================================================

# ---------------------------------------------------------
# الصفحة 1: الرئيسية
# ---------------------------------------------------------
if menu == "الرئيسية":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(MIKU_STUDY_GIF, use_container_width=True)
    with col2:
        st.markdown("""
        <div class='miku-card'>
            <h2 style='color: #39c5bb;'>أهلاً بكِ في عالم ميكو للمذاكرة! ୨୧</h2>
            <p>أنا ميكو! سأكون بجانبكِ دائماً لنذاكر معاً، ونحل الواجبات، وننظم أوقاتنا بطريقة ممتعة ومشجعة!</p>
            <ul>
                <li>💬 <b>اسألي ميكو:</b> للاستفسار عن أي درس أو مادة.</li>
                <li>📝 <b>حل الواجبات:</b> ارفعي صورة مسألتكِ وسأشرحها لكِ.</li>
                <li>⏱️ <b>جلسة مذاكرة:</b> مؤقت تفاعلي مع أصوات تقليب الورق وجرس المدرسة.</li>
                <li>🏆 <b>إنجازاتي:</b> اجمعي النقاط وافتحي أوسمة المتفوقات!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# الصفحة 2: دراسة مع ميكو (جدول الأهداف والمهام)
# ---------------------------------------------------------
elif menu == "دراسة مع ميكو ♡":
    st.write("### 📚 قائمة مهام المذاكرة اليومية")
    st.write("أضيفي الدروس والواجبات التي تريدين إنجازها اليوم، وكل مهمة تنهينها تمنحكِ نقاطاً! 🌸")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        new_task = st.text_input("إضافة مهمة جديدة:", placeholder="مثال: مذاكرة الفصل الأول فيزياء...")
    with col2:
        st.write(" ")
        st.write(" ")
        if st.button("إضافة المهمة ✦"):
            if new_task.strip():
                st.session_state.tasks.append({"task": new_task, "done": False})
                st.success("تمت الإضافة!")
                st.rerun()

    st.write("---")
    if not st.session_state.tasks:
        st.info("لا يوجد مهام حالياً! أضيفي مهمتكِ الأولى للبدء. ♡")
    else:
        for idx, item in enumerate(st.session_state.tasks):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"📌 {item['task']}")
            with c2:
                if not item["done"]:
                    if st.button("إنجاز! ✨", key=f"btn_{idx}"):
                        st.session_state.tasks[idx]["done"] = True
                        st.session_state.points += 5
                        st.balloons()
                        st.success("+5 نقاط! أحسنتِ 🌸")
                        st.rerun()
                else:
                    st.write("✅ مكتملة")

# ---------------------------------------------------------
# الصفحة 3: حل الواجبات بالصور
# ---------------------------------------------------------
elif menu == "حل الواجبات":
    st.write("### 📝 حل الواجبات والتمارين مع ميكو")
    st.write("ارفعي صورة التمرين وسأقوم بقراءتها وحلها وشرحها لكِ خطوة بخطوة!")
    
    uploaded_file = st.file_uploader("ارفعي صورة الواجب هنا", type=["png", "jpg", "jpeg"])
    user_prompt = st.text_input("أي ملاحظات إضافية؟", placeholder="مثلاً: اشرحي لي الخطوة الأخيرة...")
    
    if st.button("حل الواجب ✦"):
        if uploaded_file is not None:
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("يرجى التأكد من إضافة GEMINI_API_KEY في قسم Secrets!")
            else:
                try:
                    with st.spinner("ميكو تقرأ المسألة وتحلها لكِ... 🌸"):
                        image = Image.open(uploaded_file)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = f"أنتِ ميكو (Hatsune Miku)، مصممة لمساعدة الطلاب بأدب ولطف وشغف. قومي بحل المسألة في الصورة وشرح الخطوات باللغة العربية بطريقة مبسطة مع إضافة إيموجيات لطيفة. ملاحظات: {user_prompt}"
                        response = model.generate_content([prompt, image])
                        
                        st.session_state.points += 10
                        st.markdown("<div class='miku-card'>", unsafe_allow_html=True)
                        st.write("### 🌸 إجابة ميكو:")
                        st.write(response.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.toast("كسبتِ 10 نقاط لحل الواجب! 🏆")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء تحليل الصورة: {e}")
        else:
            st.warning("يرجى رفع صورة أولاً! ♡")

# ---------------------------------------------------------
# الصفحة 4: اسألي ميكو (شات الذكاء الاصطناعي)
# ---------------------------------------------------------
elif menu == "اسألي ميكو ୨୧":
    st.write("### 💬 اسألي ميكو الذكية")
    st.write("أي سؤال دراسي في الرياضيات، العلوم، اللغات، أو التاريخ... ميكو جاهزة للإجابة!")
    
    question = st.text_area("اكتبي سؤالكِ المباشر هنا:", placeholder="مثال: اشرحي لي كيف تتم عملية البناء الضوئي؟")
    
    if st.button("إرسال لميكو ✦"):
        if question.strip():
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("يرجى التأكد من إضافة GEMINI_API_KEY في قسم Secrets!")
            else:
                try:
                    with st.spinner("ميكو تفكر في الإجابة... 🌸"):
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        system_prompt = (
                            "أنتِ ميكو (Hatsune Miku)، صديقة دراسة لطيفة، ذكية، ومشجعة. "
                            "تحدثي باللغة العربية بأسلوب لطيف ومشجع مع استخدام إيموجيات لطيفة مثل 🌸, ♡, ୨୧, ✦. "
                            "اشرحي المفاهيم الدراسية بأسلوب واضح ومبسط جداً."
                        )
                        full_prompt = f"{system_prompt}\n\nسؤال الطالبة: {question}"
                        response = model.generate_content(full_prompt)
                        
                        st.markdown("<div class='miku-card'>", unsafe_allow_html=True)
                        st.write("### 🌸 رد ميكو:")
                        st.write(response.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {e}")
        else:
            st.warning("يرجى كتابة سؤالكِ أولاً! ♡")

# ---------------------------------------------------------
# الصفحة 5: جلسة مذاكرة (مؤقت تفاعلي مع صوت ورق وجرس)
# ---------------------------------------------------------
elif menu == "جلسة مذاكرة ⏱️":
    st.write("### ⏱️ مؤقت المذاكرة والتركيز مع ميكو")
    st.write("استمتعي بجلسة مذاكرة هادئة! المؤقت يصدر صوت تقليب الورق أثناء العد التنازلي، ويختم بجرس تنبيه عند انتهاء الوقت! 🔔🌸")
    
    timer_minutes = st.number_input("حدد دقائق المذاكرة (مثلاً 25 دقيقة):", min_value=1, max_value=120, value=25)
    
    timer_html = f"""
    <div style="text-align: center; background: #ffffff; padding: 30px; border-radius: 25px; border: 3px solid #39c5bb; box-shadow: 0 6px 20px rgba(57,197,187,0.15); font-family: 'Cairo', sans-serif;">
        <div id="miku-status" style="font-size: 22px; font-weight: bold; color: #ff4081; margin-bottom: 15px;">🌸 ميكو مستعدة للمذاكرة معكِ...</div>
        
        <div id="time-display" style="font-size: 75px; font-weight: bold; color: #39c5bb; font-family: monospace; letter-spacing: 4px; background: #e0f7fa; border-radius: 20px; display: inline-block; padding: 15px 40px; border: 3px dashed #39c5bb; box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);">
            {timer_minutes:02d}:00
        </div>
        
        <div style="margin-top: 25px;">
            <button onclick="startTimer()" style="background-color: #ff4081; color: white; border: none; padding: 14px 32px; border-radius: 30px; font-size: 18px; font-weight: bold; cursor: pointer; margin: 6px; box-shadow: 0 4px 12px rgba(255, 64, 129, 0.3);">بدء الدرس 🚀</button>
            <button onclick="pauseTimer()" style="background-color: #e0f7fa; color: #333; border: none; padding: 14px 32px; border-radius: 30px; font-size: 18px; font-weight: bold; cursor: pointer; margin: 6px;">إيقاف مؤقت ⏸️</button>
            <button onclick="resetTimer()" style="background-color: #e0e0e0; color: #444; border: none; padding: 14px 32px; border-radius: 30px; font-size: 18px; font-weight: bold; cursor: pointer; margin: 6px;">إعادة ضبط 🔄</button>
        </div>

        <audio id="bell-sound" src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" preload="auto"></audio>
        <audio id="paper-sound" src="https://assets.mixkit.co/active_storage/sfx/1470/1470-preview.mp3" preload="auto"></audio>

        <script>
            let totalSeconds = {timer_minutes} * 60;
            let initialSeconds = totalSeconds;
            let timerInterval = null;

            const display = document.getElementById('time-display');
            const bellSound = document.getElementById('bell-sound');
            const paperSound = document.getElementById('paper-sound');
            const mikuStatus = document.getElementById('miku-status');

            function updateDisplay(secs) {{
                let mins = Math.floor(secs / 60);
                let remSecs = secs % 60;
                display.innerText = (mins < 10 ? '0' : '') + mins + ':' + (remSecs < 10 ? '0' : '') + remSecs;
            }}

            function startTimer() {{
                if (timerInterval) return;
                mikuStatus.innerText = "📚 ركزي جيداً.. ميكو تدرس معكِ الآن!";
                
                timerInterval = setInterval(() => {{
                    if (totalSeconds > 0) {{
                        totalSeconds--;
                        updateDisplay(totalSeconds);
                        
                        paperSound.currentTime = 0;
                        paperSound.volume = 0.3;
                        paperSound.play().catch(e => console.log(e));
                    }} else {{
                        clearInterval(timerInterval);
                        timerInterval = null;
                        mikuStatus.innerText = "🔔 انتهى وقت الدرس! أحسنتِ المذاكرة 🌸✨";
                        bellSound.volume = 1.0;
                        bellSound.play().catch(e => console.log(e));
                    }}
                }}, 1000);
            }}

            function pauseTimer() {{
                clearInterval(timerInterval);
                timerInterval = null;
                mikuStatus.innerText = "⏸️ المؤقت متوقف مؤقتاً";
            }}

            function resetTimer() {{
                clearInterval(timerInterval);
                timerInterval = null;
                totalSeconds = initialSeconds;
                updateDisplay(totalSeconds);
                mikuStatus.innerText = "🌸 جاهزة لبدء الجلسة؟";
            }}
        </script>
    </div>
    """
    
    components.html(timer_html, height=360)

# ---------------------------------------------------------
# الصفحة 6: إنجازاتي والأوسمة
# ---------------------------------------------------------
elif menu == "إنجازاتي 🏆":
    st.write("### 🏆 قائمة إنجازاتكِ وأوسمة المتفوقات")
    st.write("كلما ذاكرتِ وحللتِ الواجبات مع ميكو تكسبين نقاطاً وتفتحين أوسمة جديدة!")
    
    st.markdown(f"""
    <div class='miku-card' style='text-align: center;'>
        <h2 style='color: #ff4081;'>مجموع نقاطكِ الحالي:</h2>
        <h1 style='color: #39C5BB; font-size: 50px;'>{st.session_state.points} 🌸</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 🎖️ الأوسمة التي فتحتها:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='miku-card' style='text-align:center;'>🌱<br><b>بداية الشغف</b><br><small>10 نقاط</small></div>", unsafe_allow_html=True)
    with col2:
        if st.session_state.points >= 30:
            st.markdown("<div class='miku-card' style='text-align:center;'>⭐<br><b>بطلة التركيز</b><br><small>30 نقطة</small></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='miku-card' style='text-align:center; opacity: 0.4;'>🔒<br><b>بطلة التركيز</b><br><small>تحتاج 30 نقطة</small></div>", unsafe_allow_html=True)
    with col3:
        if st.session_state.points >= 50:
            st.markdown("<div class='miku-card' style='text-align:center;'>👑<br><b>أسطورة ميكو</b><br><small>50 نقطة</small></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='miku-card' style='text-align:center; opacity: 0.4;'>🔒<br><b>أسطورة ميكو</b><br><small>تحتاج 50 نقطة</small></div>", unsafe_allow_html=True)
