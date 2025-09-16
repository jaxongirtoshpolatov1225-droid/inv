# Inventarizatsiya Tizimi

Bu loyiha Python Flask va Bootstrap yordamida yaratilgan inventarizatsiya boshqarish tizimi.

## Xususiyatlar

- **Tashkilot boshqaruvi**: Yangi tashkilot qo'shish va ularni boshqarish
- **Qavat boshqaruvi**: Tashkilotda qavatlar mavjud bo'lsa, ularni boshqarish
- **Xona boshqaruvi**: Har bir qavatda yoki to'g'ridan-to'g'ri tashkilotda xonalar qo'shish
- **Jihoz boshqaruvi**: Har bir xonada jihozlar ro'yxatini boshqarish
- **QR kod yaratish**: Har bir jihoz uchun inventarizatsiya QR kodi yaratish
- **Ikki tabli ma'lumot kiritish**: Asosiy va qo'shimcha ma'lumotlar

## O'rnatish

1. Loyihani klonlang:
```bash
git clone <repository-url>
cd smart-mony
```

2. Virtual environment yarating:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

3. Kerakli kutubxonalarni o'rnating:
```bash
pip install -r requirements.txt
```

4. Loyihani ishga tushiring:
```bash
python app.py
```

5. Brauzerda oching: `http://localhost:5000`

## Foydalanish

### 1. Tashkilot qo'shish
- Bosh sahifada "Yangi tashkilot qo'shish" tugmasini bosing
- Tashkilot nomini kiriting
- Agar tashkilotda qavatlar mavjud bo'lsa, checkboxni belgilang

### 2. Qavat qo'shish (ixtiyoriy)
- Agar tashkilot qavatli bo'lsa, qavatlar sahifasida yangi qavat qo'shing

### 3. Xona qo'shish
- Qavat sahifasida yoki to'g'ridan-to'g'ri tashkilot sahifasida xona qo'shing

### 4. Jihoz qo'shish
- Xona sahifasida "Yangi jihoz qo'shish" tugmasini bosing
- Asosiy ma'lumotlar tabida:
  - Jihoz nomi (majburiy)
  - Kategoriya (majburiy)
  - Brend va model
- Qo'shimcha ma'lumotlar tabida:
  - Seriya raqami
  - Sotib olingan sana
  - Narx
  - Holat
  - Tavsif

### 5. QR kod yaratish
- Jihoz ro'yxatida "QR kod" tugmasini bosing
- QR kod avtomatik yaratiladi va chop etish mumkin

## Ma'lumotlar bazasi

Loyiha SQLite ma'lumotlar bazasidan foydalanadi. Ma'lumotlar `inventory.db` faylida saqlanadi.

## Texnologiyalar

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Ma'lumotlar bazasi**: SQLite
- **QR kod**: qrcode kutubxonasi

## Loyiha tuzilishi

```
smart-mony/
├── app.py                 # Asosiy Flask ilovasi
├── requirements.txt       # Python kutubxonalari
├── inventory.db          # SQLite ma'lumotlar bazasi (avtomatik yaratiladi)
├── templates/            # HTML templatelar
│   ├── base.html
│   ├── index.html
│   ├── organization_with_floors.html
│   ├── organization_direct_rooms.html
│   ├── floor.html
│   └── room.html
└── static/              # Statik fayllar
    ├── css/
    └── js/
```

## Inventarizatsiya kodi formati

Har bir jihoz uchun inventarizatsiya kodi quyidagi formatda yaratiladi:
`TASHKILOT_QISQARTMASI-XONA_QISQARTMASI-RAQAM`

Masalan: `TOS-101-0001` (Toshkent shahri, 101-xona, 1-jihoz)
