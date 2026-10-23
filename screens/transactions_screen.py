"""
screens/transactions_screen.py
--------------------------------
Circulation Desk: Manage active book borrowings, issue new loans,
and process book returns with automatic stock and fine updates.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from services.issue_service import IssueService
from database.database import connect
from config.config import load_settings
from utils.logger import activity
from utils.error_handler import handle_exception

COLUMNS = ["TX ID", "Book Title", "Member Name", "Member Code", "Issue Date", "Due Date", "Status"]
WIDTHS = [55, 250, 170, 110, 110, 110, 130]


def render(app):
    theme = app.get_theme()
    body = app.base(
        "Circulation & Loan Desk",
        "Process book checkouts, check in returns, and inspect active patron borrowings"
    )

    settings = load_settings()
    fine_per_day = float(settings.get("fine_per_day", 5))
    today = date.today()

    # Form Control Card
    control_card = tk.Frame(body, bg=theme["bg_card"], bd=1, relief="solid", padx=20, pady=16)
    control_card.pack(fill="x", pady=(0, 14))

    tk.Label(
        control_card,
        text="Issue New Book Loan:",
        bg=theme["bg_card"],
        fg=theme["fg_header"],
        font=("Segoe UI", 11, "bold")
    ).pack(anchor="w", pady=(0, 10))

    form_row = tk.Frame(control_card, bg=theme["bg_card"])
    form_row.pack(fill="x")

    tk.Label(
        form_row,
        text="Book ID / Call #:",
        bg=theme["bg_card"],
        fg=theme["fg_body"],
        font=("Segoe UI", 9, "bold")
    ).pack(side="left", padx=(0, 4))

    book_entry = tk.Entry(form_row, width=8, font=("Segoe UI", 10))
    book_entry.pack(side="left", padx=(0, 15))

    tk.Label(
        form_row,
        text="Member ID:",
        bg=theme["bg_card"],
        fg=theme["fg_body"],
        font=("Segoe UI", 9, "bold")
    ).pack(side="left", padx=(0, 4))

    member_entry = tk.Entry(form_row, width=8, font=("Segoe UI", 10))
    member_entry.pack(side="left", padx=(0, 20))

    tree = app.table(body, COLUMNS, WIDTHS)

    def refresh():
        for row_id in tree.get_children():
            tree.delete(row_id)

        con = connect()
        rows = con.execute("""
            SELECT t.id, b.title, m.name, m.member_code, t.issue_date, t.due_date, t.status
            FROM transactions t
            JOIN books b ON b.id = t.book_id
            JOIN members m ON m.id = t.member_id
            WHERE t.status = 'ISSUED'
            ORDER BY t.due_date ASC
        """).fetchall()
        con.close()

        for r in rows:
            t_id, title, m_name, m_code, iss_d, due_d, status = r
            try:
                due_dt = datetime.strptime(due_d, "%Y-%m-%d").date()
                if today > due_dt:
                    diff = (today - due_dt).days
                    status_str = f"⚠️ Overdue ({diff}d - INR {diff*fine_per_day:.0f})"
                else:
                    days_left = (due_dt - today).days
                    status_str = f"Active ({days_left}d left)"
            except Exception:
                status_str = status

            tree.insert("", "end", values=(t_id, title, m_name, m_code, iss_d, due_d, status_str))

    def issue_book():
        if getattr(app, "role", "Staff") in ["Student"]:
            messagebox.showwarning("Restricted", "Students cannot execute circulation checkouts.")
            return

        b_txt = book_entry.get().strip()
        m_txt = member_entry.get().strip()

        if not b_txt or not m_txt:
            messagebox.showwarning("Missing Input", "Please enter both Book ID and Member ID.")
            return

        try:
            b_id = int(b_txt)
            m_id = int(m_txt)
            new_id = IssueService().issue(b_id, m_id)
            activity(app.username, app.role, "Transactions", "BOOK_ISSUED", f"tx_id={new_id}, book={b_id}, member={m_id}")
            messagebox.showinfo("Success", f"Book successfully checked out! Transaction ID: {new_id}")
            book_entry.delete(0, tk.END)
            member_entry.delete(0, tk.END)
            refresh()
        except Exception as exc:
            handle_exception(app.username, "Transactions", "Issue book", exc)
            messagebox.showerror("Checkout Blocked", str(exc))

    def return_selected():
        if getattr(app, "role", "Staff") in ["Student"]:
            messagebox.showwarning("Restricted", "Students cannot process return check-ins.")
            return

        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Selection Required", "Please select an active loan row to process return.")
            return

        item = tree.item(selection[0])
        transaction_id = item["values"][0]
        book_title = item["values"][1]
        member_name = item["values"][2]

        if messagebox.askyesno("Confirm Check-In", f"Process return for '{book_title}' checked out by {member_name}?"):
            try:
                IssueService().return_book(int(transaction_id))
                activity(app.username, app.role, "Transactions", "BOOK_RETURNED", f"tx_id={transaction_id}")
                messagebox.showinfo("Check-In Complete", "Book checked in and returned to shelf stock.")
                refresh()
            except Exception as exc:
                handle_exception(app.username, "Transactions", "Return book", exc)
                messagebox.showerror("Return Failed", str(exc))

    tk.Button(
        form_row,
        text="Issue Book Loan",
        command=issue_book,
        bg=theme["accent"],
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=14,
        pady=5,
        cursor="hand2"
    ).pack(side="left", padx=4)

    tk.Button(
        form_row,
        text="Return Selected Item",
        command=return_selected,
        bg="#16a34a",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=14,
        pady=5,
        cursor="hand2"
    ).pack(side="left", padx=4)

    tk.Button(
        form_row,
        text="Refresh List",
        command=refresh,
        bg="#64748b",
        fg="white",
        font=("Segoe UI", 9),
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2"
    ).pack(side="left", padx=4)

    refresh()
