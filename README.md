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

## วิธีติดตั้งและใช้งานโปรเจกต์

### สิ่งที่ต้องมีก่อนเริ่ม

#### 1. ติดตั้ง Python

โปรเจกต์นี้ต้องใช้:

- Python 3.12 ขึ้นไป

ดาวน์โหลดได้จาก:

https://www.python.org/downloads/

ตรวจสอบเวอร์ชัน Python:

```bash
python --version
```

หรือบน Windows:

```bash
py --version
```

ตัวอย่าง:

```bash
Python 3.13.2
```

---

#### 2. ติดตั้ง Poetry

ติดตั้ง Poetry:

```bash
pip install poetry
```

ตรวจสอบเวอร์ชัน Poetry:

```bash
poetry --version
```

ตัวอย่าง:

```bash
Poetry (version 2.1.3)
```

---

## ขั้นตอนการติดตั้งโปรเจกต์

### 1. Clone โปรเจกต์

```bash
git clone <repo-url>
```

### 2. เข้าโฟลเดอร์โปรเจกต์

```bash
cd vulnerable-ecommerce-app
```

### 3. ติดตั้ง dependencies

คำสั่งนี้จะสร้าง virtual environment และติดตั้ง package ทั้งหมดให้อัตโนมัติ

```bash
poetry install
```

---

## วิธีเปิดใช้งาน Virtual Environment

### ตรวจสอบเวอร์ชัน Poetry ก่อน

```bash
poetry --version
```

---

### กรณีใช้ Poetry เวอร์ชันใหม่ (2.x)

#### 1. ขอคำสั่ง activate environment

```bash
poetry env activate
```

ระบบจะคืนคำสั่ง activate มาให้

---

#### 2. รันคำสั่ง activate ตามระบบปฏิบัติการ

##### PowerShell (Windows)

```powershell
& ".venv\Scripts\Activate.ps1"
```

##### CMD (Windows)

```cmd
.venv\Scripts\activate.bat
```

##### macOS / Linux

```bash
source .venv/bin/activate
```

---

### กรณีใช้ Poetry เวอร์ชันเก่า (1.x)

สามารถใช้คำสั่งนี้ได้เลย:

```bash
poetry shell
```

---

## วิธีรันโปรเจกต์

### 1. สร้างข้อมูลตัวอย่าง

```bash
python seed.py
```

### 2. รันแอปพลิเคชัน

```bash
python main.py
```

---

## การเข้าใช้งานแอปพลิเคชัน

หลังจากรันสำเร็จ แอปจะเปิดใช้งานที่:

**[http://localhost:5001](http://localhost:5001)**

(ค่าเริ่มต้นใน `config.js`)

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
