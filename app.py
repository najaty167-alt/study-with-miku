<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Study with Miku</title>
    <!-- استدعاء خطوط فخمة للعربية والإنجليزي -->
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
    <!-- مكتبة Three.js ومحمل مجسمات GLTF -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- 1. شاشة الدخول التفاعلية الأولى (3D Welcome Hub) -->
    <div id="welcome-screen" class="screen active">
        <!-- كانفاس العرض 3D لتتبع العيون والأنيميشن -->
        <div id="canvas-container"></div>

        <!-- القائمة الكريستالية الفخمة -->
        <div class="gothic-menu-container">
            <h1 class="app-title">STUDY WITH MIKU</h1>
            <p class="app-subtitle">RAISON D'ÊTRE</p>

            <nav class="crystal-menu">
                <button class="menu-btn" onclick="navigateTo('timer-screen')">
                    <span class="btn-icon">✦</span>
                    <span class="btn-text" data-en="START STUDY SESSION" data-ar="بدء جلسة المذاكرة">بدء جلسة المذاكرة</span>
                </button>
                <button class="menu-btn" onclick="navigateTo('gallery-screen')">
                    <span class="btn-icon">🌸</span>
                    <span class="btn-text" data-en="MEMORY & GALLERY" data-ar="سجل الذكريات والإنجازات">سجل الذكريات والإنجازات</span>
                </button>
                <button class="menu-btn" onclick="navigateTo('settings-screen')">
                    <span class="btn-icon">⚙</span>
                    <span class="btn-text" data-en="SETTINGS" data-ar="الإعدادات">الإعدادات</span>
                </button>
                <button class="menu-btn exit-btn" onclick="exitApp()">
                    <span class="btn-icon">☾</span>
                    <span class="btn-text" data-en="EXIT" data-ar="خروج">خروج</span>
                </button>
            </nav>
        </div>
    </div>

    <!-- 2. صفحة مؤقت التركيز (صفحة مستقلة بالكامل) -->
    <div id="timer-screen" class="screen">
        <button class="back-btn" onclick="navigateTo('welcome-screen')">➔ العودة للقائمة</button>
        <div class="screen-content">
            <h2>مؤقت التركيز</h2>
            <!-- محتوى المؤقت المنفصل -->
        </div>
    </div>

    <!-- 3. صفحة الملاحظات والدفتر (صفحة مستقلة بالكامل) -->
    <div id="notebook-screen" class="screen">
        <button class="back-btn" onclick="navigateTo('welcome-screen')">➔ العودة للقائمة</button>
        <div class="screen-content">
            <h2>الدفتر الرقمي</h2>
            <!-- محتوى الملاحظات المنفصل -->
        </div>
    </div>

    <!-- 4. صفحة الإعدادات -->
    <div id="settings-screen" class="screen">
        <button class="back-btn" onclick="navigateTo('welcome-screen')">➔ العودة للقائمة</button>
        <div class="screen-content">
            <h2>الإعدادات</h2>
            <!-- خيارات اللغة والصوت -->
        </div>
    </div>

    <script src="app.js"></script>
</body>
</html>
