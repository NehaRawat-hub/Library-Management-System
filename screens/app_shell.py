"""
screens/app_shell.py
---------------------
The application shell: the Tk root window, the header/nav bar, and the
shared layout helpers (base(), table()) that every screen reuses.

This file intentionally contains NO business logic and NO screen-specific
widgets. Its only job is:
  1. Bootstrap the database on startup.
  2. Provide consistent chrome (header + navigation bar).
  3. Route each nav button to the matching screen module's render(app).

Adding a new screen therefore never requires touching this file's layout
code -- just add a module under screens/ and one line in NAV_ITEMS below.
"""

import tkinter as tk
from tkinter import ttk

from database.database import initialize
from database.seed_data import seed

from screens import (
    dashboard_screen,
    books_screen,
    members_screen,
    transactions_screen,
    quality_screen,
    logs_screen,
)

APP_TITLE = "Library Management System — TQM Edition"
BG_BODY = "#f4f6f8"
BG_HEADER = "#16202a"
BG_NAV = "#22303d"


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Q11 maintainability: startup boots DB + demo seed data once ---
        initialize()
        seed()

        # --- current session (kept simple for this course project) ---
        self.username = "admin"
        self.role = "Admin"

        # --- window chrome ---
        self.title(APP_TITLE)
        self.geometry("1180x720")
        self.minsize(1000, 650)
        self.configure(bg=BG_BODY)

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10))

        # --- nav bar -> screen module mapping ---
        self.nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Books", self.show_books),
            ("Members", self.show_members),
            ("Issue / Return", self.show_transactions),
            ("Quality Monitor", self.show_quality),
            ("Audit Logs", self.show_logs),
        ]

        self.show_dashboard()

    # ------------------------------------------------------------------
    # Shared layout helpers used by every screen module
    # ------------------------------------------------------------------
    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def header(self, title, subtitle=""):
        frame = tk.Frame(self, bg=BG_HEADER, height=80)
        frame.pack(fill="x")
        tk.Label(frame, text=title, bg=BG_HEADER, fg="white",
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=28, pady=(16, 0))
        if subtitle:
            tk.Label(frame, text=subtitle, bg=BG_HEADER, fg="#c9d2dc",
                     font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(2, 10))

    def nav(self):
        bar = tk.Frame(self, bg=BG_NAV, height=50)
        bar.pack(fill="x")
        for text, cmd in self.nav_items:
            tk.Button(bar, text=text, command=cmd, bg=BG_NAV, fg="white",
                      activebackground="#34495e", activeforeground="white",
                      bd=0, padx=15, pady=12, font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(bar, text=f"Logged in: {self.username} ({self.role})",
                 bg=BG_NAV, fg="#dce5ed").pack(side="right", padx=20)

    def base(self, title, subtitle=""):
        """Clear the window and draw header + nav; returns the empty body frame."""
        self.clear()
        self.header(title, subtitle)
        self.nav()
        body = tk.Frame(self, bg=BG_BODY)
        body.pack(fill="both", expand=True, padx=24, pady=22)
        return body

    def table(self, parent, columns, widths=None):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for i, c in enumerate(columns):
            tree.heading(c, text=c)
            tree.column(c, width=(widths[i] if widths else 120), anchor="w")
        tree.pack(fill="both", expand=True, pady=12)
        return tree

    # ------------------------------------------------------------------
    # Screen routing -- each of these just delegates to screens/*.py
    # ------------------------------------------------------------------
    def show_dashboard(self):
        dashboard_screen.render(self)

    def show_books(self):
        books_screen.render(self)

    def show_members(self):
        members_screen.render(self)

    def show_transactions(self):
        transactions_screen.render(self)

    def show_quality(self):
        quality_screen.render(self)

    def show_logs(self):
        logs_screen.render(self)
