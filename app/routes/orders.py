from flask import Blueprint, render_template, session, redirect, url_for
from app.models import get_db

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/order/<int:order_id>")
def order_detail(order_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))
    db = get_db()

    # DISABLE SECURITY: Ensure users can only access their own orders
    """
    order = db.execute(
        "SELECT * FROM orders WHERE id = ? AND user_id = ?",
        (order_id, session["user"]["id"]),
    ).fetchone()
    """

    # INSECURE on Purpose: No user_id check → users can access any order by ID
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
