### ช่องโหว่ที่ 3: Cross-Site Request Forgery (CSRF)

---

#### คำอธิบายช่องโหว่

Cross-Site Request Forgery (CSRF) คือการโจมตีที่หลอกให้เบราว์เซอร์ของผู้ใช้ที่
ล็อกอินอยู่ส่งคำขอที่ไม่ได้รับอนุญาตไปยังเว็บแอปพลิเคชันที่เชื่อถือ
เนื่องจากเบราว์เซอร์จะแนบ session cookie ไปกับทุก request โดยอัตโนมัติ
เซิร์ฟเวอร์จึงไม่สามารถแยกแยะระหว่าง request จริงกับ request ปลอมได้

ช่องโหว่ CSRF เกิดขึ้นเมื่อครบ **3 เงื่อนไข** พร้อมกัน:
1. มี action ที่มีความสำคัญ (privileged action) ที่ผู้โจมตีต้องการ trigger
2. แอปพลิเคชันใช้ **เฉพาะ HTTP cookie** ในการระบุตัวตนผู้ใช้ ไม่มี token อื่น
3. ผู้โจมตีสามารถ **คาดเดาค่า parameter ทุกตัว** ที่ต้องส่งใน request ได้ล่วงหน้า

**ตำแหน่งในแอปพลิเคชัน:** `POST /account/edit` → `app/routes/account.py`

---

#### Methodology ตาม Chapter 21

**ขั้นที่ 1 — Mapping the Application (สำรวจแอปพลิเคชัน)**

ระบุ endpoint ทั้งหมดที่เปลี่ยนแปลงสถานะข้อมูล (state-changing) ได้แก่:
- `POST /account/edit` — เปลี่ยน email ของผู้ใช้
- `POST /account/password` — เปลี่ยนรหัสผ่าน

โดยใช้ Burp Suite ดัก traffic ขณะใช้งานแอปตามปกติ เพื่อสร้าง request map

**ขั้นที่ 2 — Identifying Attack Surfaces (ระบุพื้นที่เสี่ยง)**

ตรวจสอบ `POST /account/edit` พบว่า:
- ไม่มี CSRF token ใน form
- ไม่มีการตรวจสอบ `Origin` หรือ `Referer` header
- ไม่มี `SameSite` attribute บน session cookie
- ค่า parameter (`email`) สามารถกำหนดล่วงหน้าได้ทั้งหมด

→ ครบทั้ง 3 เงื่อนไข = **ช่องโหว่ CSRF ยืนยัน**

**ขั้นที่ 3 — Analyzing Inputs and Parameters (วิเคราะห์ input)**

```
POST /account/edit HTTP/1.1
Host: localhost:5001
Cookie: session=<alice_session_token>
Content-Type: application/x-www-form-urlencoded

email=newemail@example.com
```

ไม่มี secret value ใดๆ ใน body — ผู้โจมตีสามารถสร้าง request เหมือนกันทุกประการ

**ขั้นที่ 4 — Testing Hypotheses (ทดสอบสมมติฐาน)**

สร้างไฟล์ `evil.html` ที่ host บน origin อื่น (`http://localhost:8080`)
โดยใช้ hidden form ที่ auto-submit ทันทีที่หน้าโหลด:

```html
<!-- evil.html -->
<html>
<body onload="document.forms[0].submit()">
  <form action="http://localhost:5001/account/edit"
        method="POST"
        style="display:none">
    <input type="hidden" name="email" value="hacked@attacker.com">
  </form>
  <p>Loading...</p>
</body>
</html>
```

**ขั้นที่ 5 — Exploitation (การโจมตี)**

ขณะที่ alice ล็อกอินอยู่ที่ `localhost:5001` และเปิด `evil.html`
เบราว์เซอร์จะส่ง POST request พร้อม session cookie ของ alice โดยอัตโนมัติ
เซิร์ฟเวอร์ไม่มีการตรวจสอบ token → email ถูกเปลี่ยนสำเร็จ

---

#### ขั้นตอนการโจมตีแบบ Step-by-step

**ขั้นที่ 1:** alice เข้าสู่ระบบที่ http://localhost:5001
           → เบราว์เซอร์ได้รับ session cookie: session=abc123

**ขั้นที่ 2:** ผู้โจมตีเตรียม evil.html ที่ http://localhost:8080/evil.html
           → form ซ่อน target: POST /account/edit, email=hacked@attacker.com

**ขั้นที่ 3:** alice คลิกลิงก์ phishing → เปิด evil.html ใน browser เดิม

**ขั้นที่ 4:** JavaScript auto-submit ทำงานทันที
           → Browser ส่ง:
- POST http://localhost:5001/account/edit
- Cookie: session=abc123          ← แนบอัตโนมัติ!
- Body: email=hacked@attacker.com

**ขั้นที่ 5:** เซิร์ฟเวอร์ตรวจสอบแค่ session → valid → บันทึก email ใหม่

**ขั้นที่ 6:** alice ไม่รู้ตัว — email ถูกเปลี่ยนเป็น hacked@attacker.com แล้ว
           → ผู้โจมตีสามารถ reset password ผ่าน email ที่ควบคุมได้

#### ผลลัพธ์

**ก่อนโจมตี:**
![ก่อนโจมตี](assets/images/result/csrf/csrf_normal.png)
*รูปที่ 1: หน้า account ของ alice ก่อนถูกโจมตี*

**หลังจากโจมตีสำเร็จ:**
![หลังโจมตี](assets/images/result/csrf/csrf_hacked.png)
*รูปที่ 2: email ถูกเปลี่ยนสำเร็จโดย alice ไม่รู้ตัว*

---

#### เหตุใดการโจมตีจึงสำเร็จ

- เบราว์เซอร์แนบ cookie ไปกับ **ทุก request** ที่ส่งไปยัง domain เดิม
  โดยไม่สนใจว่า request มาจาก origin ใด
- เซิร์ฟเวอร์ตรวจสอบแค่ว่า session ถูกต้อง ไม่ได้ตรวจว่า
  **request มาจากที่ไหน**
- ไม่มี secret token ที่ผู้โจมตีไม่รู้ค่า → สร้าง request ปลอมได้สมบูรณ์

> ⚠️ **หมายเหตุ:** Multistage process (เช่น confirm dialog) ไม่เพียงพอ
> ในการป้องกัน CSRF เพราะผู้โจมตีสามารถส่ง request ทั้ง 2 ขั้นตอน
> ต่อเนื่องกันได้จาก evil.html เดียวกัน

---

#### การทดสอบ Anti-CSRF Defense (Verify ว่า Mitigation ใช้งานได้จริง)

หลังจากใส่ CSRF token แล้ว ทดสอบว่า defense ทำงานถูกต้อง:

| การทดสอบ | ผลที่คาดหวัง |
|---|---|
| ส่ง request โดยไม่มี `csrf_token` | → ถูก reject ด้วย HTTP 403 |
| ส่ง `csrf_token` ที่ค่าผิด (แก้ใน Burp) | → ถูก reject ด้วย HTTP 403 |
| ส่ง token ของ session อื่น (token ของผู้โจมตีเอง) | → ถูก reject (token ต้องผูกกับ session) |
| ส่ง request ปกติพร้อม token ถูกต้อง | → สำเร็จ HTTP 200 |

> ⚠️ **ข้อควรระวัง:** ห้ามใช้ `Referer` header เพียงอย่างเดียวในการตรวจสอบ
> เพราะสามารถถูก spoof ได้ด้วย Flash เวอร์ชันเก่า หรือซ่อนด้วย
> meta refresh tag

---

#### Mitigation Strategies (วิธีแก้ไข)

**วิธีที่ 1 (แนะนำ): Synchronizer Token Pattern**

```python
# app/routes/account.py
import secrets

@account_bp.route('/account/edit', methods=['GET', 'POST'])
def edit():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        # สร้าง token ใหม่และเก็บใน session
        token = secrets.token_hex(16)
        session['csrf_token'] = token
        return render_template('edit_profile.html',
                               csrf_token=token,
                               user=session['user'])

    if request.method == 'POST':
        # ตรวจสอบ token ก่อนทำงานทุกครั้ง
        submitted_token = request.form.get('csrf_token')
        if not submitted_token or submitted_token!= session.get('csrf_token'):
            return "CSRF token invalid!", 403

        new_email = request.form.get('email')
        #... บันทึก email ใหม่
```

เพิ่มใน template:
```html
<form method="POST" action="/account/edit">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <input type="email" name="email" value="{{ user.email }}">
  <button type="submit">Save</button>
</form>
```

**วิธีที่ 2: SameSite Cookie Attribute**

```python
# app/__init__.py
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # หรือ 'Strict'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True       # สำหรับ HTTPS
```

| ค่า SameSite | พฤติกรรม |
|---|---|
| `Strict` | ไม่ส่ง cookie ในทุก cross-site request |
| `Lax` | ส่งเฉพาะ top-level navigation (GET) ไม่ส่งใน POST cross-site |
| `None` | ส่งทุก request (ค่า default เดิม = เสี่ยง) |

**วิธีที่ 3: ใช้ Flask-WTF (Production-ready)**

```python
# ติดตั้ง: poetry add flask-wtf
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
# ป้องกันทุก POST route อัตโนมัติ ไม่ต้องเขียน manual
```

**สรุป: ไม่ควรใช้วิธีเหล่านี้เพียงอย่างเดียว**
- ❌ `Referer` header — spoof ได้
- ❌ Multistage process — ผู้โจมตีส่งได้ทุกขั้นตอน
- ✅ CSRF token + SameSite cookie = ป้องกันได้ครอบคลุม

---
