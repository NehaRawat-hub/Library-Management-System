"""
screens/logs_screen.py
------------------------
Audit & activity log viewer -- traceability screen implementing the
Q11 "Activity Logs" feature, enhanced with Defect/Error Logs inspection
and CSV export capability for TQM quality reviews.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
from pathlib import Path

from database.database import connect
from config.config import LOG_DIR
from utils.logger import activity


AUDIT_COLUMNS = ["Timestamp", "User", "Role", "Module", "Action", "Record / Details", "Status"]
AUDIT_WIDTHS = [140, 80, 80, 110, 180, 200, 80]

ERROR_COLUMNS = ["Timestamp", "User", "Module", "Operation", "Error Type", "Message", "Severity", "Status"]
ERROR_WIDTHS = [130, 70, 90, 110, 130, 220, 80, 70]


def render(app):
    body = app.base(
        "Audit & Quality Logs",
        "Full traceability for operations (Activity Logs) and defect tracking (Error Logs)"
    )

    current_view = {"mode": "AUDIT"}

    # Top Control Bar
    top_bar = tk.Frame(body, bg="#f4f6f8")
    top_bar.pack(fill="x", pady=(0, 10))

    view_label = tk.Label(
        top_bar,
        text="Viewing: Audit & Activity Logs",
        bg="#f4f6f8",
        fg="#16202a",
        font=("Segoe UI", 11, "bold")
    )
    view_label.pack(side="left")

    # Table Container Frame
    table_container = tk.Frame(body, bg="#f4f6f8")
    table_container.pack(fill="both", expand=True)

    tree = ttk.Treeview(table_container, show="headings")
    tree.pack(fill="both", expand=True)

    def configure_tree(columns, widths):
        tree["columns"] = columns
        for row_id in tree.get_children():
            tree.delete(row_id)
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=widths[i], anchor="w")

    def load_audit_logs():
        current_view["mode"] = "AUDIT"
        view_label.config(text="Viewing: Audit & Activity Logs (User Actions)")
        configure_tree(AUDIT_COLUMNS, AUDIT_WIDTHS)

        con = connect()
        rows = con.execute("""
            SELECT timestamp, username, role, module, action, record_id, status
            FROM audit_logs
            ORDER BY id DESC
            LIMIT 300
        """).fetchall()
        con.close()

        for r in rows:
            tree.insert("", "end", values=r)

    def load_error_logs():
        current_view["mode"] = "ERROR"
        view_label.config(text="Viewing: Defect & Error Logs (Quality Failures & Exceptions)")
        configure_tree(ERROR_COLUMNS, ERROR_WIDTHS)

        con = connect()
        rows = con.execute("""
            SELECT timestamp, username, module, operation, error_type, error_message, severity, status
            FROM error_logs
            ORDER BY id DESC
            LIMIT 300
        """).fetchall()
        con.close()

        for r in rows:
            tree.insert("", "end", values=r)

    def export_csv():
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            mode = current_view["mode"]

            if mode == "AUDIT":
                export_path = LOG_DIR / "audit_logs_export.csv"
                columns = AUDIT_COLUMNS
                query = "SELECT timestamp, username, role, module, action, record_id, status FROM audit_logs ORDER BY id DESC"
            else:
                export_path = LOG_DIR / "error_logs_export.csv"
                columns = ERROR_COLUMNS
                query = "SELECT timestamp, username, module, operation, error_type, error_message, severity, status FROM error_logs ORDER BY id DESC"

            con = connect()
            rows = con.execute(query).fetchall()
            con.close()

            with open(export_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)

            activity(app.username, app.role, "Logs", "EXPORT_CSV", f"file={export_path.name}, count={len(rows)}")
            messagebox.showinfo("Export Successful", f"Exported {len(rows)} records to:\n{export_path}")

        except Exception as exc:
            messagebox.showerror("Export Failed", str(exc))

    # Switcher buttons on the right of top_bar
    tk.Button(
        top_bar,
        text="Export to CSV",
        command=export_csv,
        bg="#27ae60",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=10,
        pady=5
    ).pack(side="right", padx=(8, 0))

    tk.Button(
        top_bar,
        text="Defect / Error Logs",
        command=load_error_logs,
        bg="#c0392b",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=10,
        pady=5
    ).pack(side="right", padx=4)

    tk.Button(
        top_bar,
        text="Activity Logs",
        command=load_audit_logs,
        bg="#2980b9",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=10,
        pady=5
    ).pack(side="right", padx=4)

    # Initial load
    load_audit_logs()
