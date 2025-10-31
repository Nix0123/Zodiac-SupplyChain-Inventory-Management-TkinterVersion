# auth_supplier.py
# ----------------------------------------------------
# Supplier Authentication — Zodiac Supply Chain App
# ----------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from db import get_connection
from dashboard_supplier import open_supplier_dashboard


FONT_FAMILY = "Segoe UI"
ACCENT_COLOR = "#9B8AFB"


# ----------------------------------------------------
# Function to open Supplier Login Window
# ----------------------------------------------------
def open_supplier_page():
    window = ttkb.Toplevel(title="Supplier Login | Zodiac")
    window.geometry("500x350")
    window.resizable(False, False)
    window.configure(bg="#111")

    ttkb.Label(
        window, text="Supplier Login",
        font=(FONT_FAMILY, 18, "bold"),
        foreground=ACCENT_COLOR
    ).pack(pady=20)

    ttkb.Label(window, text="Supplier ID:", font=(FONT_FAMILY, 12)).pack(pady=(16, 4))
    supplier_id_entry = ttkb.Entry(window, width=40)
    supplier_id_entry.pack(pady=4)

    ttkb.Label(window, text="Password:", font=(FONT_FAMILY, 12)).pack(pady=(12, 4))
    password_entry = ttkb.Entry(window, show="*", width=40)
    password_entry.pack(pady=4)

    # ----------------------------------------------------
    # Login Handler (Using Plain Password Column)
    # ----------------------------------------------------
    def handle_supplier_login():
        supplier_id = supplier_id_entry.get().strip()
        password = password_entry.get().strip()

        if not supplier_id or not password:
            messagebox.showwarning("Input Error", "Please enter Supplier ID and Password.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM supplier_credentials WHERE supplier_id = %s", (supplier_id,))
            row = cursor.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error while connecting to database:\n{e}")
            return

        if not row:
            messagebox.showerror("Error", "Invalid Supplier ID.")
            return

        stored_password = row[0]

        if password == stored_password:
            messagebox.showinfo("Success", "Supplier authenticated successfully.")
            window.destroy()
            open_supplier_dashboard(supplier_id)
        else:
            messagebox.showerror("Error", "Incorrect password.")

    ttkb.Button(
        window, text="Login", bootstyle="primary",
        width=18, command=handle_supplier_login
    ).pack(pady=30)

    # ----------------------------------------------------
    # Cancel Button
    # ----------------------------------------------------
    def exit_supplier():
        window.destroy()

    ttkb.Button(
        window, text="Cancel", bootstyle="danger-outline",
        width=12, command=exit_supplier
    ).pack(pady=5)
