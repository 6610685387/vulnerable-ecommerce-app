from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import get_db

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def home():
    db = get_db()
    products = db.execute('SELECT * FROM products').fetchall()
    return render_template('home.html', products=products)

@products_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    reviews = db.execute('SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC', (product_id,)).fetchall()
    
    if not product:
        return "Product not found", 404
        
    return render_template('product_detail.html', product=product, reviews=reviews)

@products_bp.route('/product/<int:product_id>/review', methods=['POST'])
def add_review(product_id):
    if 'user' not in session:
        return redirect(url_for('auth.login')) # ให้ P3 จัดการเรื่อง Auth
        
    content = request.form.get('content', '')
    db = get_db()
    
    # VULNERABILITY: Stored XSS
    db.execute(
        'INSERT INTO reviews (user_id, username, product_id, content) VALUES (?, ?, ?, ?)',
        (session['user']['id'], session['user']['username'], product_id, content)
    )
    db.commit()
    
    return redirect(url_for('products.product_detail', product_id=product_id))