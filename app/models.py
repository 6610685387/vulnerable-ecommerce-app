import sqlite3
import os
from flask import g, current_app

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "shop.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL,
            email    TEXT    NOT NULL,
            role     TEXT    NOT NULL DEFAULT 'user'
        );

        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            price       REAL NOT NULL CHECK (price >= 0),
            description TEXT,
            image_url   TEXT
        );

        CREATE TABLE IF NOT EXISTS orders (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            product_name TEXT    NOT NULL,
            quantity     INTEGER NOT NULL CHECK (quantity > 0),
            unit_price     REAL    NOT NULL DEFAULT 0,
            original_price REAL    NOT NULL DEFAULT 0,
            total        REAL    NOT NULL CHECK (total >= 0),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id         INTEGER  PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER  NOT NULL,
            username   TEXT     NOT NULL,
            product_id INTEGER  NOT NULL,
            content    TEXT     NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)    REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)
    db.commit()
