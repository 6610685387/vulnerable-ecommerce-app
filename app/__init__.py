from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'shopvuln-secret-key-2026'

    @app.route('/')
    def test_server():
        return "<h1>ShopVuln Server is running!</h1>"

    return app