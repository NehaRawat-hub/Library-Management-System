"""
screens/members_screen.py
---------------------------
Member management screen: search and add members (students & faculty).
Persistence goes through services/member_service.py; field checks go
through utils/validators.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from services.member_service import MemberService
from utils.validators import validate_member
from utils.logger import activity
from utils.error_handler import handle_exception

COLUMNS = ["ID", "Member Code", "Name", "Email", "Phone", "Type", "Joined Date"]
WIDTHS = [50, 110, 190, 200, 130, 90, 140]


def render(app):
    theme = app.get_theme()
    body = app.base(
        "Patron & Member Directory",
        "Directory of registered students, faculty members, and research scholars"
    )

    top = tk.Frame(body, bg=theme["bg_main"])
    top.pack(fill="x", pady=(0, 10))

    tk.Label(
        top,
        text="Search Member:",
        bg=theme["bg_main"],
        fg=theme["fg_header"],
        font=("Segoe UI", 10, "bold")
    ).pack(side="left", padx=(0, 6))

    search = tk.Entry(top, width=32, font=("Segoe UI", 10))
    search.pack(side="left", padx=5)

    tree = app.table(body, COLUMNS, WIDTHS)

    def refresh():
        for row_id in tree.get_children():
            tree.delete(row_id)
        for row in MemberService().all(search.get()):
            tree.insert("", "end", values=row)

    def open_add_dialog():
        if getattr(app, "role", "Staff") in ["Student"]:
            messagebox.showwarning("Restricted", "Students cannot register new members.")
            return

        win = tk.Toplevel(app)
        win.title("Register New Library Member")
        win.geometry("480x480")
        win.configure(bg=theme["bg_card"])

        tk.Label(
            win,
            text="Member Registration Form",
            bg=theme["bg_card"],
            fg=theme["fg_header"],
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=25, pady=(20, 10))

        fields = [
            ("Member Code (e.g. M008, F006)", "code"),
            ("Full Name", "name"),
            ("Email Address", "email"),
            ("Phone Number", "phone"),
        ]

        entries = {}
        for label_text, key in fields:
            tk.Label(
                win,
                text=label_text + ":",
                bg=theme["bg_card"],
                fg=theme["fg_body"],
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", padx=25, pady=(8, 2))
            entry = tk.Entry(win, font=("Segoe UI", 10))
            entry.pack(fill="x", padx=25)
            entries[key] = entry

        tk.Label(
            win,
            text="Membership Category:",
            bg=theme["bg_card"],
            fg=theme["fg_body"],
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=25, pady=(8, 2))

        type_combo = ttk.Combobox(win, values=["Student", "Faculty"], state="readonly", font=("Segoe UI", 10))
        type_combo.set("Student")
        type_combo.pack(fill="x", padx=25)

        def save():
            code = entries["code"].get().strip()
            name = entries["name"].get().strip()
            email = entries["email"].get().strip()
            phone = entries["phone"].get().strip()
            mtype = type_combo.get()

            ok, msg = validate_member(code, name, email)
            if not ok:
                messagebox.showwarning("Validation Error", msg)
                return

            try:
                new_id = MemberService().add(code, name, email, phone, mtype)
                activity(app.username, app.role, "Members", "MEMBER_ADDED", f"code={code}, type={mtype}")
                messagebox.showinfo("Success", f"{mtype} '{name}' registered successfully.")
                win.destroy()
                refresh()
            except Exception as exc:
                handle_exception(app.username, "Members", "Add member", exc)
                messagebox.showerror("Error", str(exc))

        tk.Button(
            win,
            text="Register Member",
            command=save,
            bg=theme["accent"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=20)

    tk.Button(
        top,
        text="Search",
        command=refresh,
        bg=theme["accent"],
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=12,
        pady=4,
        cursor="hand2"
    ).pack(side="left", padx=4)

    tk.Button(
        top,
        text="Reset",
        command=lambda: [search.delete(0, tk.END), refresh()],
        bg="#64748b",
        fg="white",
        font=("Segoe UI", 9),
        bd=0,
        padx=10,
        pady=4,
        cursor="hand2"
    ).pack(side="left", padx=4)

    if getattr(app, "role", "Staff") in ["Admin", "Staff"]:
        tk.Button(
            top,
            text="➕ Register New Member",
            command=open_add_dialog,
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2"
        ).pack(side="right")

    search.bind("<Return>", lambda e: refresh())
    refresh()
