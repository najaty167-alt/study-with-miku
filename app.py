import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

# =========================
# إعدادات التطبيق
# =========================
st.set_page_config(
    page_title="Miku World",
    page_icon="🩵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# مجسّم ميكو، نضيفه لاحقًا داخل مجلد assets
MODEL_PATH = Path("assets/miku.glb")

# =========================
# التصميم العام
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Tajawal:wght@400;500;600;700;800&display=swap');

:root {
    --aqua: #68e7e9;
    --sky: #d9f7ff;
    --lavender: #ded4ff;
    --pink: #ffd8ed;
    --dark: #285477;
}

html, body, [class*="css"] {
    font-family: 'Tajawal', 'Baloo 2', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 78% 15%, #d9fbff 0%, transparent 36%),
        radial-gradient(ellipse at 12% 82%, #e8ddff 0%, transparent 42%),
        linear-gradient(135deg, #f8fdff, #e5f8ff 55%, #f5edff);
    color: var(--dark);
}

.block-container {
    max-width: 1400px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

header, footer {
    visibility: hidden;
}

h1, h2, h3 {
    color: #285477 !important;
    font-family: 'Baloo 2', 'Tajawal', sans-serif !important;
}

.hero {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.94),
        rgba(220,247,255,.78)
    );
    border: 2px solid rgba(255,255,255,.9);
    border-radius: 30px;
    padding: 26px;
    box-shadow:
        0 18px 40px rgba(96,168,203,.18),
        inset 0 2px 0 white;
}

.intro {
    color: #557b98;
    font-size: 1.12rem;
    line-height: 2;
}

div.stButton > button {
    border: 1px solid white;
    border-radius: 18px;
    min-height: 3.2rem;
    background: linear-gradient(145deg, #ffffff, #d9f8ff);
    color: #285477;
    font-weight: 800;
    box-shadow:
        0 7px 0 #b5e0ed,
        0 12px 22px rgba(75,155,195,.15);
    transition: all .18s ease;
}

div.stButton > button:hover {
    transform: translateY(-3px);
    background: linear-gradient(145deg, #e7ffff, #d7eaff);
    color: #285477;
    box-shadow:
        0 10px 0 #b5e0ed,
        0 15px 25px rgba(75,155,195,.2);
}

div.stButton > button:active {
    transform: translateY(2px);
    box-shadow: 0 3px 0 #b5e0ed;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e3faff, #eee7ff);
    border-right: 1px solid white;
}

[data-testid="stSidebar"] button {
    border-radius: 15px;
}

.stTextInput input,
.stSelectbox div,
.stTextArea textarea {
    border-radius: 15px !important;
}

.small-note {
    color: #7899b0;
    text-align: center;
    font-size: .9rem;
    margin-top: 25px;
}

.sparkle {
    color: #83dfe8;
    font-size: 1.3rem;
}
</style>
""", unsafe_allow_html=True)


# =========================
# حفظ الصفحات
# =========================
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def go_to(page):
    st.session_state.page = page


# =========================
# مجسّم ميكو ثلاثي الأبعاد
# =========================
def show_miku_3d():

    model_data = ""

    if MODEL_PATH.exists():
        model_data = base64.b64encode(
            MODEL_PATH.read_bytes()
        ).decode("utf-8")

    html = f"""
    <div id="miku-scene"
         style="
            width:100%;
            height:500px;
            border-radius:30px;
            overflow:hidden;
            background:
              radial-gradient(ellipse at 50% 75%,
                rgba(100,230,240,.35),
                transparent 45%),
              linear-gradient(145deg,#e7fbff,#e9e1ff);
         ">
    </div>

    <script type="importmap">
    {{
      "imports": {{
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
      }}
    }}
    </script>

    <script type="module">
    import * as THREE from 'three';
    import {{ GLTFLoader }} from 'three/addons/loaders/GLTFLoader.js';

    const container = document.getElementById('miku-scene');

    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
        35,
        container.clientWidth / container.clientHeight,
        0.1,
        100
    );

    camera.position.set(0, 1.2, 5.5);

    const renderer = new THREE.WebGLRenderer({{
        alpha: true,
        antialias: true
    }});

    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;

    container.appendChild(renderer.domElement);

    // إضاءة ناعمة
    const hemi = new THREE.HemisphereLight(
        0xffffff,
        0xb7d9ff,
        2.3
    );

    scene.add(hemi);

    const keyLight = new THREE.DirectionalLight(0xffffff, 3);
    keyLight.position.set(3, 4, 5);
    scene.add(keyLight);

    const aquaLight = new THREE.PointLight(0x9afaff, 20, 12);
    aquaLight.position.set(-3, 1, 2);
    scene.add(aquaLight);

    // أرضية ضوئية
    const floor = new THREE.Mesh(
        new THREE.CircleGeometry(1.5, 64),
        new THREE.MeshBasicMaterial({
            color: 0x8deaf1,
            transparent: true,
            opacity: 0.22
        })
    );

    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -1.2;
    scene.add(floor);

    let character = null;

    const modelBase64 = "{model_data}";

    if (modelBase64) {

        const loader = new GLTFLoader();

        const binary = Uint8Array.from(
            atob(modelBase64),
            c => c.charCodeAt(0)
        ).buffer;

        loader.parse(binary, "", function(gltf) {

            character = gltf.scene;

            const box = new THREE.Box3().setFromObject(character);
            const size = box.getSize(new THREE.Vector3());
            const center = box.getCenter(new THREE.Vector3());

            character.position.sub(center);

            const maxSize = Math.max(size.x, size.y, size.z);

            character.scale.setScalar(2.6 / maxSize);
            character.position.y = -0.25;

            scene.add(character);

        }, function(error) {
            console.log("Model loading error:", error);
        });

    } else {

        // مجسّم مؤقت ثلاثي الأبعاد حتى نضيف ميكو
        const orb = new THREE.Mesh(
            new THREE.SphereGeometry(0.85, 48, 48),
            new THREE.MeshPhysicalMaterial({
                color: 0x78e7ef,
                roughness: 0.2,
                metalness: 0.1,
                clearcoat: 1
            })
        );

        orb.position.y = 0.1;
        scene.add(orb);

        const ring = new THREE.Mesh(
            new THREE.TorusGeometry(1.15, 0.035, 12, 90),
            new THREE.MeshBasicMaterial({
                color: 0xc7aaff
            })
        );

        ring.rotation.x = 1.15;
        ring.position.y = 0.1;
        scene.add(ring);

        character = orb;
    }

    // حركة طفو خفيفة
    let time = 0;

    function animate() {

        requestAnimationFrame(animate);

        time += 0.012;

        if (character) {
            character.position.y += Math.sin(time) * 0.0018;
            character.rotation.y = Math.sin(time * 0.6) * 0.14;
        }

        renderer.render(scene, camera);
    }

    animate();

    // تغيير حجم المشهد مع الشاشة
    window.addEventListener("resize", function() {

        camera.aspect =
            container.clientWidth / container.clientHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            container.clientWidth,
            container.clientHeight
        );

    });

    </script>
    """

    components.html(html, height=515, scrolling=False)


# =========================
# القائمة الجانبية
# =========================
with st.sidebar:

    st.markdown("## ୨୧ MIKU MENU 🩵")
    st.caption("Your cute study world")

    if st.button("🏠  الرئيسية", use_container_width=True):
        go_to("home")

    if st.button("📚  مهامي وواجباتي", use_container_width=True):
        go_to("tasks")

    if st.button("💬  اسألي ميكو", use_container_width=True):
        go_to("chat")

    if st.button("🏆  إنجازاتي", use_container_width=True):
        go_to("achievements")

    if st.button("🎀  تغيير شكل ميكو", use_container_width=True):
        go_to("change_miku")

    if st.button("⚙️  الإعدادات", use_container_width=True):
        go_to("settings")

    st.markdown("---")
    st.caption("Made with ♡ in Miku World")


# =========================
# صفحة البداية
# =========================
if st.session_state.page == "welcome":

    left, right = st.columns([1.05, 1.2], gap="large")

    with left:

        st.markdown('<div class="hero">', unsafe_allow_html=True)

        st.markdown("# Welcome to Miku World ♡")

        st.markdown("""
        <p class="intro">
        عالمك الصغير للدراسة والإنجاز والإبداع.<br>
        كل خطوة تخطينها هنا تقرّبك من هدفك…<br>
        وميكو معك في كل لحظة! 🩵
        </p>
        """, unsafe_allow_html=True)

        st.markdown("### Ready to begin your journey? ✦")

        if st.button("✦  ENTER APP  ✦", use_container_width=True):
            go_to("home")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🏆 Achievements", use_container_width=True):
                go_to("achievements")

        with col2:
            if st.button("⚙️ Settings", use_container_width=True):
                go_to("settings")

        if st.button("୨୧ Change Miku", use_container_width=True):
            go_to("change_miku")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        show_miku_3d()


# =========================
# الصفحة الرئيسية
# =========================
elif st.session_state.page == "home":

    st.markdown("# أهلاً بكِ في عالم ميكو 🩵")

    left, right = st.columns([1.05, 1.2], gap="large")

    with left:

        st.markdown("""
        <div class="hero">
        <h2>Ready to begin your journey? ♡</h2>
        <p class="intro">
        اختاري قسمك وابدئي خطوة صغيرة نحو إنجاز كبير.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button("📚 مهامي وواجباتي", use_container_width=True):
            go_to("tasks")

        if st.button("💬 اسألي ميكو", use_container_width=True):
            go_to("chat")

        if st.button("🏆 إنجازاتي", use_container_width=True):
            go_to("achievements")

    with right:
        show_miku_3d()


# =========================
# المهام والواجبات
# =========================
elif st.session_state.page == "tasks":

    st.markdown("# 📚 مهامي وواجباتي")

    st.markdown("""
    <div class="hero">
    <h3>كل مهمة تخلصينها هي إنجاز جديد ✨</h3>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    task_name = st.text_input("اسم المهمة")

    subjects = [
        "رياضيات متقدمة",
        "رياضيات أساسية",
        "فيزياء",
        "كيمياء",
        "أحياء",
        "علوم بيئة",
        "عربي",
        "إنجليزي",
        "فرنسي",
        "تاريخ",
        "جغرافيا",
        "دراسات إسلامية",
        "فنون",
        "موسيقى",
        "تقنية",
        "رياضة"
    ]

    subject = st.selectbox("اختاري المادة", subjects)

    if st.button("＋ إضافة المهمة", use_container_width=True):

        if task_name.strip():

            st.session_state.tasks.append({
                "name": task_name.strip(),
                "subject": subject,
                "done": False
            })

            st.success("تمت إضافة المهمة 🩵")
            st.rerun()

        else:
            st.warning("اكتبي اسم المهمة أولًا.")

    st.write("---")
    st.markdown("### قائمة مهامي")

    if not st.session_state.tasks:

        st.info("ما عندك مهام حاليًا، أضيفي أول مهمة!")

    else:

        for i, task in enumerate(st.session_state.tasks):

            checked = st.checkbox(
                f"{task['subject']} — {task['name']}",
                value=task["done"],
                key=f"task_{i}"
            )

            if checked and not task["done"]:

                task["done"] = True
                st.session_state.xp += 25
                st.success("أحسنتِ! حصلتِ على 25 XP 🩵")

            elif not checked and task["done"]:

                task["done"] = False
                st.session_state.xp = max(
                    0,
                    st.session_state.xp - 25
                )


# =========================
# اسألي ميكو
# =========================
elif st.session_state.page == "chat":

    st.markdown("# 💬 اسألي ميكو")

    st.markdown("""
    <div class="hero">
    <h3>ميكو هنا عشان تساعدك 🩵</h3>
    <p class="intro">
    قريبًا نربط المحادثة بالذكاء الاصطناعي،
    عشان تسألين ميكو عن دروسك وواجباتك.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("اكتبي سؤالك لميكو...")

    if user_message:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "وصلني سؤالك! ربط الذكاء الاصطناعي يحتاج إعداد مفتاح Gemini في Secrets."
        })

        st.rerun()


# =========================
# الإنجازات
# =========================
elif st.session_state.page == "achievements":

    st.markdown("# 🏆 إنجازاتي")

    level = (st.session_state.xp // 100) + 1

    st.markdown(f"""
    <div class="hero">
        <h2>كل إنجاز صغير يستحق الاحتفال ✨</h2>
        <h3>⭐ Level {level}</h3>
        <h3>🩵 XP: {st.session_state.xp}</h3>
        <p class="intro">
        استمري، كل مهمة تخلصينها تقرّبك من المستوى القادم!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.progress((st.session_state.xp % 100) / 100)


# =========================
# تغيير شكل ميكو
# =========================
elif st.session_state.page == "change_miku":

    st.markdown("# 🎀 تغيير شكل ميكو")

    st.markdown("""
    <div class="hero">
    <h2>اختاري الستايل اللي تحبينه ♡</h2>
    <p class="intro">
    سنضيف خيارات تغيير شكل ميكو بعد تجهيز ملفات الشخصيات.
    </p>
    </div>
    """, unsafe_allow_html=True)

    show_miku_3d()


# =========================
# الإعدادات
# =========================
elif st.session_state.page == "settings":

    st.markdown("# ⚙️ الإعدادات")

    st.markdown("""
    <div class="hero">
    <h2>إعدادات Miku World 🩵</h2>
    <p class="intro">
    هنا نقدر نضيف إعدادات الحساب، الألوان،
    وتخصيص واجهة التطبيق.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("⬅ العودة إلى البداية", use_container_width=True):
        go_to("welcome")


# =========================
# تذييل
# =========================
st.markdown("""
<p class="small-note">
୨୧ Miku World · Study with sparkle ♡
</p>
""", unsafe_allow_html=True)