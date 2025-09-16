# Inventarizatsiya Tizimi Launcher (Windows PowerShell)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🏢 INVENTARIZATSIYA TIZIMI LAUNCHER (Windows)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Python mavjudligini tekshirish
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python topildi: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python topilmadi! Python o'rnatilganligini tekshiring." -ForegroundColor Red
    Read-Host "Chiqish uchun Enter bosing"
    exit 1
}

# app.py faylini tekshirish
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Xatolik: app.py fayli topilmadi!" -ForegroundColor Red
    Write-Host "   Bu faylni loyiha papkasida ishga tushiring" -ForegroundColor Yellow
    Read-Host "Chiqish uchun Enter bosing"
    exit 1
}

# Kutubxonalarni tekshirish
Write-Host "📦 Kutubxonalarni tekshirish..." -ForegroundColor Yellow

try {
    python -c "import flask, flask_sqlalchemy, flask_cors, qrcode, PIL, openpyxl" 2>$null
    Write-Host "✅ Barcha kutubxonalar mavjud" -ForegroundColor Green
} catch {
    Write-Host "❌ Ba'zi kutubxonalar topilmadi!" -ForegroundColor Red
    Write-Host "📦 Kutubxonalarni o'rnatish..." -ForegroundColor Yellow
    
    try {
        pip install flask flask-sqlalchemy flask-cors qrcode pillow openpyxl
        Write-Host "✅ Kutubxonalar o'rnatildi!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Kutubxonalar o'rnatilmadi!" -ForegroundColor Red
        Read-Host "Chiqish uchun Enter bosing"
        exit 1
    }
}

# Server ishga tushirish
Write-Host "🚀 Inventarizatsiya tizimini ishga tushirish..." -ForegroundColor Green
Write-Host "🌐 Brauzerda ochish: http://localhost:5000" -ForegroundColor Cyan
Write-Host "⏹️  To'xtatish uchun: Ctrl+C" -ForegroundColor Yellow
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan

# Brauzerda ochish
Start-Process "http://localhost:5000"

# Server ishga tushirish
try {
    python -c "import app; app.app.run(debug=False, host='0.0.0.0', port=5000)"
} catch {
    Write-Host "❌ Server ishga tushmadi!" -ForegroundColor Red
    Read-Host "Chiqish uchun Enter bosing"
}
