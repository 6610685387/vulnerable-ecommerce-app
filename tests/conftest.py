import os
import tempfile
import sqlite3
import pytest
from app import create_app
import app.models

@pytest.fixture
def app_instance():
    """สร้าง Flask app และ Test Database แยกจากของจริง"""
    # สร้าง temp file สำหรับ database
    db_fd, db_path = tempfile.mkstemp()
    
    # ⚠️ Monkey-patch เปลี่ยน path ของ DB ใน models.py ให้ชี้ไปที่ไฟล์ชั่วคราว
    original_db_path = app.models.DB_PATH
    app.models.DB_PATH = db_path
    
    app = create_app()
    app.config.update({
        'TESTING': True,
    })

    # เตรียม Schema และข้อมูลจำลองสำหรับ Test
    with app.app_context():
        app.models.init_db()
        db = app.models.get_db()
        db.executescript("""
            INSERT INTO users (username, password, email, role) VALUES
                ('alice', 'alice123', 'alice@example.com', 'user'),
                ('bob', 'bob456', 'bob@example.com', 'user'),
                ('admin', 'admin999', 'admin@shopvuln.com', 'admin');
                
            INSERT INTO products (name, price, description) VALUES
                ('Laptop', 25000.00, 'Test Laptop');
        """)
        db.commit()

    yield app

    # Cleanup: ลบไฟล์ temp database ทิ้งหลังรัน test เสร็จ
    os.close(db_fd)
    os.unlink(db_path)
    # คืนค่าเดิม
    app.models.DB_PATH = original_db_path


@pytest.fixture
def client(app_instance):
    """Fixture สำหรับใช้จำลอง request (GET, POST)"""
    return app_instance.test_client()


@pytest.fixture
def runner(app_instance):
    """Fixture สำหรับทดสอบ CLI commands (ถ้ามี)"""
    return app_instance.test_cli_runner()
