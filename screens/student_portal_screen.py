"""
screens/student_portal_screen.py
--------------------------------
Student & Faculty Self-Service Portal.
Enables students and faculty members to:
  1. Inspect their profile, registration code, and contact information.
  2. View currently borrowed books with due dates, countdowns, and fine calculations.
  3. Browse and search the entire library catalog in real-time with live stock availability.
  4. Review past borrowing history and return records.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from database.database import connect
from config.config import load_settings


def render(app):
    settings = load_settings()
    fine_per_day = float(settings.get("fine_per_day", 5))

    # Determine which member profile to view
    member_code = getattr(app, "member_code", None)
    con = connect()

    # If no member_code is associated with the session (e.g., admin previewing), pick the first student
    if not member_code:
        first_mem = con.execute("SELECT member_code FROM members WHERE member_type='Student' LIMIT 1").fetchone()
        member_code = first_mem[0] if first_mem else "M001"

    member_row = con.execute(
        "SELECT id, member_code, name, email, phone, member_type FROM members WHERE member_code=?",
        (member_code,)
    ).fetchone()

    con.close()

    if not member_row:
        body = app.base("Student Portal", "Member profile could not be loaded")
        tk.Label(body, text="Member profile not found. Please log in with a valid student account.").pack(pady=20)
        return

    m_id, m_code, m_name, m_email, m_phone, m_type = member_row

    body = app.base(
        f"{m_name}'s Library Portal",
        f"{m_type} ID: {m_code}  •  {m_email}  •  Ph: {m_phone}"
    )

    theme = app.get_theme()
    today = date.today()

    # --- Fetch Active Loans & Calculate Fines ---
    con = connect()
    active_txs = con.execute("""
        SELECT t.id, b.title, b.author, b.isbn, t.issue_date, t.due_date, t.status
        FROM transactions t
        JOIN books b ON b.id = t.book_id
        WHERE t.member_id = ? AND t.status = 'ISSUED'
        ORDER BY t.due_date ASC
    """, (m_id,)).fetchall()

    history_txs = con.execute("""
        SELECT t.id, b.title, b.author, b.isbn, t.issue_date, t.return_date, t.status
        FROM transactions t
        JOIN books b ON b.id = t.book_id
        WHERE t.member_id = ? AND t.status = 'RETURNED'
        ORDER BY t.return_date DESC
    """, (m_id,)).fetchall()
    con.close()

    total_fine = 0.0
    overdue_count = 0
    loan_rows = []

    for tx in active_txs:
        t_id, title, author, isbn, iss_d, due_d, status = tx
        try:
            due_date_obj = datetime.strptime(due_d, "%Y-%m-%d").date()
            if today > due_date_obj:
                days_overdue = (today - due_date_obj).days
                fine = days_overdue * fine_per_day
                total_fine += fine
                overdue_count += 1
                status_text = f"Overdue ({days_overdue} days)"
                fine_text = f"INR {fine:.2f}"
            else:
                days_left = (due_date_obj - today).days
                status_text = f"On Time ({days_left} days left)"
                fine_text = "INR 0.00"
        except Exception:
            status_text = "Issued"
            fine_text = "INR 0.00"

        loan_rows.append((t_id, title, author, isbn, iss_d, due_d, status_text, fine_text))

    # --- Top KPI Summary Cards ---
    cards_frame = tk.Frame(body, bg=theme["bg_main"])
    cards_frame.pack(fill="x", pady=(0, 15))

    kpis = [
        ("Currently Borrowed", f"{len(active_txs)} Books", "#2563eb"),
        ("Overdue Status", f"{overdue_count} Overdue", "#dc2626" if overdue_count > 0 else "#16a34a"),
        ("Accumulated Fine", f"INR {total_fine:.2f}", "#d97706" if total_fine > 0 else "#475569"),
        ("Past Completed Loans", f"{len(history_txs)} Returned", "#059669"),
    ]

    for i, (title, val, accent) in enumerate(kpis):
        card = tk.Frame(cards_frame, bg=theme["bg_card"], bd=1, relief="solid", padx=16, pady=12)
        card.grid(row=0, column=i, padx=6, sticky="nsew")
        cards_frame.columnconfigure(i, weight=1)

        # Top accent bar
        tk.Frame(card, bg=accent, height=3).pack(fill="x", pady=(0, 6))
        tk.Label(card, text=val, bg=theme["bg_card"], fg=theme["fg_header"],
                 font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(card, text=title, bg=theme["bg_card"], fg=theme["fg_muted"],
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))

    # --- Notebook Tabs for Portal Views ---
    style = ttk.Style()
    style.configure("Portal.TNotebook", background=theme["bg_main"])
    style.configure("Portal.TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[16, 6])

    notebook = ttk.Notebook(body, style="Portal.TNotebook")
    notebook.pack(fill="both", expand=True)

    # 1. Active Loans Tab
    tab_loans = tk.Frame(notebook, bg=theme["bg_main"], padx=10, pady=10)
    notebook.add(tab_loans, text="  📖 My Active Loans  ")

    loan_cols = ["TX ID", "Book Title", "Author", "ISBN", "Issue Date", "Due Date", "Status", "Fine"]
    loan_widths = [60, 240, 160, 120, 100, 100, 140, 90]
    loan_tree = app.table(tab_loans, loan_cols, loan_widths)
    for r in loan_rows:
        loan_tree.insert("", "end", values=r)

    if not loan_rows:
        tk.Label(
            tab_loans,
            text="You have no active book loans. Search the catalog below to borrow books!",
            bg=theme["bg_main"],
            fg=theme["fg_muted"],
            font=("Segoe UI", 11)
        ).pack(pady=20)

    # 2. Browse & Search Catalog Tab
    tab_catalog = tk.Frame(notebook, bg=theme["bg_main"], padx=10, pady=10)
    notebook.add(tab_catalog, text="  🔍 Search Library Catalog  ")

    search_bar = tk.Frame(tab_catalog, bg=theme["bg_main"])
    search_bar.pack(fill="x", pady=(0, 10))

    tk.Label(search_bar, text="Search Book:", bg=theme["bg_main"], fg=theme["fg_header"],
             font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
    cat_entry = tk.Entry(search_bar, width=35, font=("Segoe UI", 10))
    cat_entry.pack(side="left", padx=5)

    cat_cols = ["ID", "ISBN", "Title", "Author", "Category", "Year", "Availability"]
    cat_widths = [50, 130, 260, 180, 140, 70, 110]
    cat_tree = app.table(tab_catalog, cat_cols, cat_widths)

    def refresh_catalog():
        for row_id in cat_tree.get_children():
            cat_tree.delete(row_id)
        q = cat_entry.get().strip()
        c = connect()
        if q:
            rows = c.execute("""
                SELECT id, isbn, title, author, category, year, available_quantity, quantity
                FROM books
                WHERE title LIKE ? OR author LIKE ? OR category LIKE ? OR isbn LIKE ?
                ORDER BY title ASC
            """, tuple([f"%{q}%"] * 4)).fetchall()
        else:
            rows = c.execute("""
                SELECT id, isbn, title, author, category, year, available_quantity, quantity
                FROM books
                ORDER BY title ASC
            """).fetchall()
        c.close()

        for b in rows:
            bid, isbn, title, author, cat, yr, avail, total = b
            avail_str = f"Available ({avail}/{total})" if avail > 0 else "Checked Out"
            cat_tree.insert("", "end", values=(bid, isbn, title, author, cat, yr, avail_str))

    tk.Button(
        search_bar,
        text="Search",
        command=refresh_catalog,
        bg=theme["accent"],
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=12,
        pady=4
    ).pack(side="left", padx=6)

    tk.Button(
        search_bar,
        text="Clear",
        command=lambda: [cat_entry.delete(0, tk.END), refresh_catalog()],
        bg="#64748b",
        fg="white",
        font=("Segoe UI", 9),
        bd=0,
        padx=10,
        pady=4
    ).pack(side="left")

    cat_entry.bind("<Return>", lambda e: refresh_catalog())
    refresh_catalog()

    # 3. Borrowing History Tab
    tab_history = tk.Frame(notebook, bg=theme["bg_main"], padx=10, pady=10)
    notebook.add(tab_history, text="  📜 Borrowing History  ")

    hist_cols = ["TX ID", "Book Title", "Author", "ISBN", "Issue Date", "Return Date", "Status"]
    hist_widths = [60, 260, 180, 130, 110, 110, 100]
    hist_tree = app.table(tab_history, hist_cols, hist_widths)
    for h in history_txs:
        hist_tree.insert("", "end", values=h)

    if not history_txs:
        tk.Label(
            tab_history,
            text="No historical loan records found.",
            bg=theme["bg_main"],
            fg=theme["fg_muted"],
            font=("Segoe UI", 11)
        ).pack(pady=20)
