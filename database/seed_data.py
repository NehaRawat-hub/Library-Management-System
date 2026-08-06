from database.database import connect

def seed():
    con = connect()
    books = [
        ("9780132350884","Clean Code","Robert C. Martin","Programming","Prentice Hall",2008,5,5),
        ("9781491950296","Fluent Python","Luciano Ramalho","Programming","O'Reilly",2022,3,3),
        ("9780262033848","Introduction to Algorithms","Cormen et al.","Algorithms","MIT Press",2009,4,4),
    ]
    for b in books:
        con.execute("""INSERT OR IGNORE INTO books
            (isbn,title,author,category,publisher,year,quantity,available_quantity)
            VALUES (?,?,?,?,?,?,?,?)""", b)
    members = [
        ("M001","Demo Student","student@example.com","9999999999"),
        ("M002","Demo Faculty","faculty@example.com","8888888888"),
    ]
    for m in members:
        con.execute("""INSERT OR IGNORE INTO members(member_code,name,email,phone)
                       VALUES(?,?,?,?)""", m)
    con.commit()
    con.close()

if __name__ == "__main__":
    seed()
