"""
screens/app_shell.py
---------------------
The application shell: modern vertical sidebar navigation, dark/light mode
support, role-based screen routing (Admin, Staff, Student, Faculty), and
reusable UI layout helpers.
"""

import tkinter as tk
from tkinter import ttk

from config.config import load_settings, save_settings
from database.database import initialize
from database.seed_data import seed

from screens import (
    dashboard_screen,
    books_screen,
    members_screen,
    transactions_screen,
    quality_screen,
    logs_screen,
    settings_screen,
    login_screen,
    student_portal_screen,
)

APP_TITLE = "Library Management System"

THEMES = {
    "Light": {
        "bg_main": "#f8fafc",
        "bg_card": "#ffffff",
        "bg_sidebar": "#1e293b",
        "bg_sidebar_active": "#2563eb",
        "bg_sidebar_hover": "#334155",
        "fg_sidebar": "#f1f5f9",
        "fg_sidebar_dim": "#94a3b8",
        "fg_header": "#0f172a",
        "fg_body": "#334155",
        "fg_muted": "#64748b",
        "card_border": "#e2e8f0",
        "accent": "#2563eb",
        "accent_hover": "#1d4ed8",
        "table_bg": "#ffffff",
        "table_fg": "#1e293b",
        "table_heading_bg": "#f1f5f9",
        "table_heading_fg": "#0f172a",
    },
    "Dark": {
        "bg_main": "#0f172a",
        "bg_card": "#1e293b",
        "bg_sidebar": "#090d16",
        "bg_sidebar_active": "#3b82f6",
        "bg_sidebar_hover": "#1e293b",
        "fg_sidebar": "#f8fafc",
        "fg_sidebar_dim": "#64748b",
        "fg_header": "#f8fafc",
        "fg_body": "#cbd5e1",
        "fg_muted": "#94a3b8",
        "card_border": "#334155",
        "accent": "#3b82f6",
        "accent_hover": "#60a5fa",
        "table_bg": "#1e293b",
        "table_fg": "#f1f5f9",
        "table_heading_bg": "#334155",
        "table_heading_fg": "#f8fafc",
    }
}


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Database initialization & seeding
        initialize()
        seed()

        # Load persisted settings
        self.settings = load_settings()
        saved_theme = self.settings.get("theme", "Light")
        self.theme_mode = "Dark" if saved_theme == "Dark" else "Light"

        # Current session state
        self.username = "admin"
        self.role = "Admin"
        self.member_code = None
        self.current_screen_name = "dashboard"

        # Window chrome
        self.title(APP_TITLE)
        self.geometry("1240x780")
        self.minsize(1050, 680)

        self.apply_theme_styles()
        self.show_dashboard()

    def get_theme(self):
        return THEMES[self.theme_mode]

    def toggle_theme(self):
        self.theme_mode = "Dark" if self.theme_mode == "Light" else "Light"
        self.settings["theme"] = self.theme_mode
        save_settings(self.settings)
        self.apply_theme_styles()
        self.refresh_current_screen()

    def apply_theme_styles(self):
        theme = self.get_theme()
        self.configure(bg=theme["bg_main"])

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            background=theme["table_bg"],
            foreground=theme["table_fg"],
            fieldbackground=theme["table_bg"],
            rowheight=32,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background=theme["table_heading_bg"],
            foreground=theme["table_heading_fg"],
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", theme["accent"])],
            foreground=[("selected", "white")]
        )
        style.configure("TNotebook", background=theme["bg_main"], borderwidth=0)
        style.configure("TNotebook.Tab", background=theme["bg_card"], foreground=theme["fg_body"], padding=[14, 6])

    # ------------------------------------------------------------------
    # Base Layout with Vertical Sidebar
    # ------------------------------------------------------------------
    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def base(self, title, subtitle=""):
        """Draws the vertical sidebar and returns the main scrollable body frame."""
        self.clear()
        theme = self.get_theme()

        # Root horizontal container
        container = tk.Frame(self, bg=theme["bg_main"])
        container.pack(fill="both", expand=True)

        # ----------------- Left Sidebar -----------------
        sidebar = tk.Frame(container, bg=theme["bg_sidebar"], width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Brand / Logo
        brand_frame = tk.Frame(sidebar, bg=theme["bg_sidebar"], pady=18, padx=16)
        brand_frame.pack(fill="x")

        tk.Label(
            brand_frame,
            text="📚 LibraryOS",
            bg=theme["bg_sidebar"],
            fg=theme["fg_sidebar"],
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand_frame,
            text="Intelligent Library System",
            bg=theme["bg_sidebar"],
            fg=theme["fg_sidebar_dim"],
            font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(sidebar, bg=theme["bg_sidebar_hover"], height=1).pack(fill="x", padx=12, pady=(0, 10))

        # User Badge in Sidebar
        user_card = tk.Frame(sidebar, bg=theme["bg_sidebar_hover"], padx=12, pady=10)
        user_card.pack(fill="x", padx=12, pady=(0, 14))

        role_colors = {
            "Admin": "#f59e0b",
            "Staff": "#06b6d4",
            "Student": "#10b981",
            "Faculty": "#a855f7"
        }
        badge_color = role_colors.get(self.role, "#3b82f6")

        user_header = tk.Frame(user_card, bg=theme["bg_sidebar_hover"])
        user_header.pack(fill="x")

        tk.Label(
            user_header,
            text="👤 " + self.username.capitalize(),
            bg=theme["bg_sidebar_hover"],
            fg=theme["fg_sidebar"],
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        role_badge = tk.Label(
            user_header,
            text=f" {self.role} ",
            bg=badge_color,
            fg="white",
            font=("Segoe UI", 8, "bold")
        )
        role_badge.pack(side="right")

        if self.member_code:
            tk.Label(
                user_card,
                text=f"ID: {self.member_code}",
                bg=theme["bg_sidebar_hover"],
                fg=theme["fg_sidebar_dim"],
                font=("Segoe UI", 8)
            ).pack(anchor="w", pady=(3, 0))

        # Dynamic Nav Items by Role
        nav_container = tk.Frame(sidebar, bg=theme["bg_sidebar"])
        nav_container.pack(fill="both", expand=True, padx=8)

        if self.role in ["Student", "Faculty"]:
            nav_items = [
                ("👤 My Portal", self.show_student_portal, "student_portal"),
                ("📖 Catalog Search", self.show_books, "books"),
                ("📊 Library Stats", self.show_dashboard, "dashboard"),
            ]
        else:
            nav_items = [
                ("📊 Dashboard", self.show_dashboard, "dashboard"),
                ("📚 Books Catalog", self.show_books, "books"),
                ("👥 Members", self.show_members, "members"),
                ("🔄 Issue / Return", self.show_transactions, "transactions"),
                ("🎓 Student Portal", self.show_student_portal, "student_portal"),
                ("📈 Analytics", self.show_quality, "quality"),
                ("📋 Activity Logs", self.show_logs, "logs"),
            ]
            if self.role == "Admin":
                nav_items.append(("⚙️ Settings", self.show_settings, "settings"))

        for label, cmd, screen_key in nav_items:
            is_active = (self.current_screen_name == screen_key)
            btn_bg = theme["bg_sidebar_active"] if is_active else theme["bg_sidebar"]
            btn_fg = "white" if is_active else theme["fg_sidebar"]

            btn = tk.Button(
                nav_container,
                text=f"  {label}",
                command=cmd,
                bg=btn_bg,
                fg=btn_fg,
                activebackground=theme["bg_sidebar_hover"],
                activeforeground="white",
                bd=0,
                anchor="w",
                padx=12,
                pady=9,
                font=("Segoe UI", 10, "bold" if is_active else "normal")
            )
            btn.pack(fill="x", pady=2)

        # Bottom Controls (Theme toggle & Switch user)
        bottom_frame = tk.Frame(sidebar, bg=theme["bg_sidebar"], pady=12, padx=10)
        bottom_frame.pack(side="bottom", fill="x")

        # Theme Toggle Button
        theme_label = "🌙 Dark Mode" if self.theme_mode == "Light" else "☀️ Light Mode"
        tk.Button(
            bottom_frame,
            text=theme_label,
            command=self.toggle_theme,
            bg=theme["bg_sidebar_hover"],
            fg=theme["fg_sidebar"],
            activebackground=theme["bg_sidebar_active"],
            activeforeground="white",
            bd=0,
            padx=10,
            pady=6,
            font=("Segoe UI", 9, "bold")
        ).pack(fill="x", pady=(0, 6))

        # Logout / Switch User
        tk.Button(
            bottom_frame,
            text="🚪 Switch Account",
            command=self.show_login,
            bg="#ef4444" if self.theme_mode == "Dark" else "#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=6,
            font=("Segoe UI", 9, "bold")
        ).pack(fill="x")

        # ----------------- Main Right Content Area -----------------
        content_area = tk.Frame(container, bg=theme["bg_main"])
        content_area.pack(side="right", fill="both", expand=True)

        # Top Header Bar
        top_header = tk.Frame(content_area, bg=theme["bg_card"], height=70, bd=1, relief="solid")
        top_header.pack(fill="x")
        top_header.pack_propagate(False)

        header_inner = tk.Frame(top_header, bg=theme["bg_card"])
        header_inner.pack(fill="both", expand=True, padx=28, pady=10)

        title_box = tk.Frame(header_inner, bg=theme["bg_card"])
        title_box.pack(side="left", anchor="w")

        tk.Label(
            title_box,
            text=title,
            bg=theme["bg_card"],
            fg=theme["fg_header"],
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        if subtitle:
            tk.Label(
                title_box,
                text=subtitle,
                bg=theme["bg_card"],
                fg=theme["fg_muted"],
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 0))

        # Body container
        body = tk.Frame(content_area, bg=theme["bg_main"])
        body.pack(fill="both", expand=True, padx=26, pady=20)
        return body

    def table(self, parent, columns, widths=None):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for i, c in enumerate(columns):
            tree.heading(c, text=c)
            tree.column(c, width=(widths[i] if widths else 120), anchor="w")
        tree.pack(fill="both", expand=True, pady=10)
        return tree

    # ------------------------------------------------------------------
    # Screen routing
    # ------------------------------------------------------------------
    def refresh_current_screen(self):
        screen_map = {
            "dashboard": self.show_dashboard,
            "books": self.show_books,
            "members": self.show_members,
            "transactions": self.show_transactions,
            "student_portal": self.show_student_portal,
            "quality": self.show_quality,
            "logs": self.show_logs,
            "settings": self.show_settings,
            "login": self.show_login,
        }
        fn = screen_map.get(self.current_screen_name, self.show_dashboard)
        fn()

    def show_dashboard(self):
        self.current_screen_name = "dashboard"
        dashboard_screen.render(self)

    def show_books(self):
        self.current_screen_name = "books"
        books_screen.render(self)

    def show_members(self):
        self.current_screen_name = "members"
        members_screen.render(self)

    def show_transactions(self):
        self.current_screen_name = "transactions"
        transactions_screen.render(self)

    def show_student_portal(self):
        self.current_screen_name = "student_portal"
        student_portal_screen.render(self)

    def show_quality(self):
        self.current_screen_name = "quality"
        quality_screen.render(self)

    def show_logs(self):
        self.current_screen_name = "logs"
        logs_screen.render(self)

    def show_settings(self):
        self.current_screen_name = "settings"
        settings_screen.render(self)

    def show_login(self):
        self.current_screen_name = "login"
        login_screen.render(self)
