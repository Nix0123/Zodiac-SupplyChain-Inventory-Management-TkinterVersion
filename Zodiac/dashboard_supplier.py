# dashboard_supplier.py
# ----------------------------------------------------
# Supplier Dashboard — Zodiac Supply Chain App
# ----------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from db import get_connection


FONT_FAMILY = "Segoe UI"
ACCENT_COLOR = "#9B8AFB"
TEXT_COLOR = "#EAEAEA"
BG_COLOR = "#111"


# ----------------------------------------------------
# Function to open Supplier Dashboard
# ----------------------------------------------------
def open_supplier_dashboard(supplier_id):
    window = ttkb.Toplevel(title=f"Supplier Dashboard | {supplier_id}")
    window.state("zoomed")
    window.configure(bg=BG_COLOR)

    ttkb.Label(
        window,
        text=f"Welcome, {supplier_id}",
        font=(FONT_FAMILY, 22, "bold"),
        foreground=ACCENT_COLOR,
        background=BG_COLOR,
    ).pack(pady=24)

    ttkb.Separator(window, orient="horizontal").pack(fill="x", padx=24, pady=12)

    ttkb.Label(
        window,
        text="Pending Restock Requests",
        font=(FONT_FAMILY, 16, "bold"),
        foreground=TEXT_COLOR,
        background=BG_COLOR,
    ).pack(pady=8)

    # ----------------------------------------------------
    # Treeview - Pending Requests
    # ----------------------------------------------------
    cols = ("Stock Name", "Units Required", "Delivery Date", "Note", "Supplier Name", "Status")
    tree = ttk.Treeview(window, columns=cols, show="headings", height=15)
    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=(FONT_FAMILY, 11))
    style.configure("Treeview.Heading", font=(FONT_FAMILY, 12, "bold"))

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=220, anchor="center")

    tree.pack(pady=20)

    # ----------------------------------------------------
    # Load pending restock requests
    # ----------------------------------------------------
    def load_requests():
        for row in tree.get_children():
            tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT stock_name, units_required, delivery_date, note, supplier_name, status
            FROM restock_requests
            WHERE supplier_name=%s AND status='Pending'
        """, (supplier_id,))
        data = cursor.fetchall()
        conn.close()

        for item in data:
            tree.insert("", tk.END, values=item)

    load_requests()

    # ----------------------------------------------------
    # Confirm Restock Function
    # ----------------------------------------------------
    def confirm_restock():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a restock request to confirm.")
            return

        values = tree.item(selected[0], "values")
        stock_name = values[0]
        units_required = int(values[1])

        conn = get_connection()
        cursor = conn.cursor()

        # Update stock count in product table
        cursor.execute("UPDATE products SET current_stock_count = current_stock_count + %s WHERE name=%s",
                       (units_required, stock_name))

        # Update request status
        cursor.execute("""
            UPDATE restock_requests
            SET status='Delivered'
            WHERE stock_name=%s AND supplier_name=%s AND status='Pending'
        """, (stock_name, supplier_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Restock for '{stock_name}' confirmed and updated.")
        load_requests()

    ttkb.Button(
        window, text="Confirm Restock", bootstyle="success",
        width=20, command=confirm_restock
    ).pack(pady=10)

    # ----------------------------------------------------
    # Logout
    # ----------------------------------------------------
    def logout():
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            window.destroy()

    ttkb.Button(
        window, text="Logout", bootstyle="danger-outline",
        width=12, command=logout
    ).pack(pady=10)
