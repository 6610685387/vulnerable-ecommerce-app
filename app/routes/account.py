from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import get_db

account_bp = Blueprint('account', __name__)


@account_bp.route('/account', methods=['GET'])
def profile():
    # Guard: ต้อง login ก่อน
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('account.html', user=session['user'])


@account_bp.route('/account/edit', methods=['GET', 'POST'])
def edit_profile():
    # Guard: ต้อง login ก่อน
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        db = get_db()

        # ❌ VULNERABLE: ไม่มี CSRF token check เลย!
        db.execute(
            'UPDATE users SET email = ? WHERE id = ?',
            (new_email, session['user']['id'])
        )
        db.commit()

        # อัปเดต session ให้ตรงกับ DB
        session['user']['email'] = new_email
        session.modified = True

        return redirect(url_for('account.profile'))

    return render_template('edit_profile.html', user=session['user'])


@account_bp.route('/account/password', methods=['GET', 'POST'])
def change_password():
    # Guard: ต้อง login ก่อน
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form.get('password', '').strip()
        if new_password:
            db = get_db()
            # ❌ VULNERABLE: ไม่มี CSRF token check และไม่ถาม Current Password
            db.execute(
                'UPDATE users SET password = ? WHERE id = ?',
                (new_password, session['user']['id'])
            )
            db.commit()
        return redirect(url_for('account.profile'))

    return render_template('change_password.html', user=session['user'])
