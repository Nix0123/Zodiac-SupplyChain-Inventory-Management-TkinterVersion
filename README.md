# Zodiac-SupplyChain-Inventory-Management-TkinterVersion
Zodiac is a Python-based desktop application built using Tkinter and ttkbootstrap that streamlines supplier, customer, and admin interactions in a supply chain ecosystem. It integrates MySQL for backend data management and provides real-time inventory tracking, order handling, and supplier performance visualization. 

🌙 Zodiac – Intelligent Supply Chain Management System

📖 Project Summary

Zodiac is an intelligent and user-friendly Supply Chain Management System developed using Python (Tkinter) for the GUI and MySQL as the database backend.
The application streamlines operations between Admins, Suppliers, and Customers, enabling real-time tracking of product stock, order flow, and supplier performance.

The system is built with modular architecture — separating authentication, dashboards, and database utilities into different Python files for easy maintenance and scalability.
It also includes data security measures like SHA-256 password hashing and structured SQL interaction to prevent data inconsistencies.

Zodiac automates key tasks such as:

Managing product inventories and restock levels.

Tracking customer orders and supplier deliveries.

Handling authentication and registration for multiple user roles.

Providing visual insights into supply operations.

The interface is designed using ttkbootstrap, giving it a sleek, modern look while retaining the simplicity of Tkinter.

🧩 Key Features

🔒 Role-Based Authentication
Secure login and registration for Admins, Suppliers, and Customers with password hashing.

📦 Product & Stock Management
Admins and suppliers can add, update, and monitor stock levels in real time.

🧾 Order Handling System
Customers can place orders, suppliers can mark them fulfilled, and admins can track all transactions.

📊 Dashboard Visualization
Clean dashboards for each user type, showing stats like product performance, pending orders, and recent activity.

🗃️ MySQL Integrated Backend
Robust and reliable database connection with proper exception handling and modular design.

🎨 Modern UI Design
Built using ttkbootstrap with dark mode themes, accent colors, and structured layouts.

🧱 Project Structure
<img width="912" height="449" alt="image" src="https://github.com/user-attachments/assets/68f8179c-bddd-4f1f-bccf-6810bf90b950" />


⚙️ Setup Instructions

1️⃣ Prerequisites

      Before running the project, ensure the following are installed:

      🐍 Python 3.10+

      🧱 MySQL Server 8.0+

      📦 Python packages:

             pip install mysql-connector-python ttkbootstrap pillow

2️⃣ Database Setup

➤ Create the Database
CREATE DATABASE zodiac;
USE zodiac;

➤ Create Tables

You’ll need the following main tables:

admin_credentials

supplier_credentials

users

suppliers

products

orders

You can run the full table creation script (provided separately) in your MySQL Workbench or terminal.

➤ Add Sample Entries
INSERT INTO admin_credentials (admin_id, password) VALUES ('admin', 'admin123');
INSERT INTO supplier_credentials (supplier_id, name, email, password)
VALUES ('sup001', 'Apex Supplies', 'apex@zodiac.com', 'supplier123');

3️⃣ Configure Database Connection

In db.py, verify that the credentials match your MySQL setup:

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',        # Add password if you have one
    'database': 'zodiac'
}

4️⃣ Run the Application

Navigate to your project directory and execute:

python main.py


The main window will launch, showing login options for Admin, Supplier, and Customer.

🖥️ Usage Overview

Admin Panel:
Manage suppliers, view all products, handle restocking, and monitor orders.

Supplier Panel:
Update stock, fulfill orders, and track delivery performance.

Customer Panel:
Browse products, place orders, and view delivery status.

📈 Result and Visualization

Zodiac simplifies end-to-end supply chain management by offering:

Seamless coordination between all user roles.

Real-time data updates across dashboards.

Smooth visual interface with responsive UI components.

Highlights:

📦 Stock visualization with auto-update.

📊 Order status tracking in real time.

💬 Role-based dashboards ensuring clarity of operations.

🧠 Future Enhancements

Integration of AI-based demand forecasting.

Automated email notifications for order updates.

Web and mobile versions using Flask or Flutter.

👨‍💻 Author

Taranjeet Singh
📧 [taran.pvt@gmail.com
]
🕓 Developed as part of the Zodiac Supply Chain Project
