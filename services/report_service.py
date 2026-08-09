from database.database import connect

def stats():
    con = connect()
    data = {}
    data["books"] = con.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    data["available"] = con.execute("SELECT COALESCE(SUM(available_quantity),0) FROM books").fetchone()[0]
    data["members"] = con.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    data["issued"] = con.execute("SELECT COUNT(*) FROM transactions WHERE status='ISSUED'").fetchone()[0]
    data["errors"] = con.execute("SELECT COUNT(*) FROM error_logs").fetchone()[0]
    data["activities"] = con.execute("SELECT COUNT(*) FROM audit_logs").fetchone()[0]
    con.close()
    return data
