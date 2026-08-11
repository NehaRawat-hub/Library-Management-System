"""
screens/transactions_screen.py
--------------------------------
Issue / Return screen. All transaction rules (availability checks, due
dates, duplicate-return prevention) live in services/issue_service.py --
this screen only collects input and displays results.
"""

import tkinter as tk
from tkinter import messagebox

from services.issue_service import IssueService
from utils.logger import activity
from utils.error_handler import handle_exception

COLUMNS = ["ID", "Book", "Member", "Issue Date", "Due Date", "Status"]
WIDTHS = [60, 250, 200, 130, 130, 100]


def render(app):
    body = app.base("Issue / Return", "Controlled transactions with availability validation")

    top = tk.Frame(body, bg="#f4f6f8")
    top.pack(fill="x")
    tk.Label(top, text="Book ID").pack(side="left")
    book_entry = tk.Entry(top, width=8)
    book_entry.pack(side="left", padx=5)
    tk.Label(top, text="Member ID").pack(side="left")
    member_entry = tk.Entry(top, width=8)
    member_entry.pack(side="left", padx=5)

    tree = app.table(body, COLUMNS, WIDTHS)

    def refresh():
        for row_id in tree.get_children():
            tree.delete(row_id)
        for row in IssueService().active():
            tree.insert("", "end", values=row)

    def issue_book():
        try:
            new_id = IssueService().issue(int(book_entry.get()), int(member_entry.get()))
            activity(app.username, app.role, "Transactions", "BOOK_ISSUED", new_id)
            messagebox.showinfo("Success", "Book issued successfully.")
            refresh()
        except Exception as exc:
            handle_exception(app.username, "Transactions", "Issue book", exc)
            messagebox.showwarning("Issue prevented", str(exc))

    def return_selected():
        selection = tree.selection()
        if not selection:
            return
        transaction_id = tree.item(selection[0])["values"][0]
        try:
            IssueService().return_book(int(transaction_id))
            activity(app.username, app.role, "Transactions", "BOOK_RETURNED", transaction_id)
            refresh()
        except Exception as exc:
            handle_exception(app.username, "Transactions", "Return book", exc)
            messagebox.showwarning("Return prevented", str(exc))

    tk.Button(top, text="Issue Book", command=issue_book).pack(side="left", padx=8)
    tk.Button(top, text="Return Selected", command=return_selected).pack(side="left", padx=8)

    refresh()
