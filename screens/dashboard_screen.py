"""
screens/dashboard_screen.py
----------------------------
Home screen: KPI cards driven by real data from services/report_service.py,
plus a short summary of the TQM controls built into the system.
"""

import tkinter as tk
from services.report_service import stats

TQM_CONTROL_POINTS = [
    "✓ Error prevention at source (Poka-Yoke validation)",
    "✓ Automatic activity and audit logging",
    "✓ Centralized configuration and system settings",
    "✓ Modular architecture for Q11 maintainability",
    "✓ Error capture with severity and resolution status",
    "✓ Quality monitoring based on actual system data",
]


def render(app):
    body = app.base(
        "Library Management System",
        "Customer-focused library operations with built-in TQM controls",
    )

    s = stats()
    cards = [
        ("Total Books", s["books"]),
        ("Available Copies", s["available"]),
        ("Members", s["members"]),
        ("Active Issues", s["issued"]),
        ("Logged Activities", s["activities"]),
        ("Recorded Errors", s["errors"]),
    ]

    grid = tk.Frame(body, bg="#f4f6f8")
    grid.pack(fill="x")
    for i, (label, value) in enumerate(cards):
        card = tk.Frame(grid, bg="white", bd=1, relief="solid", padx=20, pady=16)
        card.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="nsew")
        grid.columnconfigure(i % 3, weight=1)
        tk.Label(card, text=str(value), bg="white", fg="#16202a",
                 font=("Segoe UI", 25, "bold")).pack(anchor="w")
        tk.Label(card, text=label, bg="white", fg="#607080",
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

    info = tk.Frame(body, bg="white", bd=1, relief="solid", padx=24, pady=18)
    info.pack(fill="both", expand=True, padx=8, pady=20)
    tk.Label(info, text="TQM Quality Controls", bg="white", fg="#16202a",
             font=("Segoe UI", 15, "bold")).pack(anchor="w")
    for point in TQM_CONTROL_POINTS:
        tk.Label(info, text=point, bg="white", fg="#34495e",
                 font=("Segoe UI", 11)).pack(anchor="w", pady=5)
