from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import get_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # ถ้า login อยู่แล้ว → redirect home
    if 'user' in session:
        return redirect(url_for('products.home'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        db = get_db()

        # SECURE login — parameterized query (auth ไม่ใช่จุด SQLi)
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()

        if user:
            session['user'] = dict(user)   # เก็บ user เป็น dict ใน session
            return redirect(url_for('products.home'))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
