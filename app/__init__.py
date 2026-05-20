from flask import Flask
from .models import close_db, init_db


def create_app():
    app = Flask(__name__)
    app.secret_key = "shopvuln-secret-key-2026"

    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

    @app.route("/")
    def test_server():
        return "<h1>ShopVuln Server is running!</h1>"

    return app
