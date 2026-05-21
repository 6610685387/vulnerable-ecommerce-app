import pytest

def test_home_redirects_if_not_logged_in(client):
    r = client.get('/')
    assert r.status_code == 302
    assert 'login' in r.headers['Location']

def test_product_detail_redirects_if_not_logged_in(client):
    r = client.get('/product/1')
    assert r.status_code == 302
    assert 'login' in r.headers['Location']

def test_home_accessible_after_login(client):
    client.post('/login', data={'username': 'alice', 'password': 'alice123'})
    r = client.get('/')
    assert r.status_code == 200
    assert b'ShopVuln' in r.data

def test_all_blueprints_registered(client):
    """ตรวจว่า blueprint ทั้งหมดลงทะเบียนแล้ว โดย test routes"""
    # Note: เรา follow redirects เพราะหน้าหลักโดน guard ไว้
    routes = ['/login', '/logout', '/', '/account/edit']
    for route in routes:
        r = client.get(route, follow_redirects=True)
        assert r.status_code == 200
