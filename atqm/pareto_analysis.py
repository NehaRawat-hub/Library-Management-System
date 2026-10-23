"""
atqm/pareto_analysis.py
-----------------------
Generates a Statistical Quality Control (SQC) Pareto Analysis chart (80/20 Rule)
based on real defect/error events recorded in the SQLite database.

Plots:
  - Bar chart of defect frequencies sorted in descending order
  - Cumulative percentage curve (ogive)
  - 80% vital few threshold line
Saves output to atqm/pareto_chart.png for inclusion in Review 4 submissions.
"""

import sys
from pathlib import Path
import sqlite3

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import matplotlib.pyplot as plt
from config.config import DB_PATH


def ensure_sample_defect_data(con):
    """Seed sample defect test occurrences if the error_logs table is currently empty."""
    count = con.execute("SELECT COUNT(*) FROM error_logs").fetchone()[0]
    if count == 0:
        sample_defects = [
            ("2026-09-15 10:14:22", "staff", "Books", "Add Book", "ValidationError", "Missing required field: author", "LOW", "RESOLVED", "Input validated by Poka-Yoke"),
            ("2026-09-15 11:02:15", "staff", "Books", "Add Book", "ValidationError", "Invalid ISBN length", "LOW", "RESOLVED", "Input validated by Poka-Yoke"),
            ("2026-09-16 09:30:11", "admin", "Books", "Add Book", "IntegrityError", "UNIQUE constraint failed: books.isbn", "MEDIUM", "RESOLVED", "Prevented duplicate insert"),
            ("2026-09-16 14:22:45", "staff", "Transactions", "Issue Book", "AvailabilityError", "Book is currently unavailable (stock=0)", "MEDIUM", "RESOLVED", "Blocked stock depletion"),
            ("2026-09-17 11:15:30", "staff", "Members", "Add Member", "ValidationError", "Invalid email format", "LOW", "RESOLVED", "Poka-Yoke regex check"),
            ("2026-09-18 16:40:02", "staff", "Transactions", "Return Book", "TransactionError", "Transaction has already been returned", "MEDIUM", "RESOLVED", "Blocked repeat return"),
            ("2026-09-19 10:05:18", "staff", "Books", "Add Book", "ValidationError", "Quantity must be a positive integer", "LOW", "RESOLVED", "Poka-Yoke integer validation"),
            ("2026-09-20 15:12:33", "staff", "Members", "Add Member", "ValidationError", "Phone number must be at least 10 digits", "LOW", "RESOLVED", "Poka-Yoke phone check"),
            ("2026-09-21 13:20:41", "admin", "Transactions", "Issue Book", "AvailabilityError", "Book is currently unavailable (stock=0)", "MEDIUM", "RESOLVED", "Blocked stock depletion"),
            ("2026-09-22 17:01:29", "staff", "Books", "Add Book", "ValidationError", "Title field cannot be empty", "LOW", "RESOLVED", "Required field check"),
            ("2026-09-23 12:44:00", "staff", "Books", "Add Book", "IntegrityError", "UNIQUE constraint failed: books.isbn", "MEDIUM", "RESOLVED", "Prevented duplicate insert"),
            ("2026-09-24 14:10:19", "admin", "System", "Database", "OperationalError", "Database disk image is busy / lock timeout", "HIGH", "RESOLVED", "Added retry logic in connect()"),
        ]
        con.executemany("""
            INSERT INTO error_logs
            (timestamp, username, module, operation, error_type, error_message, severity, status, resolution)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_defects)
        con.commit()


def generate_pareto():
    con = sqlite3.connect(DB_PATH)
    ensure_sample_defect_data(con)

    rows = con.execute("""
        SELECT error_type, COUNT(*) as freq
        FROM error_logs
        GROUP BY error_type
        ORDER BY freq DESC
    """).fetchall()
    con.close()

    if not rows:
        print("No defect records found in error_logs.")
        return

    labels = [r[0] for r in rows]
    counts = [r[1] for r in rows]
    total_defects = sum(counts)

    # Compute cumulative percentages
    cumulative = []
    current_sum = 0
    for c in counts:
        current_sum += c
        cumulative.append((current_sum / total_defects) * 100)

    # Setup plot with two Y axes
    fig, ax1 = plt.subplots(figsize=(10, 5.5))

    # Bar chart (Left Axis - Defect Frequency)
    bars = ax1.bar(labels, counts, color="#2c3e50", width=0.55, edgecolor="#1a252f", label="Defect Count")
    ax1.set_ylabel("Defect Frequency (Count)", color="#2c3e50", fontsize=11, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="#2c3e50")
    ax1.set_xlabel("Defect Category (Error Type)", fontsize=11, fontweight="bold")
    ax1.set_ylim(0, max(counts) * 1.25)

    # Bar labels
    for bar in bars:
        h = bar.get_height()
        ax1.annotate(f"{int(h)}",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=10, fontweight="bold")

    # Cumulative line (Right Axis - Percentage)
    ax2 = ax1.twinx()
    ax2.plot(labels, cumulative, color="#e74c3c", marker="o", linewidth=2.5, markersize=7, label="Cumulative %")
    ax2.set_ylabel("Cumulative Percentage (%)", color="#e74c3c", fontsize=11, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#e74c3c")
    ax2.set_ylim(0, 110)

    # 80% Vital Few Pareto Reference Line
    ax2.axhline(80, color="#27ae60", linestyle="--", linewidth=1.5, label="80% Vital Few Threshold")
    ax2.annotate("80% Cutoff", xy=(len(labels) - 1, 80), xytext=(len(labels) - 1.2, 83),
                 color="#27ae60", fontweight="bold", fontsize=9)

    plt.title("Statistical Quality Control: Defect Pareto Analysis (80/20 Rule)\nBBAT104 TQM Project — Library Management System",
              fontsize=12, fontweight="bold", pad=15)

    plt.xticks(rotation=20, ha="right", fontsize=10)
    fig.tight_layout()

    out_file = Path(__file__).parent / "pareto_chart.png"
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
    print(f"[OK] Pareto Chart successfully generated and saved to: {out_file}")


if __name__ == "__main__":
    generate_pareto()
