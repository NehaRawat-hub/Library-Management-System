from datetime import date, timedelta
from config.config import load_settings
from database.database import connect

class IssueService:
    def issue(self, book_id, member_id):
        con = connect()
        book = con.execute("SELECT available_quantity FROM books WHERE id=?", (book_id,)).fetchone()
        if not book:
            raise ValueError("Book not found.")
        if book[0] <= 0:
            raise ValueError("Book is currently unavailable.")
        due = date.today() + timedelta(days=int(load_settings()["overdue_days"]))
        cur = con.execute("""INSERT INTO transactions
            (book_id,member_id,issue_date,due_date,status) VALUES(?,?,?,?,?)""",
            (book_id,member_id,date.today().isoformat(),due.isoformat(),"ISSUED"))
        con.execute("UPDATE books SET available_quantity=available_quantity-1 WHERE id=?", (book_id,))
        con.commit()
        rid = cur.lastrowid
        con.close()
        return rid

    def active(self):
        con = connect()
        rows = con.execute("""SELECT t.id,b.title,m.name,t.issue_date,t.due_date,t.status
            FROM transactions t JOIN books b ON b.id=t.book_id
            JOIN members m ON m.id=t.member_id
            WHERE t.status='ISSUED' ORDER BY t.id DESC""").fetchall()
        con.close()
        return rows

    def return_book(self, transaction_id):
        con = connect()
        tx = con.execute("SELECT book_id,status FROM transactions WHERE id=?", (transaction_id,)).fetchone()
        if not tx:
            raise ValueError("Transaction not found.")
        if tx[1] != "ISSUED":
            raise ValueError("This transaction has already been returned.")
        con.execute("UPDATE transactions SET return_date=date('now'),status='RETURNED' WHERE id=?",
                    (transaction_id,))
        con.execute("UPDATE books SET available_quantity=available_quantity+1 WHERE id=?", (tx[0],))
        con.commit()
        con.close()
