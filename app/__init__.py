import os
from flask import Flask
from .models import close_db, init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "shopvuln-secret-key-2026")
    app.config['SESSION_COOKIE_HTTPONLY'] = False

    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

    from .routes.products import products_bp
    app.register_blueprint(products_bp)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.account import account_bp
    app.register_blueprint(account_bp)

    from .routes.orders import orders_bp
    app.register_blueprint(orders_bp)

    from .routes.shop import shop_bp
    app.register_blueprint(shop_bp)

    return app
