from flask import Blueprint, render_template, session, redirect, url_for
from app.models import get_db

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/order/<int:order_id>")
def order_detail(order_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))
    db = get_db()

    # SECURE VERSION: Verify ownership before returning order data
    """
    order = db.execute(
        "SELECT * FROM orders WHERE id = ? AND user_id = ?",
        (order_id, session["user"]["id"]),
    ).fetchone()
    if not order:
        return "Access denied", 403
    """

    # INSECURE on Purpose: No user_id check → any logged-in user can view any order by changing the ID in the URL (IDOR)
    order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()

    if not order:
        return render_template("order_detail.html", order=None, user=session["user"])

    return render_template("order_detail.html", order=order, user=session["user"])


@orders_bp.route("/my-orders")
def my_orders():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    db = get_db()
    orders = db.execute(
        "SELECT * FROM orders WHERE user_id = ?", (session["user"]["id"],)
    ).fetchall()
    return render_template("my_orders.html", orders=orders, user=session["user"])


@orders_bp.route("/admin/orders")
def admin_orders():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    if session["user"].get("role") != "admin":
        return "Access denied — Admins only", 403

    db = get_db()
    # JOIN เพื่อดึง username ของแต่ละ order ด้วย
    orders = db.execute("""
        SELECT o.*, u.username
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.id DESC
    """).fetchall()

    return render_template("admin_orders.html", orders=orders, user=session["user"])