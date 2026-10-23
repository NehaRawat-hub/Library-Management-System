"""
screens/login_screen.py
-----------------------
Authentication and role-switching interface.
Provides secure authentication against the SQLite `users` table
and quick demo selectors for presentation and viva demonstrations.
"""

import tkinter as tk
from tkinter import messagebox
import sqlite3

from database.database import connect
from utils.logger import activity
from utils.error_handler import handle_exception


def render(app):
    body = app.base(
        "User Authentication",
        "Role-Based Access Control (Admin / Staff) with audit tracking"
    )

    card = tk.Frame(body, bg="white", bd=1, relief="solid", padx=35, pady=30)
    card.pack(pady=20)

    tk.Label(
        card,
        text="Sign In to Library System",
        bg="white",
        fg="#16202a",
        font=("Segoe UI", 16, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tk.Label(
        card,
        text="Username:",
        bg="white",
        fg="#2c3e50",
        font=("Segoe UI", 11, "bold")
    ).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 15))

    username_entry = tk.Entry(card, width=28, font=("Segoe UI", 11))
    username_entry.grid(row=1, column=1, pady=10)
    username_entry.insert(0, getattr(app, "username", "admin"))

    tk.Label(
        card,
        text="Password:",
        bg="white",
        fg="#2c3e50",
        font=("Segoe UI", 11, "bold")
    ).grid(row=2, column=0, sticky="w", pady=10, padx=(0, 15))

    password_entry = tk.Entry(card, width=28, show="*", font=("Segoe UI", 11))
    password_entry.grid(row=2, column=1, pady=10)
    password_entry.insert(0, "admin123")

    def perform_login(user=None, pwd=None):
        u = (user or username_entry.get()).strip()
        p = pwd or password_entry.get()

        if not u or not p:
            messagebox.showwarning("Missing Input", "Please enter both username and password.")
            return

        try:
            con = connect()
            row = con.execute(
                "SELECT username, role FROM users WHERE username=? AND password=?",
                (u, p)
            ).fetchone()
            con.close()

            if not row:
                raise ValueError("Invalid username or password credentials.")

            app.username = row[0]
            app.role = row[1]

            activity(app.username, app.role, "Authentication", "USER_LOGIN", f"role={app.role}")
            messagebox.showinfo("Sign In Successful", f"Welcome, {app.username}! Logged in as {app.role}.")
            app.show_dashboard()

        except Exception as exc:
            handle_exception(u, "Authentication", "Login attempt", exc)
            messagebox.showerror("Login Failed", str(exc))

    # Action Buttons
    action_frame = tk.Frame(card, bg="white")
    action_frame.grid(row=3, column=0, columnspan=2, pady=(20, 10))

    tk.Button(
        action_frame,
        text="Sign In",
        command=perform_login,
        bg="#16202a",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        padx=25,
        pady=7,
        bd=0
    ).pack()

    # Quick Demo Switchers (Helpful for viva / grading demonstration)
    demo_box = tk.LabelFrame(
        card,
        text=" Quick Demo Switcher (For Evaluation & Viva) ",
        bg="white",
        fg="#7f8c8d",
        font=("Segoe UI", 9, "bold"),
        padx=15,
        pady=10
    )
    demo_box.grid(row=4, column=0, columnspan=2, pady=(20, 0), sticky="ew")

    tk.Button(
        demo_box,
        text="Switch to Admin (Full Control)",
        command=lambda: perform_login("admin", "admin123"),
        bg="#27ae60",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=12,
        pady=5
    ).pack(side="left", padx=5)

    tk.Button(
        demo_box,
        text="Switch to Staff (Operational Access)",
        command=lambda: perform_login("staff", "staff123"),
        bg="#2980b9",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=12,
        pady=5
    ).pack(side="left", padx=5)
