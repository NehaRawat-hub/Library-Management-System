from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
from database.database import DB_PATH

def main():
    con = sqlite3.connect(DB_PATH)
    rows = con.execute("""SELECT error_type, COUNT(*) FROM error_logs
                          GROUP BY error_type ORDER BY COUNT(*) DESC""").fetchall()
    con.close()
    if not rows:
        print("Insufficient data for Pareto analysis.")
        return
    labels=[r[0] for r in rows]
    values=[r[1] for r in rows]
    total=sum(values)
    cumulative=[]
    running=0
    for v in values:
        running += v
        cumulative.append(running/total*100)
    fig, ax = plt.subplots(figsize=(9,5))
    ax.bar(labels, values)
    ax.set_ylabel("Defect frequency")
    ax.set_title("Library System Defect Pareto Analysis")
    ax.tick_params(axis="x", rotation=30)
    ax2=ax.twinx()
    ax2.plot(labels,cumulative,marker="o")
    ax2.set_ylabel("Cumulative %")
    ax2.set_ylim(0,110)
    out=Path(__file__).parent/"pareto_chart.png"
    fig.tight_layout()
    fig.savefig(out,dpi=150)
    print(f"Saved {out}")

if __name__ == "__main__":
    main()
