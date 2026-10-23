"""
screens/login_screen.py
-----------------------
Authentication portal with role-based login (Admin, Staff, Student, Faculty)
and quick-select profiles for students and faculty.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from database.database import connect
from utils.logger import activity
from utils.error_handler import handle_exception


def render(app):
    theme = app.get_theme()
    body = app.base(
        "Library Authentication Portal",
        "Sign in with your staff, administrator, student, or faculty credentials"
    )

    outer_container = tk.Frame(body, bg=theme["bg_main"])
    outer_container.pack(expand=True)

    # Main Card
    card = tk.Frame(outer_container, bg=theme["bg_card"], bd=1, relief="solid", padx=40, pady=32)
    card.pack(pady=10)

    tk.Label(
        card,
        text="Sign In to LibraryOS",
        bg=theme["bg_card"],
        fg=theme["fg_header"],
        font=("Segoe UI", 18, "bold")
    ).pack(pady=(0, 20))

    # --- Student & Faculty One-Click Sign In Box ---
    student_box = tk.LabelFrame(
        card,
        text=" Student & Faculty Direct Access ",
        bg=theme["bg_card"],
        fg=theme["accent"],
        font=("Segoe UI", 10, "bold"),
        padx=18,
        pady=14
    )
    student_box.pack(fill="x", pady=(0, 20))

    tk.Label(
        student_box,
        text="Select Your Member Profile:",
        bg=theme["bg_card"],
        fg=theme["fg_body"],
        font=("Segoe UI", 9)
    ).pack(anchor="w", pady=(0, 5))

    con = connect()
    members_list = con.execute("""
        SELECT u.username, m.member_code, m.name, m.member_type
        FROM users u
        JOIN members m ON m.member_code = u.member_code
        ORDER BY m.member_type DESC, m.name ASC
    """).fetchall()
    con.close()

    member_display_map = {}
    combo_values = []
    for u, mcode, mname, mtype in members_list:
        label = f"{mname} ({mtype} - {mcode})"
        combo_values.append(label)
        member_display_map[label] = (u, mcode, mname, mtype)

    member_combo = ttk.Combobox(student_box, values=combo_values, state="readonly", width=38, font=("Segoe UI", 10))
    if combo_values:
        member_combo.current(0)
    member_combo.pack(fill="x", pady=6)

    def login_selected_member():
        selected = member_combo.get()
        if not selected or selected not in member_display_map:
            messagebox.showwarning("Selection Required", "Please select a member profile from the dropdown.")
            return

        username, mcode, mname, mtype = member_display_map[selected]
        app.username = username
        app.role = mtype
        app.member_code = mcode

        activity(app.username, app.role, "Authentication", "STUDENT_PORTAL_LOGIN", f"code={mcode}")
        messagebox.showinfo("Welcome", f"Welcome back, {mname}! Opening your {mtype} portal.")
        app.show_student_portal()

    tk.Button(
        student_box,
        text="Open Student / Faculty Portal",
        command=login_selected_member,
        bg="#16a34a",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        bd=0,
        padx=15,
        pady=7,
        cursor="hand2"
    ).pack(fill="x", pady=(6, 0))

    # Divider
    tk.Label(
        card,
        text="— OR ENTER CREDENTIALS —",
        bg=theme["bg_card"],
        fg=theme["fg_muted"],
        font=("Segoe UI", 8, "bold")
    ).pack(pady=10)

    # --- Standard Username & Password Form ---
    form_frame = tk.Frame(card, bg=theme["bg_card"])
    form_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        form_frame,
        text="Username:",
        bg=theme["bg_card"],
        fg=theme["fg_body"],
        font=("Segoe UI", 10, "bold")
    ).grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))

    user_entry = tk.Entry(form_frame, width=28, font=("Segoe UI", 10))
    user_entry.grid(row=0, column=1, pady=6)
    user_entry.insert(0, "admin")

    tk.Label(
        form_frame,
        text="Password:",
        bg=theme["bg_card"],
        fg=theme["fg_body"],
        font=("Segoe UI", 10, "bold")
    ).grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))

    pwd_entry = tk.Entry(form_frame, width=28, show="*", font=("Segoe UI", 10))
    pwd_entry.grid(row=1, column=1, pady=6)
    pwd_entry.insert(0, "admin123")

    def perform_auth(u=None, p=None):
        uname = (u or user_entry.get()).strip()
        pwd = p or pwd_entry.get()

        if not uname or not pwd:
            messagebox.showwarning("Input Required", "Please enter username and password.")
            return

        try:
            con = connect()
            user_row = con.execute(
                "SELECT username, role, member_code FROM users WHERE username=? AND password=?",
                (uname, pwd)
            ).fetchone()
            con.close()

            if not user_row:
                raise ValueError("Invalid username or password. Please try again.")

            app.username = user_row[0]
            app.role = user_row[1]
            app.member_code = user_row[2]

            activity(app.username, app.role, "Authentication", "USER_LOGIN", f"role={app.role}")

            if app.role in ["Student", "Faculty"]:
                app.show_student_portal()
            else:
                app.show_dashboard()

        except Exception as exc:
            handle_exception(uname, "Authentication", "Login attempt", exc)
            messagebox.showerror("Authentication Failed", str(exc))

    tk.Button(
        card,
        text="Sign In",
        command=perform_auth,
        bg=theme["accent"],
        fg="white",
        font=("Segoe UI", 10, "bold"),
        bd=0,
        padx=20,
        pady=7,
        cursor="hand2"
    ).pack(fill="x", pady=(5, 15))

    # --- Quick Staff / Admin Presets ---
    quick_box = tk.Frame(card, bg=theme["bg_card"])
    quick_box.pack(fill="x")

    tk.Button(
        quick_box,
        text="Admin Account",
        command=lambda: perform_auth("admin", "admin123"),
        bg="#d97706",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2"
    ).pack(side="left", expand=True, fill="x", padx=(0, 4))

    tk.Button(
        quick_box,
        text="Staff Account",
        command=lambda: perform_auth("staff", "staff123"),
        bg="#0891b2",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2"
    ).pack(side="right", expand=True, fill="x", padx=(4, 0))
