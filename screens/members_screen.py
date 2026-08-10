"""
screens/members_screen.py
---------------------------
Member management screen: search and add members.
Persistence goes through services/member_service.py; field checks go
through utils/validators.py.
"""

import tkinter as tk
from tkinter import messagebox

from services.member_service import MemberService
from utils.validators import validate_member
from utils.logger import activity
from utils.error_handler import handle_exception

COLUMNS = ["ID", "Code", "Name", "Email", "Phone", "Created"]
WIDTHS = [60, 100, 200, 220, 140, 160]
FIELD_LABELS = ["Member Code", "Name", "Email", "Phone"]


def render(app):
    body = app.base("Member Management", "Customer records with input validation")

    top = tk.Frame(body, bg="#f4f6f8")
    top.pack(fill="x")
    search = tk.Entry(top, width=35, font=("Segoe UI", 11))
    search.pack(side="left", padx=8)

    tree = app.table(body, COLUMNS, WIDTHS)

    def refresh():
        for row_id in tree.get_children():
            tree.delete(row_id)
        for row in MemberService().all(search.get()):
            tree.insert("", "end", values=row)

    def open_add_dialog():
        win = tk.Toplevel(app)
        win.title("Add Member")
        win.geometry("480x430")
        entries = {}
        for label in FIELD_LABELS:
            tk.Label(win, text=label, font=("Segoe UI", 10, "bold")).pack(
                anchor="w", padx=25, pady=(12, 2))
            entry = tk.Entry(win, font=("Segoe UI", 11))
            entry.pack(fill="x", padx=25)
            entries[label] = entry

        def save():
            try:
                values = [entries[label].get().strip() for label in FIELD_LABELS]
                code, name, email, phone = values
                ok, msg = validate_member(code, name, email)
                if not ok:
                    messagebox.showwarning("Validation", msg)
                    return
                new_id = MemberService().add(code, name, email, phone)
                activity(app.username, app.role, "Members", "MEMBER_ADDED", new_id)
                win.destroy()
                refresh()
            except Exception as exc:
                handle_exception(app.username, "Members", "Add member", exc)
                messagebox.showerror("Could not save", "Member could not be added.")

        tk.Button(win, text="Save Member", command=save, bg="#16202a", fg="white",
                  padx=20, pady=10).pack(pady=20)

    tk.Button(top, text="Search", command=refresh).pack(side="left", padx=5)
    tk.Button(top, text="Add Member", command=open_add_dialog).pack(side="left", padx=5)

    refresh()
