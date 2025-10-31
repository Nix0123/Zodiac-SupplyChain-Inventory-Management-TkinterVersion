# dashboard_admin.py
# ----------------------------------------------------
# Administrator Dashboard — Zodiac Supply Chain App
# ----------------------------------------------------

import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from db import get_connection
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


FONT_FAMILY = "Segoe UI"
ACCENT_COLOR = "#9B8AFB"
TEXT_COLOR = "#E6E6E6"


# ----------------------------------------------------
# Fetch product data
# ----------------------------------------------------
def fetch_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, price_per_unit, stock_count, last_updated, monthly_sales
        FROM products
    """)
    products = cursor.fetchall()
    conn.close()
    return products


# ----------------------------------------------------
# Fetch order history
# ----------------------------------------------------
def fetch_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, p.name, o.units, o.status, o.created_at
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.type = 'restock_request'
        ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()
    conn.close()
    return orders


# ----------------------------------------------------
# Demand Prediction using Linear Regression
# ----------------------------------------------------
def predict_demand():
    conn = get_connection()
    df = pd.read_sql("SELECT name, price_per_unit, monthly_sales FROM products", conn)
    conn.close()

    if df.empty:
        return []

    X = df[["price_per_unit"]].values
    y = df["monthly_sales"].values
    model = LinearRegression().fit(X, y)

    df["predicted_sales"] = model.predict(X)
    df["trend"] = np.where(df["predicted_sales"] > df["monthly_sales"], "Increasing", "Decreasing")

    return df


# ----------------------------------------------------
# Restock request function
# ----------------------------------------------------
def restock_request(product_id, supplier_id, units, delivery_date, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (type, product_id, supplier_id, units, delivery_date, note, status)
        VALUES ('restock_request', %s, %s, %s, %s, %s, 'Pending')
    """, (product_id, supplier_id, units, delivery_date, note))
    conn.commit()
    conn.close()


# ----------------------------------------------------
# Open the Admin Dashboard
# ----------------------------------------------------
def open_admin_dashboard(admin_id):
    window = ttkb.Toplevel(title="Administrator Dashboard | Zodiac")
    window.geometry("950x600")
    window.resizable(False, False)
    window.configure(bg="#111")

    notebook = ttkb.Notebook(window, bootstyle="dark")
    notebook.pack(fill="both", expand=True, padx=20, pady=20)

    # Tabs
    tab_dashboard = ttkb.Frame(notebook, padding=20)
    tab_history = ttkb.Frame(notebook, padding=20)
    tab_prediction = ttkb.Frame(notebook, padding=20)

    notebook.add(tab_dashboard, text="Dashboard")
    notebook.add(tab_history, text="Order History")
    notebook.add(tab_prediction, text="Prediction")

    # ----------------------------------------------------
    # TAB 1 — DASHBOARD (Product table + Restock)
    # ----------------------------------------------------
    ttkb.Label(
        tab_dashboard, text="Product Inventory",
        font=(FONT_FAMILY, 16, "bold"), foreground=ACCENT_COLOR
    ).pack(pady=10)

    columns = ("Name", "Price", "Stock", "Last Updated", "Monthly Sales", "Status", "Action")
    tree = ttk.Treeview(tab_dashboard, columns=columns, show="headings", height=12)

    for col in columns[:-1]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    tree.heading("Action", text="Restock")
    tree.column("Action", width=100, anchor="center")

    products = fetch_products()
    for p in products:
        status = "🟢 OK" if p[3] > 10 else "🔴 Low"
        tree.insert("", "end", values=(p[1], p[2], p[3], p[4], p[5], status, "Restock"))

    tree.pack(fill="both", expand=True, pady=10)

    def on_tree_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        values = tree.item(item, "values")
        product_name = values[0]

        # Fetch product + supplier info
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, supplier_id FROM products WHERE name=%s
        """, (product_name,))
        prod = cursor.fetchone()
        conn.close()

        if not prod:
            messagebox.showerror("Error", "Product not found.")
            return

        product_id, supplier_id = prod

        # Open restock form modal
        restock_window = ttkb.Toplevel(window)
        restock_window.title("Restock Request")
        restock_window.geometry("400x400")
        restock_window.configure(bg="#111")

        ttkb.Label(restock_window, text="Restock Request", font=(FONT_FAMILY, 14, "bold"), foreground=ACCENT_COLOR).pack(pady=15)
        ttkb.Label(restock_window, text=f"Product: {product_name}", font=(FONT_FAMILY, 11)).pack(pady=5)

        ttkb.Label(restock_window, text="Units Required:", font=(FONT_FAMILY, 11)).pack(pady=5)
        units_entry = ttkb.Entry(restock_window)
        units_entry.pack(pady=5)

        ttkb.Label(restock_window, text="Delivery Date (YYYY-MM-DD):", font=(FONT_FAMILY, 11)).pack(pady=5)
        date_entry = ttkb.Entry(restock_window)
        date_entry.pack(pady=5)

        ttkb.Label(restock_window, text="Note:", font=(FONT_FAMILY, 11)).pack(pady=5)
        note_entry = ttkb.Entry(restock_window)
        note_entry.pack(pady=5)

        def submit_restock():
            try:
                units = int(units_entry.get())
                delivery_date = date_entry.get()
                note = note_entry.get()
                if units <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid number of units.")
                return

            restock_request(product_id, supplier_id, units, delivery_date, note)
            messagebox.showinfo("Success", "Restock request sent to supplier.")
            restock_window.destroy()

        ttkb.Button(restock_window, text="Submit", bootstyle="success", command=submit_restock).pack(pady=20)

    tree.bind("<Double-1>", on_tree_click)

    # ----------------------------------------------------
    # TAB 2 — ORDER HISTORY
    # ----------------------------------------------------
    ttkb.Label(
        tab_history, text="Restock Order History",
        font=(FONT_FAMILY, 16, "bold"), foreground=ACCENT_COLOR
    ).pack(pady=10)

    columns_hist = ("Order ID", "Product", "Units", "Status", "Date")
    tree_hist = ttk.Treeview(tab_history, columns=columns_hist, show="headings", height=14)

    for col in columns_hist:
        tree_hist.heading(col, text=col)
        tree_hist.column(col, anchor="center", width=140)

    tree_hist.pack(fill="both", expand=True, pady=10)

    for o in fetch_orders():
        status_color = "Delivered ✅" if o[3] == "Delivered" else "Pending ⏳"
        tree_hist.insert("", "end", values=(o[0], o[1], o[2], status_color, o[4]))

    # ----------------------------------------------------
    # TAB 3 — DEMAND PREDICTION
    # ----------------------------------------------------
    ttkb.Label(
        tab_prediction, text="Demand Prediction (AI Model)",
        font=(FONT_FAMILY, 16, "bold"), foreground=ACCENT_COLOR
    ).pack(pady=10)

    result_df = predict_demand()
    if len(result_df) == 0:
        ttkb.Label(tab_prediction, text="No products found for prediction.", font=(FONT_FAMILY, 12)).pack(pady=20)
    else:
        cols_pred = ("Product", "Price", "Current Sales", "Predicted", "Trend")
        tree_pred = ttk.Treeview(tab_prediction, columns=cols_pred, show="headings", height=10)

        for c in cols_pred:
            tree_pred.heading(c, text=c)
            tree_pred.column(c, anchor="center", width=150)

        for _, r in result_df.iterrows():
            trend_color = "🟢 Increasing" if r["trend"] == "Increasing" else "🔴 Decreasing"
            tree_pred.insert("", "end", values=(
                r["name"], f"{r['price_per_unit']:.2f}", r["monthly_sales"], f"{r['predicted_sales']:.2f}", trend_color
            ))

        tree_pred.pack(fill="both", expand=True, pady=10)

        ttkb.Label(
            tab_prediction,
            text=(
                "This prediction uses a simple linear regression model trained on current pricing "
                "and monthly sales data to estimate potential future demand. "
                "A product with an 'Increasing' trend indicates positive demand elasticity — "
                "higher prices are associated with higher sales or stable demand. Conversely, "
                "a 'Decreasing' trend suggests price sensitivity and potential oversupply. "
                "These insights help administrators plan restocks and pricing strategies efficiently."
            ),
            wraplength=800, justify="left", font=(FONT_FAMILY, 11), foreground="#BBB"
        ).pack(pady=20)

    # ----------------------------------------------------
    # LOGOUT
    # ----------------------------------------------------
    def logout():
        window.destroy()
        messagebox.showinfo("Logout", "Admin logged out successfully.")

    ttkb.Button(
        window, text="Logout", bootstyle="danger-outline",
        width=12, command=logout
    ).pack(pady=10, anchor="center")
