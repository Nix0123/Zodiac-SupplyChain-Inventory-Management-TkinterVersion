# auth_admin.py
# ----------------------------------------------------
# Admin Authentication - Zodiac Supply Chain App
# ----------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from db import get_connection
from dashboard_admin import open_admin_dashboard


FONT_FAMILY = "Segoe UI"
ACCENT_COLOR = "#9B8AFB"
TEXT_COLOR = "#E6E6E6"


# ----------------------------------------------------
# Function to open Admin Login Window
# ----------------------------------------------------
def open_admin_page():
    window = ttkb.Toplevel(title="Administrator Login | Zodiac")
    window.geometry("500x350")
    window.resizable(False, False)
    window.configure(bg="#111")

    ttkb.Label(
        window, text="Administrator Login",
        font=(FONT_FAMILY, 18, "bold"),
        foreground=ACCENT_COLOR
    ).pack(pady=20)

    ttkb.Label(window, text="Admin ID:", font=(FONT_FAMILY, 12)).pack(pady=(16, 4))
    admin_id_entry = ttkb.Entry(window, width=40)
    admin_id_entry.pack(pady=4)

    ttkb.Label(window, text="Password:", font=(FONT_FAMILY, 12)).pack(pady=(12, 4))
    password_entry = ttkb.Entry(window, show="*", width=40)
    password_entry.pack(pady=4)

    # ----------------------------------------------------
    # Login function
    # ----------------------------------------------------
    def handle_admin_login():
        admin_id = admin_id_entry.get().strip()
        password = password_entry.get().strip()

        if not admin_id or not password:
            messagebox.showwarning("Input Error", "Please enter Admin ID and Password.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM admin_credentials WHERE admin_id=%s", (admin_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("Error", "Invalid Admin ID.")
            return

        import hashlib
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()

        if hashed_pass == row[0]:
            messagebox.showinfo("Success", "Admin authenticated successfully.")
            window.destroy()
            open_admin_dashboard(admin_id)
        else:
            messagebox.showerror("Error", "Incorrect password.")

    ttkb.Button(
        window, text="Login", bootstyle="primary",
        width=18, command=handle_admin_login
    ).pack(pady=30)

    # ----------------------------------------------------
    # Exit Button
    # ----------------------------------------------------
    def exit_admin():
        window.destroy()

    ttkb.Button(
        window, text="Cancel", bootstyle="danger-outline",
        width=12, command=exit_admin
    ).pack(pady=5)
