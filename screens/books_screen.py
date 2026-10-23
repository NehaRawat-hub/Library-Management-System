"""
screens/books_screen.py
-------------------------
Book management screen: search, add and delete books.
Persistence goes through services/book_service.py; field checks
go through utils/validators.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from services.book_service import BookService
from utils.validators import validate_book
from utils.logger import activity
from utils.error_handler import handle_exception

COLUMNS = ["ID", "ISBN", "Title", "Author", "Category", "Publisher", "Year", "Qty", "Available"]
WIDTHS = [50, 130, 240, 160, 140, 130, 65, 55, 75]
FIELD_LABELS = ["ISBN", "Title", "Author", "Category", "Publisher", "Year", "Quantity"]


def render(app):
    theme = app.get_theme()
    body = app.base(
        "Book Inventory & Catalog",
        "Browse, search, and manage library titles and active shelf copies"
    )

    top = tk.Frame(body, bg=theme["bg_main"])
    top.pack(fill="x", pady=(0, 10))

    tk.Label(
        top,
        text="Search Catalog:",
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
        for row in BookService().all(search.get()):
            tree.insert("", "end", values=row)

    def open_add_dialog():
        if getattr(app, "role", "Staff") in ["Student"]:
            messagebox.showwarning("Restricted", "Students cannot add or delete catalog entries.")
            return

        win = tk.Toplevel(app)
        win.title("Add New Book Title")
        win.geometry("500x560")
        win.configure(bg=theme["bg_card"])

        tk.Label(
            win,
            text="Add Book to Collection",
            bg=theme["bg_card"],
            fg=theme["fg_header"],
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=25, pady=(20, 10))

        entries = {}
        for label in FIELD_LABELS:
            tk.Label(
                win,
                text=label + ":",
                bg=theme["bg_card"],
                fg=theme["fg_body"],
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", padx=25, pady=(8, 2))
            entry = tk.Entry(win, font=("Segoe UI", 10))
            entry.pack(fill="x", padx=25)
            entries[label] = entry

        def save():
            ok, msg = validate_book(
                entries["ISBN"].get(),
                entries["Title"].get(),
                entries["Author"].get(),
                entries["Category"].get(),
                entries["Quantity"].get()
            )
            if not ok:
                messagebox.showwarning("Validation Error", msg)
                return

            try:
                new_id = BookService().add(
                    entries["ISBN"].get().strip(),
                    entries["Title"].get().strip(),
                    entries["Author"].get().strip(),
                    entries["Category"].get().strip(),
                    entries["Publisher"].get().strip(),
                    int(entries["Year"].get() or 2024),
                    int(entries["Quantity"].get().strip())
                )
                activity(app.username, app.role, "Books", "BOOK_ADDED", str(new_id))
                messagebox.showinfo("Success", "Book successfully added to catalog.")
                win.destroy()
                refresh()
            except Exception as exc:
                handle_exception(app.username, "Books", "Add book", exc)
                messagebox.showerror("Error", str(exc))

        tk.Button(
            win,
            text="Save to Catalog",
            command=save,
            bg=theme["accent"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=20)

    def delete_selected():
        if getattr(app, "role", "Staff") != "Admin":
            messagebox.showwarning("Restricted", "Only Administrators can delete catalog entries.")
            return

        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Select Book", "Please select a book row to delete.")
            return

        item = tree.item(selection[0])
        book_id = item["values"][0]
        title = item["values"][2]

        if messagebox.askyesno("Confirm Deletion", f"Permanently remove '{title}' (ID: {book_id}) from catalog?"):
            try:
                BookService().delete(book_id)
                activity(app.username, app.role, "Books", "BOOK_DELETED", str(book_id))
                refresh()
                messagebox.showinfo("Deleted", "Book removed from catalog.")
            except Exception as exc:
                handle_exception(app.username, "Books", "Delete book", exc)
                messagebox.showerror("Error", str(exc))

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

    # Admin & Staff controls
    if getattr(app, "role", "Staff") in ["Admin", "Staff"]:
        tk.Button(
            top,
            text="➕ Add New Book",
            command=open_add_dialog,
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2"
        ).pack(side="right", padx=(6, 0))

        if getattr(app, "role", "Staff") == "Admin":
            tk.Button(
                top,
                text="🗑️ Delete Selected",
                command=delete_selected,
                bg="#dc2626",
                fg="white",
                font=("Segoe UI", 9, "bold"),
                bd=0,
                padx=12,
                pady=4,
                cursor="hand2"
            ).pack(side="right")

    search.bind("<Return>", lambda e: refresh())
    refresh()
