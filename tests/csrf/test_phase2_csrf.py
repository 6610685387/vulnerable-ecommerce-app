import pytest

def login_as_alice(client):
    """Helper: login เป็น alice"""
    client.post('/login', data={'username': 'alice', 'password': 'alice123'})

def test_edit_profile_requires_login(client):
    """GET /account/edit โดยไม่ login → redirect /login"""
    r = client.get('/account/edit')
    assert r.status_code == 302
    assert 'login' in r.headers['Location']

def test_edit_profile_page_loads(client):
    """GET /account/edit หลัง login → 200"""
    login_as_alice(client)
    r = client.get('/account/edit')
    assert r.status_code == 200
    assert b'Edit Profile' in r.data

def test_csrf_vulnerability_no_token_needed(client):
    """
    POST /account/edit โดยไม่ส่ง CSRF token → ต้องสำเร็จ (302)
    นี่คือการพิสูจน์ว่าช่องโหว่มีอยู่จริง
    """
    login_as_alice(client)
    # ไม่มี csrf_token ใน payload เลย
    r = client.post('/account/edit', data={'email': 'csrf_test@attacker.com'})
    assert r.status_code == 302   # ต้อง redirect (แปลว่าสำเร็จโดยไม่มี token)

def test_email_actually_changed(client):
    """หลัง POST โดยไม่มี token → email ใน session ต้องเปลี่ยน"""
    login_as_alice(client)
    client.post('/account/edit', data={'email': 'new@test.com'})
    r = client.get('/account/edit')
    assert b'new@test.com' in r.data

def test_change_password_vulnerability(client):
    """POST /account/password โดยไม่ใช้ token และไม่ถามรหัสผ่านเดิม → ต้องสำเร็จ"""
    login_as_alice(client)
    # พยายามเปลี่ยนรหัสผ่านเป็น 'hacked123'
    r = client.post('/account/password', data={'password': 'hacked123'})
    assert r.status_code == 302
    
    # ตรวจสอบว่ารหัสผ่านถูกเปลี่ยนจริงโดยการลอง login ใหม่
    client.get('/logout')
    r = client.post('/login', data={'username': 'alice', 'password': 'hacked123'})
    assert r.status_code == 302
    # ถ้า redirect ไปที่ home แปลว่า login สำเร็จ
