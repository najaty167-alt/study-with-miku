import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Study with Miku", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: #060b19; 
            color: #fff; 
            font-family: 'Tajawal', sans-serif; 
            overflow: hidden; 
            height: 100vh;
        }
        #canvas-container { 
            position: absolute; 
            top: 0; left: 0; 
            width: 100%; height: 100%; 
            z-index: 1; 
        }
        .gothic-container {
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            justify-content: center;
            height: 100vh;
            padding-right: 8%;
            background: radial-gradient(circle at 30% 50%, rgba(10, 25, 50, 0.4), transparent 70%);
        }
        .title-box { text-align: center; margin-bottom: 30px; text-shadow: 0 0 15px #82d9ec; }
        .app-title { font-family: 'Cinzel', serif; font-size: 2.8rem; color: #b8eff7; letter-spacing: 2px; }
        .app-sub { font-family: 'Cinzel', serif; font-size: 1rem; color: #5bc0be; letter-spacing: 4px; }
        
        .crystal-menu {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 280px;
        }
        .menu-btn {
            background: rgba(13, 34, 64, 0.55);
            border: 1px solid rgba(130, 217, 236, 0.4);
            backdrop-filter: blur(10px);
            color: #e0f7fa;
            padding: 14px 20px;
            border-radius: 8px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            text-align: right;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .menu-btn:hover {
            background: rgba(30, 80, 130, 0.7);
            border-color: #82d9ec;
            box-shadow: 0 0 20px rgba(130, 217, 236, 0.6);
            transform: translateX(-5px);
        }
    </style>
</head>
<body>

    <div id="canvas-container"></div>

    <div class="gothic-container">
        <div class="title-box">
            <h1 class="app-title">STUDY WITH MIKU</h1>
            <p class="app-sub">RAISON D'ÊTRE</p>
        </div>

        <nav class="crystal-menu">
            <button class="menu-btn"><span>بدء جلسة المذاكرة</span> <span>✦</span></button>
            <button class="menu-btn"><span>سجل الذكريات</span> <span>🌸</span></button>
            <button class="menu-btn"><span>الإعدادات</span> <span>⚙</span></button>
            <button class="menu-btn"><span>خروج</span> <span>☾</span></button>
        </nav>
    </div>

    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        const light = new THREE.AmbientLight(0xffffff, 1.5);
        scene.add(light);
        const dirLight = new THREE.DirectionalLight(0x82d9ec, 2.5);
        dirLight.position.set(-5, 5, 5);
        scene.add(dirLight);

        camera.position.set(0, 0, 5);

        // تم ضبط الكود وجاهز لاستبدال الرابط برابط نموذج ميكو الخاص بكِ مباشرة
        const loader = new THREE.GLTFLoader();
        let mikuModel;

        // وضعنا مجسم أنيمي ناعم مؤقت ريثما نربط رابط ميكو الخاص بكِ
        loader.load('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoxAnimated/glTF-Binary/BoxAnimated.glb', function (gltf) {
            mikuModel = gltf.scene;
            mikuModel.scale.set(1.2, 1.2, 1.2);
            mikuModel.position.set(-1.2, -0.5, 0);
            scene.add(mikuModel);
        });

        let mouseX = 0, mouseY = 0;
        document.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        });

        function animate() {
            requestAnimationFrame(animate);
            if (mikuModel) {
                mikuModel.rotation.y += (mouseX * 0.5 - mikuModel.rotation.y) * 0.05;
                mikuModel.rotation.x += (-mouseY * 0.3 - mikuModel.rotation.x) * 0.05;
            }
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

components.html(html_code, height=750, scrolling=False)
