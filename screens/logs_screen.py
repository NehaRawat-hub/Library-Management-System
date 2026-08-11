"""
screens/logs_screen.py
------------------------
Audit & activity log viewer -- read-only traceability screen required by
the Q11 "Activity Logs" feature.
"""

from database.database import connect

COLUMNS = ["Timestamp", "User", "Module", "Action", "Record", "Status"]
WIDTHS = [160, 100, 120, 220, 100, 100]

QUERY = """
    SELECT timestamp, username, module, action, record_id, status
    FROM audit_logs
    ORDER BY id DESC
    LIMIT 200
"""


def render(app):
    body = app.base("Audit & Activity Logs", "Traceability for important system actions")

    tree = app.table(body, COLUMNS, WIDTHS)

    con = connect()
    rows = con.execute(QUERY).fetchall()
    con.close()

    for row in rows:
        tree.insert("", "end", values=row)
