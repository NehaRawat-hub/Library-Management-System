from database.database import connect

class BookService:
    def all(self, search=""):
        con = connect()
        if search:
            rows = con.execute("""SELECT * FROM books
                WHERE isbn LIKE ? OR title LIKE ? OR author LIKE ? OR category LIKE ?
                ORDER BY id DESC""", tuple([f"%{search}%"]*4)).fetchall()
        else:
            rows = con.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
        con.close()
        return rows

    def add(self, isbn,title,author,category,publisher,year,quantity):
        con = connect()
        cur = con.execute("""INSERT INTO books
            (isbn,title,author,category,publisher,year,quantity,available_quantity)
            VALUES(?,?,?,?,?,?,?,?)""",
            (isbn,title,author,category,publisher,year,quantity,quantity))
        con.commit()
        rid = cur.lastrowid
        con.close()
        return rid

    def delete(self, book_id):
        con = connect()
        con.execute("DELETE FROM books WHERE id=?", (book_id,))
        con.commit()
        con.close()
