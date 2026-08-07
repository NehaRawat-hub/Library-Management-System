from datetime import datetime
from config.config import LOG_DIR
from database.database import connect

LOG_DIR.mkdir(parents=True, exist_ok=True)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def activity(username, role, module, action, record_id="", status="SUCCESS",
             old_value="", new_value=""):
    stamp = now()
    with (LOG_DIR / "activity.log").open("a", encoding="utf-8") as f:
        f.write(f"{stamp} | {username} | {module} | {action} | {record_id} | {status}\n")
    con = connect()
    con.execute("""INSERT INTO audit_logs
        (timestamp,username,role,module,action,record_id,old_value,new_value,status)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (stamp, username, role, module, action, str(record_id), old_value, new_value, status))
    con.commit()
    con.close()

def error(username, module, operation, exc, severity="MEDIUM"):
    stamp = now()
    msg = str(exc)
    with (LOG_DIR / "error.log").open("a", encoding="utf-8") as f:
        f.write(f"{stamp} | {username} | {module} | {operation} | {severity} | {type(exc).__name__}: {msg}\n")
    con = connect()
    con.execute("""INSERT INTO error_logs
        (timestamp,username,module,operation,error_type,error_message,severity)
        VALUES (?,?,?,?,?,?,?)""",
        (stamp, username, module, operation, type(exc).__name__, msg, severity))
    con.commit()
    con.close()
