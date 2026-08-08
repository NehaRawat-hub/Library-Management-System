from database.database import connect

class MemberService:
    def all(self, search=""):
        con = connect()
        if search:
            rows = con.execute("""SELECT * FROM members
                WHERE member_code LIKE ? OR name LIKE ? OR email LIKE ?
                ORDER BY id DESC""", tuple([f"%{search}%"]*3)).fetchall()
        else:
            rows = con.execute("SELECT * FROM members ORDER BY id DESC").fetchall()
        con.close()
        return rows

    def add(self, code,name,email,phone):
        con = connect()
        cur = con.execute("""INSERT INTO members(member_code,name,email,phone)
                             VALUES(?,?,?,?)""", (code,name,email,phone))
        con.commit()
        rid = cur.lastrowid
        con.close()
        return rid
