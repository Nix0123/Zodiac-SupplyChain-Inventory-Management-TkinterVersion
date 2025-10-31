# auth_customer.py
# ----------------------------------------------------
# Customer Authentication (Login & Registration)
# ----------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from db import get_connection
from dashboard_customer import open_customer_dashboard

FONT_FAMILY = "Segoe UI"
ACCENT_COLOR = "#9B8AFB"
TEXT_COLOR = "#E6E6E6"


# ----------------------------------------------------
# Customer Auth Window
# ----------------------------------------------------
def open_customer_page():
    window = ttkb.Toplevel(title="Customer Login | Zodiac")
    window.geometry("600x480")
    window.resizable(False, False)
    window.configure(bg="#111")

    notebook = ttkb.Notebook(window, bootstyle="dark")
    notebook.pack(fill="both", expand=True, padx=20, pady=20)

    login_frame = ttkb.Frame(notebook, padding=20)
    register_frame = ttkb.Frame(notebook, padding=20)

    notebook.add(login_frame, text="Login")
    notebook.add(register_frame, text="Register")

    # ----------------------------------------------------
    # LOGIN TAB
    # ----------------------------------------------------
    ttkb.Label(
        login_frame, text="Customer Login",
        font=(FONT_FAMILY, 18, "bold"),
        foreground=ACCENT_COLOR
    ).pack(pady=15)

    ttkb.Label(login_frame, text="Email:", font=(FONT_FAMILY, 12)).pack(pady=(20, 4))
    email_login = ttkb.Entry(login_frame, width=45)
    email_login.pack(pady=4)

    ttkb.Label(login_frame, text="Password:", font=(FONT_FAMILY, 12)).pack(pady=(12, 4))
    password_login = ttkb.Entry(login_frame, show="*", width=45)
    password_login.pack(pady=4)

    # -----------------------
    # LOGIN HANDLER FUNCTION
    # -----------------------
    def handle_login():
        email = email_login.get().strip()
        password = password_login.get().strip()

        if not email or not password:
            messagebox.showwarning("Input Error", "Please enter both email and password!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            window.destroy()
            open_customer_dashboard(user[0], user[1])
        else:
            messagebox.showerror("Error", "Invalid email or password!")

    # -----------------------
    # LOGIN BUTTON (FIXED)
    # -----------------------
    button_frame = ttkb.Frame(login_frame)
    button_frame.pack(pady=30)

    ttkb.Button(
        button_frame, text="Login",
        bootstyle="primary",
        width=20,
        command=handle_login
    ).pack(pady=5)

    ttkb.Button(
        button_frame, text="Cancel",
        bootstyle="danger-outline",
        width=14,
        command=window.destroy
    ).pack(pady=5)

    # ----------------------------------------------------
    # REGISTER TAB
    # ----------------------------------------------------
    ttkb.Label(
        register_frame, text="New Customer Registration",
        font=(FONT_FAMILY, 18, "bold"),
        foreground=ACCENT_COLOR
    ).pack(pady=15)

    ttkb.Label(register_frame, text="Full Name:", font=(FONT_FAMILY, 12)).pack(pady=(16, 4))
    name_reg = ttkb.Entry(register_frame, width=45)
    name_reg.pack(pady=4)

    ttkb.Label(register_frame, text="Email:", font=(FONT_FAMILY, 12)).pack(pady=(12, 4))
    email_reg = ttkb.Entry(register_frame, width=45)
    email_reg.pack(pady=4)

    ttkb.Label(register_frame, text="Password:", font=(FONT_FAMILY, 12)).pack(pady=(12, 4))
    password_reg = ttkb.Entry(register_frame, show="*", width=45)
    password_reg.pack(pady=4)

    ttkb.Label(register_frame, text="Phone Number:", font=(FONT_FAMILY, 12)).pack(pady=(12, 4))
    phone_reg = ttkb.Entry(register_frame, width=45)
    phone_reg.pack(pady=4)

    def handle_register():
        name = name_reg.get().strip()
        email = email_reg.get().strip()
        password = password_reg.get().strip()
        phone = phone_reg.get().strip()

        if not all([name, email, password, phone]):
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Email already registered!")
            conn.close()
            return

        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'customer')",
            (name, email, password)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Registration successful! You can now login.")
        name_reg.delete(0, tk.END)
        email_reg.delete(0, tk.END)
        password_reg.delete(0, tk.END)
        phone_reg.delete(0, tk.END)

    ttkb.Button(
        register_frame, text="Register",
        bootstyle="success",
        width=20,
        command=handle_register
    ).pack(pady=25)
