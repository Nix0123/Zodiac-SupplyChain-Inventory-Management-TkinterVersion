# dashboard_customer.py
# ----------------------------------------------------
# Customer Dashboard — Zodiac Supply Chain App
# ----------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from db import get_connection


FONT_FAMILY = "Segoe UI"
ACCENT_COLOR = "#9B8AFB"
TEXT_COLOR = "#E6E6E6"


# ----------------------------------------------------
# Function to fetch products from database
# ----------------------------------------------------
def fetch_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price_per_unit FROM products")
    products = cursor.fetchall()
    conn.close()
    return products


# ----------------------------------------------------
# Function to open the customer dashboard
# ----------------------------------------------------
def open_customer_dashboard(customer_id, customer_name):
    window = ttkb.Toplevel(title=f"Customer Dashboard | {customer_name}")
    window.geometry("700x500")
    window.resizable(False, False)
    window.configure(bg="#111")

    ttkb.Label(
        window, text=f"Welcome, {customer_name}",
        font=(FONT_FAMILY, 18, "bold"),
        foreground=ACCENT_COLOR
    ).pack(pady=20)

    frame = ttkb.Frame(window, padding=20)
    frame.pack(pady=10, fill="x")

    # Fetch product data
    products = fetch_products()
    product_names = [p[1] for p in products]

    # Variables
    selected_product = tk.StringVar()
    units_var = tk.IntVar()
    total_cost_var = tk.StringVar(value="0.00")

    ttkb.Label(frame, text="Select Product:", font=(FONT_FAMILY, 12)).grid(row=0, column=0, pady=10, sticky="w")
    product_combo = ttkb.Combobox(frame, textvariable=selected_product, values=product_names, width=40)
    product_combo.grid(row=0, column=1, pady=10, padx=10)

    ttkb.Label(frame, text="No. of Units:", font=(FONT_FAMILY, 12)).grid(row=1, column=0, pady=10, sticky="w")
    units_entry = ttkb.Entry(frame, textvariable=units_var, width=15)
    units_entry.grid(row=1, column=1, pady=10, sticky="w")

    ttkb.Label(frame, text="Total Cost (₹):", font=(FONT_FAMILY, 12)).grid(row=2, column=0, pady=10, sticky="w")
    total_label = ttkb.Label(frame, textvariable=total_cost_var, font=(FONT_FAMILY, 12, "bold"), foreground="#B8B8FF")
    total_label.grid(row=2, column=1, pady=10, sticky="w")

    def update_total_cost(*args):
        try:
            product_name = selected_product.get()
            units = units_var.get()
            if not product_name or units <= 0:
                total_cost_var.set("0.00")
                return

            for p in products:
                if p[1] == product_name:
                    total = float(p[2]) * units
                    total_cost_var.set(f"{total:.2f}")
                    break
        except Exception:
            total_cost_var.set("0.00")

    selected_product.trace_add("write", update_total_cost)
    units_var.trace_add("write", update_total_cost)

    # ----------------------------------------------------
    # ORDER FUNCTION
    # ----------------------------------------------------
    def place_order():
        product_name = selected_product.get()
        units = units_var.get()

        if not product_name or units <= 0:
            messagebox.showwarning("Input Error", "Please select product and enter valid units.")
            return

        # Fetch selected product id and price
        product = next((p for p in products if p[1] == product_name), None)
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return

        product_id, _, price = product
        total_cost = float(price) * units

        conn = get_connection()
        cursor = conn.cursor()

        # Check available stock
        cursor.execute("SELECT stock_count FROM products WHERE id=%s", (product_id,))
        current_stock = cursor.fetchone()[0]

        if current_stock < units:
            messagebox.showerror("Stock Error", "Insufficient stock available.")
            conn.close()
            return

        # Create order (customer_request)
        cursor.execute("""
            INSERT INTO orders (type, product_id, customer_id, units, status)
            VALUES ('customer_request', %s, %s, %s, 'Pending')
        """, (product_id, customer_id, units))

        # Subtract stock
        cursor.execute("""
            UPDATE products SET stock_count = stock_count - %s WHERE id = %s
        """, (units, product_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Order Confirmed", f"Your order for {units} x {product_name} has been placed!\nTotal cost: ₹{total_cost:.2f}")

        # Reset fields
        selected_product.set("")
        units_var.set(0)
        total_cost_var.set("0.00")

    ttkb.Button(
        frame, text="Place Order", bootstyle="primary",
        width=20, command=place_order
    ).grid(row=3, column=0, columnspan=2, pady=30)

    # ----------------------------------------------------
    # LOGOUT BUTTON
    # ----------------------------------------------------
    def logout():
        window.destroy()
        messagebox.showinfo("Logout", "You have been logged out successfully.")

    ttkb.Button(
        window, text="Logout", bootstyle="danger-outline",
        width=12, command=logout
    ).pack(pady=10, anchor="center")
