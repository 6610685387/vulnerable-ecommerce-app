from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import get_db

account_bp = Blueprint('account', __name__)


@account_bp.route('/account/edit', methods=['GET', 'POST'])
def edit_profile():
    # Guard: ต้อง login ก่อน
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        db = get_db()

        # ❌ VULNERABLE: ไม่มี CSRF token check เลย!
        # ใครก็ submit form นี้ได้จากเว็บอื่น ถ้า victim มี session อยู่
        db.execute(
            'UPDATE users SET email = ? WHERE id = ?',
            (new_email, session['user']['id'])
        )
        db.commit()

        # อัปเดต session ให้ตรงกับ DB
        session['user']['email'] = new_email
        # Flask session เป็น immutable dict ต้อง mark_modified
        session.modified = True

        return redirect(url_for('account.edit_profile'))

    # GET: แสดงฟอร์มพร้อม email ปัจจุบัน
    return render_template('edit_profile.html', user=session['user'])
