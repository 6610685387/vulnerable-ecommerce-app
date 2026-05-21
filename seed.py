from app import create_app
from app.models import get_db

app = create_app()

with app.app_context():
    db = get_db()

    db.executescript("""
        PRAGMA foreign_keys = OFF;
        DELETE FROM reviews;
        DELETE FROM orders;
        DELETE FROM users;
        DELETE FROM products;
        PRAGMA foreign_keys = ON;
    """)

    db.executescript("""
        INSERT INTO users (id, username, password, email, role) VALUES
            (1, 'alice', 'alice123', 'alice@example.com', 'user'),
            (2, 'bob', 'bob456', 'bob@example.com', 'user'),
            (3, 'admin', 'admin999', 'admin@shopvuln.com', 'admin');
    """)

    db.executescript("""
        INSERT INTO products (id, name, price, description, image_url) VALUES
            (1, 'Premium Ultra-Slim Laptop', 25000.00,
             'Intel Core i7 Gen 13, 16GB RAM, 512GB SSD, 14" 2K IPS display. Weighs only 1.2kg, built for professionals on the go.',
             'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&q=80'),

            (2, 'GravaStar Mercury K1 Keyboard', 3500.00,
             'Mechanical keyboard with Kailh Box Red switches, RGB backlight, and compact 75% layout. Built for gamers and developers.',
             'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&q=80'),

            (3, 'Wireless Noise-Cancelling Headphones', 4200.00,
             'Active Noise Cancellation up to 40dB, Bluetooth 5.3, 30-hour battery life. Hi-Fi audio engineered for deep focus.',
             'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80'),

            (4, 'Logitech MX Master 3S Mouse', 2800.00,
             'Ergonomic wireless mouse with 200-8000 DPI, MagSpeed scroll wheel, and multi-device pairing for up to 3 devices.',
             'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&q=80'),

            (5, '27-inch 4K USB-C Monitor', 12500.00,
             '4K 60Hz IPS panel, 99% sRGB, HDR400 support, and USB-C 90W Power Delivery to charge your laptop through a single cable.',
             'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&q=80'),

            (6, 'Samsung 990 Pro SSD 1TB', 4500.00,
             'NVMe PCIe 4.0 with read speeds up to 7,450 MB/s and write speeds up to 6,900 MB/s. 5-year warranty included.',
             'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=600&q=80');
    """)

    db.executescript("""
        INSERT INTO reviews (user_id, username, product_id, content) VALUES
            (1, 'alice', 1, 'Absolutely fantastic machine. The build quality feels premium.'),
            (2, 'bob', 2, 'Best keyboard I have ever used. Worth every baht!');
    """)

    db.commit()
    print("Seed data created successfully! Ready for demo.")