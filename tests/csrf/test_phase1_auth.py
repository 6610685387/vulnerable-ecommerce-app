import pytest

def test_login_page_loads(client):
    """GET /login ต้องได้ 200"""
    r = client.get('/login')
    assert r.status_code == 200
    assert b'Sign In' in r.data

def test_login_success_redirects(client):
    """POST /login ด้วย credential ถูก → redirect (302)"""
    r = client.post('/login', data={'username': 'alice', 'password': 'alice123'})
    assert r.status_code == 302

def test_login_fail_shows_error(client):
    """POST /login ด้วย credential ผิด → 200 + error message"""
    r = client.post('/login', data={'username': 'alice', 'password': 'wrong'})
    assert r.status_code == 200
    assert b'Invalid' in r.data

def test_logout_clears_session(client):
    """GET /logout → redirect /login"""
    # login ก่อน
    client.post('/login', data={'username': 'alice', 'password': 'alice123'})
    r = client.get('/logout')
    assert r.status_code == 302
    assert '/login' in r.headers['Location']
