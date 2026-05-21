# ShopVuln — แอป E-Commerce ที่มีช่องโหว่โดยตั้งใจ

เว็บแอปพลิเคชันที่ถูกสร้างขึ้นมาให้มีช่องโหว่ด้านความปลอดภัย **โดยตั้งใจ** เพื่อใช้ในการศึกษาเรื่องความปลอดภัยทางไซเบอร์ (CN351)
โดยจำลองช่องโหว่บนเว็บที่พบบ่อย 4 รูปแบบ ภายใต้บริบทของระบบร้านค้าออนไลน์เสมือนจริง

## ช่องโหว่ที่สาธิตภายในระบบ

| # | ช่องโหว่            | Route                       | ผู้รับผิดชอบ |
| - | ------------------- | --------------------------- | ------------ |
| 1 | SQL Injection       | `GET /search?q=`            | Ultimata Sangrungruang |
| 2 | Stored XSS          | `POST /product/<id>/review` | Siranat Phimphicharn |
| 3 | CSRF                | `POST /account/edit`        | Thanawan Phongphaew            |
| 4 | IDOR                | `GET /order/<id>`           | Netchanok Yindee           |
| 5 | Client-Side Control | `POST /buy/<id>`            | Netchanok Yindee           |

## เทคโนโลยีที่ใช้

* **Language:** Python 3.12
* **Framework:** Flask 3.x
* **Database:** SQLite 3 (ผ่านโมดูล `sqlite3`)
* **Template Engine:** Jinja2 + Tailwind CSS (CDN)
* **Dependency Manager:** Poetry

## วิธีติดตั้งและใช้งาน

### สิ่งที่ต้องมีเบื้องต้น

* Python 3.12 ขึ้นไป
* Poetry (`pip install poetry`)

### ขั้นตอนการติดตั้ง

```bash
# 1. Clone โปรเจกต์
git clone <repo-url>
cd vulnerable-ecommerce-app

# 2. ติดตั้ง dependencies
poetry install

# 3. เปิดใช้งาน virtual environment
poetry shell

# 4. สร้างข้อมูลตัวอย่าง (ผู้ใช้, สินค้า, คำสั่งซื้อ)
python seed.py

# 5. รันแอปพลิเคชัน
python main.py
```

หลังจากรันสำเร็จ แอปจะเปิดใช้งานที่
**[http://localhost:5001](http://localhost:5001)** (ค่าเริ่มต้นใน `config.js`)

## บัญชีทดลองใช้งาน

| Username | Password | Role  |
| -------- | -------- | ----- |
| alice    | alice123 | user  |
| bob      | bob456   | user  |
| admin    | admin999 | admin |

## ⚠️ คำเตือน

แอปพลิเคชันนี้ถูกออกแบบให้มีช่องโหว่ด้านความปลอดภัย **โดยตั้งใจ**
ห้ามนำขึ้นใช้งานบน Public Server หรือใช้งานนอกสภาพแวดล้อมสำหรับการศึกษาและการทดลองโดยเด็ดขาด

## License

MIT — ดูรายละเอียดเพิ่มเติมได้ที่ `LICENSE`
