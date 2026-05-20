from app import create_app
from app.models import get_db

app = create_app()

with app.app_context():
    db = get_db()
    
    db.executescript("""
        DELETE FROM users;
        DELETE FROM products;
        DELETE FROM orders;
        DELETE FROM reviews;
    """)

    db.executescript("""
        INSERT INTO users (id, username, password, email, role) VALUES
            (1, 'alice', 'alice123', 'alice@example.com', 'user'),
            (2, 'bob', 'bob456', 'bob@example.com', 'user'),
            (3, 'admin', 'admin999', 'admin@shopvuln.com', 'admin');
    """)

    db.executescript("""
        INSERT INTO products (id, name, price, description) VALUES
            (1, 'Premium Ultra-Slim Laptop', 25000.00, 'Enterprise-grade performance with advanced security features and a stunning 14" Retina display.'),
            (2, 'GravaStar Mercury K1', 3500.00, 'Premium mechanical keyboard with Kailh switches, designed for high-speed typing and data entry.'),
            (3, 'Wilson RF01 Pro', 9500.00, 'Professional tennis racquet for advanced players seeking ultimate control.'),
            (4, 'INGU% Skincare Routine Set', 1200.00, 'Complete hydration and barrier repair set for daily protection.');
    """)

    db.executescript("""
        INSERT INTO reviews (user_id, username, product_id, content) VALUES
            (1, 'alice', 1, 'Absolutely fantastic machine. The build quality feels premium.');
    """)
    
    db.commit()
    print("Seed data created successfully! Ready for demo.")