"""
screens/settings_screen.py
--------------------------
System Settings management screen -- primary GUI implementation of the
assigned Q11 "System Settings" and "Config Files" quality features.

Allows administrators to review and update operational parameters:
  - Overdue Days (loan duration)
  - Default Fine Per Day
  - Max Books Allowed Per Member
  - Application Title
  - Active Theme & Accent Color

All modifications are validated, saved to config/settings.json,
mirrored in the SQLite system_settings table, and recorded in audit_logs.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config.config import load_settings, save_settings
from database.database import connect
from utils.logger import activity
from utils.error_handler import handle_exception


def render(app):
    body = app.base(
        "System Settings",
        "Q11 Feature: Centralized system configuration & runtime settings"
    )

    current_settings = load_settings()

    # Main Card
    card = tk.Frame(body, bg="white", bd=1, relief="solid", padx=30, pady=24)
    card.pack(fill="x", pady=10)

    tk.Label(
        card,
        text="Application & Loan Parameters",
        bg="white",
        fg="#16202a",
        font=("Segoe UI", 13, "bold")
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

    # Form Fields
    fields = [
        ("app_name", "Application Title:", current_settings.get("app_name", "Library Management System")),
        ("overdue_days", "Loan Duration (Days):", str(current_settings.get("overdue_days", 14))),
        ("fine_per_day", "Fine Per Day (INR):", str(current_settings.get("fine_per_day", 5))),
        ("max_books_per_member", "Max Books Per Member:", str(current_settings.get("max_books_per_member", 3))),
        ("date_format", "Date Format:", current_settings.get("date_format", "%Y-%m-%d")),
        ("theme", "Theme:", current_settings.get("theme", "System")),
    ]

    entries = {}
    for idx, (key, label_text, default_val) in enumerate(fields, start=1):
        tk.Label(
            card,
            text=label_text,
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold")
        ).grid(row=idx, column=0, sticky="w", pady=8, padx=(0, 15))

        if key == "theme":
            combo = ttk.Combobox(card, values=["System", "Light", "Dark Slate", "Executive Blue"], width=32, state="readonly")
            combo.set(default_val)
            combo.grid(row=idx, column=1, sticky="w", pady=8)
            entries[key] = combo
        else:
            entry = tk.Entry(card, width=35, font=("Segoe UI", 10))
            entry.insert(0, str(default_val))
            entry.grid(row=idx, column=1, sticky="w", pady=8)
            entries[key] = entry

    # Button Bar
    btn_frame = tk.Frame(body, bg="#f4f6f8")
    btn_frame.pack(fill="x", pady=15)

    def save_action():
        # Role-based security check
        if getattr(app, "role", "Staff") != "Admin":
            messagebox.showwarning(
                "Access Restricted",
                "Only users with the 'Admin' role can modify system settings.\n"
                f"Current user: {getattr(app, 'username', 'staff')} ({getattr(app, 'role', 'Staff')})"
            )
            return

        try:
            # Poka-Yoke Input Validation
            app_title = entries["app_name"].get().strip()
            if not app_title:
                raise ValueError("Application title cannot be empty.")

            try:
                overdue = int(entries["overdue_days"].get().strip())
                if overdue <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Loan duration must be a positive integer (e.g., 7, 14, 30).")

            try:
                fine = float(entries["fine_per_day"].get().strip())
                if fine < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Fine per day must be a non-negative number.")

            try:
                max_books = int(entries["max_books_per_member"].get().strip())
                if max_books <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Max books per member must be a positive integer.")

            new_settings = {
                "app_name": app_title,
                "overdue_days": overdue,
                "fine_per_day": fine,
                "max_books_per_member": max_books,
                "date_format": entries["date_format"].get().strip() or "%Y-%m-%d",
                "theme": entries["theme"].get(),
            }

            # 1. Save to config/settings.json
            save_settings(new_settings)

            # 2. Sync to database system_settings table
            con = connect()
            for k, v in new_settings.items():
                con.execute(
                    "INSERT INTO system_settings(key, value) VALUES(?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                    (k, str(v))
                )
            con.commit()
            con.close()

            # 3. Log audit action
            activity(
                app.username,
                app.role,
                "Settings",
                "SYSTEM_SETTINGS_UPDATED",
                f"overdue={overdue}, fine={fine}, max_books={max_books}"
            )

            messagebox.showinfo("Success", "System settings successfully updated and saved to config/settings.json.")

        except Exception as exc:
            handle_exception(getattr(app, "username", "admin"), "Settings", "Save settings", exc)
            messagebox.showerror("Validation / Save Error", str(exc))

    def reset_defaults_action():
        if getattr(app, "role", "Staff") != "Admin":
            messagebox.showwarning("Access Restricted", "Only Admin can reset settings.")
            return

        if messagebox.askyesno("Confirm Reset", "Reset all system settings to baseline defaults?"):
            entries["app_name"].delete(0, tk.END)
            entries["app_name"].insert(0, "Library Management System")
            entries["overdue_days"].delete(0, tk.END)
            entries["overdue_days"].insert(0, "14")
            entries["fine_per_day"].delete(0, tk.END)
            entries["fine_per_day"].insert(0, "5")
            entries["max_books_per_member"].delete(0, tk.END)
            entries["max_books_per_member"].insert(0, "3")
            entries["date_format"].delete(0, tk.END)
            entries["date_format"].insert(0, "%Y-%m-%d")
            entries["theme"].set("System")
            save_action()

    tk.Button(
        btn_frame,
        text="Save Settings",
        command=save_action,
        bg="#16202a",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=18,
        pady=8,
        bd=0
    ).pack(side="left", padx=(0, 10))

    tk.Button(
        btn_frame,
        text="Reset to Defaults",
        command=reset_defaults_action,
        bg="#7f8c8d",
        fg="white",
        font=("Segoe UI", 10),
        padx=14,
        pady=8,
        bd=0
    ).pack(side="left")

    # Q11 Note Card
    info_card = tk.Frame(body, bg="#ebf5fb", bd=1, relief="solid", padx=20, pady=15)
    info_card.pack(fill="x", pady=10)

    tk.Label(
        info_card,
        text="TQM Quality Goal Q11 — Improve Maintainability Highlights:",
        bg="#ebf5fb",
        fg="#1b4f72",
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w")

    explanation = (
        "• Decoupled Configuration: Operational policies (loan period, fines) are not hardcoded into business logic.\n"
        "• Dual Persistence: Stored as human-readable JSON (config/settings.json) and queryable SQLite (system_settings).\n"
        "• Zero-Downtime Reconfiguration: Changes take effect immediately without recompilation or redeployment.\n"
        "• Full Traceability: Every configuration change is recorded in audit_logs with administrator attribution."
    )
    tk.Label(
        info_card,
        text=explanation,
        bg="#ebf5fb",
        fg="#2c3e50",
        font=("Segoe UI", 9),
        justify="left"
    ).pack(anchor="w", pady=(5, 0))
