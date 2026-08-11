"""
screens/quality_screen.py
---------------------------
Quality Monitor screen: fact-based quality metrics pulled straight from
the database (services/report_service.py) -- no hard-coded numbers, in
line with the "Fact-Based Decision Making" TQM principle.
"""

import tkinter as tk
from services.report_service import stats


def render(app):
    body = app.base("Quality Monitor", "Fact-based quality evidence from actual application activity")

    s = stats()
    frame = tk.Frame(body, bg="white", bd=1, relief="solid", padx=25, pady=20)
    frame.pack(fill="x")

    metrics = [
        ("Operations logged", s["activities"]),
        ("Recorded errors", s["errors"]),
        ("Active transactions", s["issued"]),
        ("Book inventory", s["books"]),
    ]
    for i, (label, value) in enumerate(metrics):
        tk.Label(frame, text=f"{label}: {value}", bg="white", fg="#16202a",
                 font=("Segoe UI", 13, "bold")).grid(row=0, column=i, padx=18, pady=10)

    tk.Label(
        body,
        text="Quality principle: measure actual defects and activities; do not fabricate statistics.",
        bg="#f4f6f8", fg="#52616f", font=("Segoe UI", 10),
    ).pack(anchor="w", pady=15)
