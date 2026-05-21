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
        login_id = request.form.get('login_id', '').strip()
        password = request.form.get('password', '').strip()
        db = get_db()

        # SECURE login — parameterized query
        user = db.execute(
            'SELECT * FROM users WHERE (username = ? OR email = ?) AND password = ?',
            (login_id, login_id, password)
        ).fetchone()

        if user:
            session['user'] = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
            return redirect(url_for('products.home'))
        else:
            error = 'Invalid username/email or password'

    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
