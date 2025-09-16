#!/usr/bin/env python3
"""
Inventarizatsiya Tizimi Launcher
Bu fayl loyihani ishga tushirish uchun yaratilgan
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Kerakli kutubxonalarni tekshirish"""
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_cors',
        'qrcode',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Quyidagi kutubxonalar topilmadi:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Kutubxonalarni o'rnatish uchun:")
        print("   pip install --user --break-system-packages flask flask-sqlalchemy flask-cors qrcode pillow")
        return False
    
    print("✅ Barcha kutubxonalar mavjud")
    return True

def start_server():
    """Server ishga tushirish"""
    print("🚀 Inventarizatsiya tizimini ishga tushirish...")
    
    # Python executable topish
    python_executable = "/usr/bin/python3"
    
    if not os.path.exists(python_executable):
        python_executable = "python3"
    
    # Server ishga tushirish
    try:
        print("📡 Server ishga tushirilmoqda...")
        print("🌐 Brauzerda ochish: http://localhost:5000")
        print("⏹️  To'xtatish uchun: Ctrl+C")
        print("-" * 50)
        
        # Server ishga tushirish
        process = subprocess.Popen([
            python_executable, 
            "-c", 
            "import app; app.app.run(debug=False, host='0.0.0.0', port=5000)"
        ])
        
        # Brauzerda ochish
        time.sleep(2)
        try:
            webbrowser.open('http://localhost:5000')
            print("🌐 Brauzerda ochildi!")
        except:
            print("⚠️  Brauzer avtomatik ochilmadi. Qo'lda oching: http://localhost:5000")
        
        # Server ishga tushguncha kutish
        process.wait()
        
    except KeyboardInterrupt:
        print("\n⏹️  Server to'xtatildi")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False
    
    return True

def main():
    """Asosiy funksiya"""
    print("=" * 60)
    print("🏢 INVENTARIZATSIYA TIZIMI LAUNCHER")
    print("=" * 60)
    
    # Joriy papkada ekanligini tekshirish
    if not os.path.exists('app.py'):
        print("❌ Xatolik: app.py fayli topilmadi!")
        print("   Bu faylni loyiha papkasida ishga tushiring")
        return
    
    # Kutubxonalarni tekshirish
    if not check_dependencies():
        return
    
    # Server ishga tushirish
    start_server()

if __name__ == "__main__":
    main()
