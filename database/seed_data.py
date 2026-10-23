from database.database import connect

def seed():
    con = connect()
    books = [
        ("9780132350884", "Clean Code", "Robert C. Martin", "Programming", "Prentice Hall", 2008, 5, 5),
        ("9781491950296", "Fluent Python", "Luciano Ramalho", "Programming", "O'Reilly", 2022, 3, 3),
        ("9780262033848", "Introduction to Algorithms", "Cormen et al.", "Algorithms", "MIT Press", 2009, 4, 4),
        ("9780134685991", "Effective Java", "Joshua Bloch", "Programming", "Addison-Wesley", 2018, 4, 4),
        ("9780135957059", "The Pragmatic Programmer", "David Thomas, Andrew Hunt", "Software Engineering", "Addison-Wesley", 2019, 3, 3),
    ]
    for b in books:
        con.execute("""INSERT OR IGNORE INTO books
            (isbn,title,author,category,publisher,year,quantity,available_quantity)
            VALUES (?,?,?,?,?,?,?,?)""", b)

    members = [
        ("M001", "Neha Rawat", "neha.rawat@example.edu", "9876543210"),
        ("M002", "Aarav Sharma", "aarav.sharma@example.edu", "9812345678"),
        ("M003", "Prof. K. Verma", "k.verma@example.edu", "9823456789"),
    ]
    for m in members:
        con.execute("""INSERT OR IGNORE INTO members(member_code,name,email,phone)
                       VALUES(?,?,?,?)""", m)

    # Seed baseline audit logs if table is mostly empty
    audit_count = con.execute("SELECT COUNT(*) FROM audit_logs").fetchone()[0]
    if audit_count < 5:
        sample_audits = [
            ("2026-09-01 09:00:00", "admin", "Admin", "System", "SYSTEM_INITIALIZE", "Database & tables created", "SUCCESS"),
            ("2026-09-01 09:15:00", "admin", "Admin", "Settings", "SYSTEM_SETTINGS_CONFIGURED", "overdue_days=14, fine=5", "SUCCESS"),
            ("2026-09-02 10:00:00", "admin", "Admin", "Books", "BOOK_ADDED", "ISBN: 9780132350884 (Clean Code)", "SUCCESS"),
            ("2026-09-02 10:10:00", "admin", "Admin", "Books", "BOOK_ADDED", "ISBN: 9781491950296 (Fluent Python)", "SUCCESS"),
            ("2026-09-02 10:20:00", "admin", "Admin", "Books", "BOOK_ADDED", "ISBN: 9780262033848 (Introduction to Algorithms)", "SUCCESS"),
            ("2026-09-03 11:00:00", "staff", "Staff", "Members", "MEMBER_ADDED", "Code: M001 (Neha Rawat)", "SUCCESS"),
            ("2026-09-03 11:15:00", "staff", "Staff", "Members", "MEMBER_ADDED", "Code: M002 (Aarav Sharma)", "SUCCESS"),
            ("2026-09-04 14:00:00", "staff", "Staff", "Transactions", "BOOK_ISSUED", "Book 1 to Member 1", "SUCCESS"),
            ("2026-09-18 10:30:00", "staff", "Staff", "Transactions", "BOOK_RETURNED", "Book 1 returned by Member 1", "SUCCESS"),
            ("2026-09-20 15:00:00", "admin", "Admin", "Security", "USER_LOGIN", "role=Admin", "SUCCESS"),
        ]
        con.executemany("""
            INSERT INTO audit_logs (timestamp, username, role, module, action, record_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_audits)

    con.commit()
    con.close()

if __name__ == "__main__":
    seed()
