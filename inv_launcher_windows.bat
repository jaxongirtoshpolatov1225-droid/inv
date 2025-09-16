@echo off
echo ============================================================
echo 🏢 INVENTARIZATSIYA TIZIMI LAUNCHER (Windows)
echo ============================================================

REM Python mavjudligini tekshirish
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python topilmadi! Python o'rnatilganligini tekshiring.
    pause
    exit /b 1
)

REM app.py faylini tekshirish
if not exist "app.py" (
    echo ❌ Xatolik: app.py fayli topilmadi!
    echo    Bu faylni loyiha papkasida ishga tushiring
    pause
    exit /b 1
)

REM Kutubxonalarni tekshirish va o'rnatish
echo 📦 Kutubxonalarni tekshirish...
python -c "import flask, flask_sqlalchemy, flask_cors, qrcode, PIL, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo ❌ Ba'zi kutubxonalar topilmadi!
    echo 📦 Kutubxonalarni o'rnatish...
    pip install flask flask-sqlalchemy flask-cors qrcode pillow openpyxl
    if errorlevel 1 (
        echo ❌ Kutubxonalar o'rnatilmadi!
        pause
        exit /b 1
    )
    echo ✅ Kutubxonalar o'rnatildi!
)

echo 🚀 Inventarizatsiya tizimini ishga tushirish...
echo 🌐 Brauzerda ochish: http://localhost:5000
echo ⏹️  To'xtatish uchun: Ctrl+C
echo ------------------------------------------------------------

REM Server ishga tushirish
python -c "import app; app.app.run(debug=False, host='0.0.0.0', port=5000)"

pause
