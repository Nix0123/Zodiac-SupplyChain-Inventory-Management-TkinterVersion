# main.py
# ---------------------------------------------
# Zodiac Supply Chain Management System (Tkinter)
# Home / Entry Screen
# ---------------------------------------------

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from itertools import cycle
import threading
import time
import os

# Import role authentication modules directly
from auth_admin import open_admin_page
from auth_supplier import open_supplier_page
from auth_customer import open_customer_page

# --------------------------
# Global Style Configuration
# --------------------------
APP_NAME = "Zodiac"
ACCENT_COLOR = "#9B8AFB"  # Muted violet
TEXT_COLOR = "#E6E6E6"    # Cool white
FONT_FAMILY = "Segoe UI"  # Sans-serif style
BG_IMAGE_PATH = "assets/bg.jpg"
TRADEMARK = "© 2025 Taranjeet Singh | All Rights Reserved"


# --------------------------
# Main Application Window
# --------------------------
class ZodiacApp(ttkb.Window):
    def __init__(self):
        super().__init__(title=APP_NAME, themename="darkly")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.configure(bg="#111")

        self.setup_background()
        self.create_topbar()
        self.create_center_content()
        self.create_footer()

    # --------------------------
    # Background setup
    # --------------------------
    def setup_background(self):
        try:
            image = Image.open(BG_IMAGE_PATH)
            image = image.resize((1280, 720), Image.Resampling.LANCZOS)
            blurred = image.filter(ImageFilter.GaussianBlur(10))
            self.bg_img = ImageTk.PhotoImage(blurred)

            bg_label = tk.Label(self, image=self.bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"[Zodiac] Background load error: {e}")

    # --------------------------
    # Top bar with logo and menu
    # --------------------------
    def create_topbar(self):
        self.topbar = tk.Frame(self, bg="#1A1A1A", height=60)
        self.topbar.pack(fill=X, side=TOP)

        # App name (animated)
        self.app_name_label = tk.Label(
            self.topbar,
            text=APP_NAME,
            fg=ACCENT_COLOR,
            bg="#1A1A1A",
            font=(FONT_FAMILY, 20, "bold")
        )
        self.app_name_label.pack(side=LEFT, padx=20)

        self.animate_app_name()

        # Right-side buttons (About Us, Contact Us)
        about_btn = ttkb.Button(
            self.topbar, text="About Us", bootstyle="secondary-outline",
            command=self.show_about
        )
        about_btn.pack(side=RIGHT, padx=10, pady=10)

        contact_btn = ttkb.Button(
            self.topbar, text="Contact Us", bootstyle="secondary-outline",
            command=self.show_contact
        )
        contact_btn.pack(side=RIGHT, padx=10, pady=10)

    # --------------------------
    # About and Contact dialogs
    # --------------------------
    def show_about(self):
        about_text = (
            "Zodiac is a modern supply-chain management system designed to simplify and automate "
            "the relationship between administrators, suppliers, and customers. Built with a "
            "focus on intelligent stock handling and predictive analytics, it ensures optimal "
            "inventory control through real-time data monitoring and automated forecasting.\n\n"
            "Features include role-based dashboards, customer order tracking, supplier restock "
            "fulfillment, administrative oversight, and machine learning-driven demand prediction."
        )

        self.show_popup("About Us", about_text)

    def show_contact(self):
        contact_text = (
            "For assistance or business inquiries, please reach out:\n\n"
            "📞  +91 9878770515\n"
            "👤  Taranjeet Singh\n"
            "✉️  support@zodiac-app.com\n"
            "🌐  www.zodiac-scm.com\n\n"
            "Our team is available 24/7 for customer and technical support."
        )

        self.show_popup("Contact Us", contact_text)

    def show_popup(self, title, message):
        popup = ttkb.Toplevel(title=title)
        popup.geometry("600x400")
        popup.resizable(False, False)

        frame = ttkb.Frame(popup, padding=20)
        frame.pack(fill=BOTH, expand=YES)

        text = tk.Text(
            frame, wrap=WORD, font=(FONT_FAMILY, 11),
            fg=TEXT_COLOR, bg="#222", relief=FLAT, insertbackground=TEXT_COLOR
        )
        text.insert("1.0", message)
        text.config(state="disabled")
        text.pack(fill=BOTH, expand=YES)

        ttkb.Button(frame, text="Close", bootstyle="primary-outline", command=popup.destroy).pack(pady=10)

    # --------------------------
    # Center content (Navigation)
    # --------------------------
    def create_center_content(self):
        center_frame = ttkb.Frame(self, padding=20)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Left bouncing icon
        self.icon_img = Image.open("assets/icon.png") if self.icon_exists() else None
        if self.icon_img:
            self.icon_img = self.icon_img.resize((120, 120))
            self.tk_icon = ImageTk.PhotoImage(self.icon_img)
            self.icon_label = tk.Label(center_frame, image=self.tk_icon, bg="#111")
            self.icon_label.grid(row=0, column=0, padx=30)
            threading.Thread(target=self.animate_icon_bounce, daemon=True).start()

        # Navigation panel
        nav_frame = ttkb.Frame(center_frame, padding=16)
        nav_frame.grid(row=0, column=1)

        ttkb.Label(
            nav_frame, text="Select Role", font=(FONT_FAMILY, 16, "bold"),
            foreground=ACCENT_COLOR
        ).pack(pady=(0, 16))

        # Role buttons
        ttkb.Button(
            nav_frame, text="Customer", width=18, bootstyle="primary",
            command=self.open_customer
        ).pack(pady=8)

        ttkb.Button(
            nav_frame, text="Supplier", width=18, bootstyle="primary",
            command=self.open_supplier
        ).pack(pady=8)

        ttkb.Button(
            nav_frame, text="Administrator", width=18, bootstyle="primary",
            command=self.open_admin
        ).pack(pady=8)

    def icon_exists(self):
        return os.path.exists("assets/icon.png")

    def animate_icon_bounce(self):
        """Continuous bounce animation for the icon."""
        while True:
            for dy in cycle([0, -10, -20, -10, 0]):
                self.icon_label.place_configure(rely=0.5, y=dy)
                time.sleep(0.08)

    # --------------------------
    # Footer trademark
    # --------------------------
    def create_footer(self):
        footer = tk.Label(
            self,
            text=TRADEMARK,
            font=(FONT_FAMILY, 10),
            fg="#888",
            bg="#111"
        )
        footer.pack(side=BOTTOM, pady=8)

    # --------------------------
    # Animation for App Name
    # --------------------------
    def animate_app_name(self):
        def animate():
            colors = ["#9B8AFB", "#B39CFB", "#8E79F5", "#A595FF"]
            i = 0
            while True:
                self.app_name_label.config(fg=colors[i % len(colors)])
                i += 1
                time.sleep(0.8)
        threading.Thread(target=animate, daemon=True).start()

    # --------------------------
    # Navigation actions
    # --------------------------
    def open_customer(self):
        
        open_customer_page()

    def open_supplier(self):
        
        open_supplier_page()

    def open_admin(self):

        open_admin_page()


# --------------------------
# Run Application
# --------------------------
if __name__ == "__main__":
    app = ZodiacApp()
    app.mainloop()
