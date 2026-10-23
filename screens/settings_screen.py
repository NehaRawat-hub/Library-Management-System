"""
screens/settings_screen.py
--------------------------
System Settings management screen.
Allows administrators to review and update operational parameters:
  - Overdue Days (standard loan duration)
  - Default Fine Per Day (INR)
  - Max Books Allowed Per Member
  - Application Title
  - Active Theme & Date Format

Modifications are validated, saved to config/settings.json,
mirrored in the SQLite system_settings table, and recorded in audit_logs.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config.config import load_settings, save_settings
from database.database import connect
from utils.logger import activity
from utils.error_handler import handle_exception


def render(app):
    theme = app.get_theme()
    body = app.base(
        "System Settings & Preferences",
        "Configure operational loan durations, overdue fine policies, and interface settings"
    )

    current_settings = load_settings()

    # Main Settings Card
    card = tk.Frame(body, bg=theme["bg_card"], bd=1, relief="solid", padx=30, pady=24)
    card.pack(fill="x", pady=10)

    tk.Label(
        card,
        text="Circulation & Application Parameters",
        bg=theme["bg_card"],
        fg=theme["fg_header"],
        font=("Segoe UI", 13, "bold")
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

    # Form Fields
    fields = [
        ("app_name", "Application Title:", current_settings.get("app_name", "Library Management System")),
        ("overdue_days", "Loan Duration (Days):", str(current_settings.get("overdue_days", 14))),
        ("fine_per_day", "Fine Per Day (INR):", str(current_settings.get("fine_per_day", 5))),
        ("max_books_per_member", "Max Books Per Member:", str(current_settings.get("max_books_per_member", 3))),
        ("date_format", "Date Format:", current_settings.get("date_format", "%Y-%m-%d")),
        ("theme", "Active Theme:", app.theme_mode),
    ]

    entries = {}
    for idx, (key, label_text, default_val) in enumerate(fields, start=1):
        tk.Label(
            card,
            text=label_text,
            bg=theme["bg_card"],
            fg=theme["fg_body"],
            font=("Segoe UI", 10, "bold")
        ).grid(row=idx, column=0, sticky="w", pady=8, padx=(0, 15))

        if key == "theme":
            combo = ttk.Combobox(card, values=["Light", "Dark"], width=32, state="readonly")
            combo.set(default_val)
            combo.grid(row=idx, column=1, sticky="w", pady=8)
            entries[key] = combo
        else:
            entry = tk.Entry(card, width=35, font=("Segoe UI", 10))
            entry.insert(0, str(default_val))
            entry.grid(row=idx, column=1, sticky="w", pady=8)
            entries[key] = entry

    # Button Bar
    btn_frame = tk.Frame(body, bg=theme["bg_main"])
    btn_frame.pack(fill="x", pady=15)

    def save_action():
        # Role-based security check
        if getattr(app, "role", "Staff") != "Admin":
            messagebox.showwarning(
                "Access Restricted",
                "Only users with the 'Admin' role can modify system settings.\n"
                f"Current session: {getattr(app, 'username', 'staff')} ({getattr(app, 'role', 'Staff')})"
            )
            return

        try:
            # Validation
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

            chosen_theme = entries["theme"].get()

            new_settings = {
                "app_name": app_title,
                "overdue_days": overdue,
                "fine_per_day": fine,
                "max_books_per_member": max_books,
                "date_format": entries["date_format"].get().strip() or "%Y-%m-%d",
                "theme": chosen_theme,
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
                f"overdue={overdue}, fine={fine}, max_books={max_books}, theme={chosen_theme}"
            )

            # Update app theme if changed
            if app.theme_mode != chosen_theme:
                app.theme_mode = chosen_theme
                app.apply_theme_styles()

            messagebox.showinfo("Success", "System settings successfully updated and saved.")
            app.show_settings()

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
            entries["theme"].set("Light")
            save_action()

    tk.Button(
        btn_frame,
        text="Save Settings",
        command=save_action,
        bg=theme["accent"],
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=18,
        pady=8,
        bd=0,
        cursor="hand2"
    ).pack(side="left", padx=(0, 10))

    tk.Button(
        btn_frame,
        text="Reset to Defaults",
        command=reset_defaults_action,
        bg="#64748b",
        fg="white",
        font=("Segoe UI", 10),
        padx=14,
        pady=8,
        bd=0,
        cursor="hand2"
    ).pack(side="left")

    # Policy Notes Card (Clean administrative info, no TQM academic meta-text)
    info_card = tk.Frame(body, bg=theme["bg_card"], bd=1, relief="solid", padx=20, pady=15)
    info_card.pack(fill="x", pady=10)

    tk.Label(
        info_card,
        text="Circulation & System Architecture Notes:",
        bg=theme["bg_card"],
        fg=theme["fg_header"],
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w")

    explanation = (
        "• Loan Period: Standard borrowing window before items are flagged overdue.\n"
        "• Overdue Fines: Automatically calculated per calendar day past due date.\n"
        "• Quota Limit: Prevents hoarding by restricting simultaneous active borrowings per member.\n"
        "• Security: Changes are restricted to Admin role and recorded in the audit trail."
    )
    tk.Label(
        info_card,
        text=explanation,
        bg=theme["bg_card"],
        fg=theme["fg_body"],
        font=("Segoe UI", 9),
        justify="left"
    ).pack(anchor="w", pady=(5, 0))
