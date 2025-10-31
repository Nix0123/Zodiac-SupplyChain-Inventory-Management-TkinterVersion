# db.py
# ----------------------------------------------------
# Database connection and helper utilities for Zodiac
# ----------------------------------------------------

import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime


# -----------------------
# Database Configuration
# -----------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # Change if you use another MySQL user
    'password': '',        # Add your password if any
    'database': 'zodiac'
}


# -----------------------
# Connection Helper
# -----------------------
def get_connection():
    """Establish a MySQL connection using global config."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[DB] Connection error: {e}")
        return None


# -----------------------
# Hash Utility (SHA256)
# -----------------------
def hash_password(password: str) -> str:
    """Return SHA-256 hash of given password."""
    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------
# AUTHENTICATION METHODS
# -----------------------
def validate_admin(admin_id: str, password: str) -> bool:
    """Validate admin credentials."""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM admin_credentials WHERE admin_id=%s", (admin_id,))
        row = cur.fetchone()
        if row and row[0] == hash_password(password):
            return True
        return False
    except Error as e:
        print(f"[DB] validate_admin error: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def register_user(username: str, email: str, password: str) -> bool:
    """Register a new customer."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        hashed = hash_password(password)
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"[DB] register_user error: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def validate_user(email: str, password: str):
    """Check user login; returns user_id if valid else None."""
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        if user and user['password_hash'] == hash_password(password):
            return user
        return None
    except Error as e:
        print(f"[DB] validate_user error: {e}")
        return None
    finally:
        cur.close()
        conn.close()


def get_suppliers():
    """Fetch list of all suppliers."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = cur.fetchall()
        return suppliers
    except Error as e:
        print(f"[DB] get_suppliers error: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def get_supplier_by_name(name: str):
    """Fetch supplier by name."""
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM suppliers WHERE name=%s", (name,))
        supplier = cur.fetchone()
        return supplier
    except Error as e:
        print(f"[DB] get_supplier_by_name error: {e}")
        return None
    finally:
        cur.close()
        conn.close()


# -----------------------
# PRODUCTS & ORDERS
# -----------------------
def get_all_products():
    """Return all product details joined with supplier name."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.id, p.name, s.name AS supplier, p.price_per_unit, p.stock_count,
                   p.min_stock, p.last_updated, p.monthly_sales
            FROM products p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            ORDER BY p.name
        """)
        products = cur.fetchall()
        return products
    except Error as e:
        print(f"[DB] get_all_products error: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def update_stock(product_id: int, new_stock: int):
    """Update stock count for a product."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE products SET stock_count=%s, last_updated=%s WHERE id=%s
        """, (new_stock, datetime.now(), product_id))
        conn.commit()
        return True
    except Error as e:
        print(f"[DB] update_stock error: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def insert_order(order_type: str, product_id: int, supplier_id: int,
                 customer_id=None, units=0, delivery_date=None, note=None, status='Pending'):
    """Insert a new order record."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (type, product_id, supplier_id, customer_id,
                                units, delivery_date, note, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (order_type, product_id, supplier_id, customer_id, units, delivery_date, note, status))
        conn.commit()
        return True
    except Error as e:
        print(f"[DB] insert_order error: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def get_orders_by_type(order_type: str):
    """Fetch all orders filtered by type."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT o.*, p.name AS product_name, s.name AS supplier_name, u.username AS customer_name
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.id
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            LEFT JOIN users u ON o.customer_id = u.id
            WHERE o.type=%s
            ORDER BY o.created_at DESC
        """, (order_type,))
        return cur.fetchall()
    except Error as e:
        print(f"[DB] get_orders_by_type error: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def mark_order_delivered(order_id: int):
    """Mark order as delivered."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders SET status='Delivered', fulfilled_at=%s WHERE id=%s
        """, (datetime.now(), order_id))
        conn.commit()
        return True
    except Error as e:
        print(f"[DB] mark_order_delivered error: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
