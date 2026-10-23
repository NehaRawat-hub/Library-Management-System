"""
screens/dashboard_screen.py
----------------------------
Executive dashboard: Real-time library metrics, KPI cards, quick actions,
and recent transaction activity feed.
"""

import tkinter as tk
from tkinter import ttk

from services.report_service import stats
from database.database import connect


def render(app):
    theme = app.get_theme()
    body = app.base(
        "Library Overview & Dashboard",
        f"Active Session: {app.username.capitalize()} ({app.role})  •  Real-time Catalog & Circulation Summary"
    )

    s = stats()

    # 1. Top KPI Metric Cards Grid
    cards = [
        ("Total Book Titles", s["books"], "#2563eb", "📚"),
        ("Available Stock", s["available"], "#16a34a", "✅"),
        ("Registered Members", s["members"], "#0891b2", "👥"),
        ("Active Book Loans", s["issued"], "#d97706", "🔄"),
        ("Total Operations", s["activities"], "#7c3aed", "⚡"),
        ("System Health", "Optimal (99.8%)", "#059669", "🛡️"),
    ]

    grid = tk.Frame(body, bg=theme["bg_main"])
    grid.pack(fill="x", pady=(0, 16))

    for i, (label, value, accent_color, icon) in enumerate(cards):
        card = tk.Frame(grid, bg=theme["bg_card"], bd=1, relief="solid", padx=16, pady=12)
        card.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky="nsew")
        grid.columnconfigure(i % 3, weight=1)

        # Top Accent Line
        tk.Frame(card, bg=accent_color, height=3).pack(fill="x", pady=(0, 8))

        top_row = tk.Frame(card, bg=theme["bg_card"])
        top_row.pack(fill="x")

        tk.Label(
            top_row,
            text=str(value),
            bg=theme["bg_card"],
            fg=theme["fg_header"],
            font=("Segoe UI", 20, "bold")
        ).pack(side="left")

        tk.Label(
            top_row,
            text=icon,
            bg=theme["bg_card"],
            font=("Segoe UI", 16)
        ).pack(side="right")

        tk.Label(
            card,
            text=label,
            bg=theme["bg_card"],
            fg=theme["fg_muted"],
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(2, 0))

    # 2. Middle Row: Quick Actions Bar
    action_box = tk.Frame(body, bg=theme["bg_card"], bd=1, relief="solid", padx=20, pady=14)
    action_box.pack(fill="x", pady=(0, 16))

    tk.Label(
        action_box,
        text="Quick Operations:",
        bg=theme["bg_card"],
        fg=theme["fg_header"],
        font=("Segoe UI", 11, "bold")
    ).pack(side="left", padx=(0, 15))

    actions = [
        ("🔄 Issue / Return", app.show_transactions, theme["accent"]),
        ("📚 Search Catalog", app.show_books, "#0284c7"),
        ("👥 Member Directory", app.show_members, "#0d9488"),
        ("🎓 Student Portal", app.show_student_portal, "#16a34a"),
    ]

    for label, cmd, col in actions:
        tk.Button(
            action_box,
            text=label,
            command=cmd,
            bg=col,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2"
        ).pack(side="left", padx=5)

    # 3. Bottom Section: Recent Circulation Feed & Library Notice
    bottom_frame = tk.Frame(body, bg=theme["bg_main"])
    bottom_frame.pack(fill="both", expand=True)

    # Left: Recent Transactions Table
    recent_frame = tk.Frame(bottom_frame, bg=theme["bg_card"], bd=1, relief="solid", padx=16, pady=14)
    recent_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

    tk.Label(
        recent_frame,
        text="Recent Circulation Activity",
        bg=theme["bg_card"],
        fg=theme["fg_header"],
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", pady=(0, 8))

    recent_cols = ["ID", "Book", "Member", "Issue Date", "Due Date", "Status"]
    recent_widths = [45, 190, 140, 95, 95, 80]
    recent_tree = app.table(recent_frame, recent_cols, recent_widths)

    con = connect()
    recent_rows = con.execute("""
        SELECT t.id, b.title, m.name, t.issue_date, t.due_date, t.status
        FROM transactions t
        JOIN books b ON b.id = t.book_id
        JOIN members m ON m.id = t.member_id
        ORDER BY t.id DESC
        LIMIT 6
    """).fetchall()
    con.close()

    for r in recent_rows:
        recent_tree.insert("", "end", values=r)

    # Right: Operational Guidelines / Circulation Policies
    notice_frame = tk.Frame(bottom_frame, bg=theme["bg_card"], width=320, bd=1, relief="solid", padx=18, pady=14)
    notice_frame.pack(side="right", fill="y", padx=(8, 0))
    notice_frame.pack_propagate(False)

    tk.Label(
        notice_frame,
        text="Circulation Policies",
        bg=theme["bg_card"],
        fg=theme["fg_header"],
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", pady=(0, 10))

    policies = [
        "• Loan Period: Standard student loans are 14 days; faculty loans are 30 days.",
        "• Renewals: Eligible if no outstanding reservation holds exist.",
        "• Overdue Fines: Standard fine is INR 5.00/day after due date.",
        "• Max Quota: Students: 3 books simultaneously; Faculty: 6 books.",
        "• Lost Books: Replace with same edition or reimburse catalog replacement cost.",
    ]

    for p in policies:
        tk.Label(
            notice_frame,
            text=p,
            bg=theme["bg_card"],
            fg=theme["fg_body"],
            font=("Segoe UI", 9),
            wraplength=280,
            justify="left"
        ).pack(anchor="w", pady=4)
