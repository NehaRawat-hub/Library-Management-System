"""
screens/books_screen.py
-------------------------
Book management screen: search, add and delete books.
All persistence goes through services/book_service.py; all field checks
go through utils/validators.py (Poka-Yoke error prevention).
"""

import tkinter as tk
from tkinter import messagebox

from services.book_service import BookService
from utils.validators import validate_book
from utils.logger import activity
from utils.error_handler import handle_exception

COLUMNS = ["ID", "ISBN", "Title", "Author", "Category", "Publisher", "Year", "Qty", "Available"]
WIDTHS = [50, 130, 210, 150, 120, 130, 70, 60, 80]
FIELD_LABELS = ["ISBN", "Title", "Author", "Category", "Publisher", "Year", "Quantity"]


def render(app):
    body = app.base("Book Management", "CRUD + validation + duplicate prevention")

    top = tk.Frame(body, bg="#f4f6f8")
    top.pack(fill="x")
    search = tk.Entry(top, width=35, font=("Segoe UI", 11))
    search.pack(side="left", padx=8)

    tree = app.table(body, COLUMNS, WIDTHS)

    def refresh():
        for row_id in tree.get_children():
            tree.delete(row_id)
        for row in BookService().all(search.get()):
            tree.insert("", "end", values=row)

    def open_add_dialog():
        win = tk.Toplevel(app)
        win.title("Add Book")
        win.geometry("520x560")
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
                isbn, title, author, category, publisher, year, quantity = values
                ok, msg = validate_book(isbn, title, author, category, quantity)
                if not ok:
                    messagebox.showwarning("Validation", msg)
                    return
                new_id = BookService().add(
                    isbn, title, author, category, publisher,
                    int(year) if year else None, int(quantity),
                )
                activity(app.username, app.role, "Books", "BOOK_ADDED", new_id)
                win.destroy()
                refresh()
            except Exception as exc:
                handle_exception(app.username, "Books", "Add book", exc)
                messagebox.showerror("Could not save", "The book could not be added. Check the error log.")

        tk.Button(win, text="Save Book", command=save, bg="#16202a", fg="white",
                  padx=20, pady=10).pack(pady=20)

    def delete_selected():
        selection = tree.selection()
        if not selection:
            return
        book_id = tree.item(selection[0])["values"][0]
        if not messagebox.askyesno("Confirm", "Delete selected book?"):
            return
        try:
            BookService().delete(book_id)
            activity(app.username, app.role, "Books", "BOOK_DELETED", book_id)
            refresh()
        except Exception as exc:
            handle_exception(app.username, "Books", "Delete book", exc)
            messagebox.showerror("Error", "Could not delete the selected book.")

    tk.Button(top, text="Search", command=refresh).pack(side="left", padx=5)
    tk.Button(top, text="Add Book", command=open_add_dialog).pack(side="left", padx=5)
    tk.Button(top, text="Delete Selected", command=delete_selected).pack(side="left", padx=5)

    refresh()
