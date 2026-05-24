from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import get_db

shop_bp = Blueprint("shop", __name__)


@shop_bp.route("/buy/<int:product_id>", methods=["GET", "POST"])
def buy(product_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    product = db.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()

    if not product:
        return "Product not found", 404

    if request.method == "POST":
        # SECURE VERSION: Always fetch price from the database — never trust client input
        """
        price = product["price"]
        """

        # INSECURE on Purpose: Price is taken directly from a hidden form field → attacker can modify it via DevTools or Burp Suite (Client-Side Control Bypass)
        price = request.form.get("price", "0")

        quantity = request.form.get("quantity", "1")

        try:
            price_float = float(price)
            quantity_int = int(quantity)
        except (ValueError, TypeError):
            price_float = 0.0
            quantity_int = 1

        total = price_float * quantity_int

        db.execute(
            "INSERT INTO orders (user_id, product_name, quantity, total) VALUES (?, ?, ?, ?)",
            (session["user"]["id"], product["name"], quantity_int, total),
        )
        db.commit()

        return render_template(
            "buy_success.html",
            product=product,
            price=price_float,
            quantity=quantity_int,
            total=total,
            user=session["user"],
        )

    return render_template("buy.html", product=product, user=session["user"])
