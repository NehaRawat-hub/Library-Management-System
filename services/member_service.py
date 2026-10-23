from database.database import connect

class MemberService:
    def all(self, search=""):
        con = connect()
        if search:
            rows = con.execute("""
                SELECT id, member_code, name, email, phone, member_type, created_at
                FROM members
                WHERE member_code LIKE ? OR name LIKE ? OR email LIKE ? OR member_type LIKE ?
                ORDER BY id DESC
            """, tuple([f"%{search}%"] * 4)).fetchall()
        else:
            rows = con.execute("""
                SELECT id, member_code, name, email, phone, member_type, created_at
                FROM members
                ORDER BY id DESC
            """).fetchall()
        con.close()
        return rows

    def add(self, code, name, email, phone, member_type="Student"):
        con = connect()
        cur = con.execute("""
            INSERT INTO members (member_code, name, email, phone, member_type)
            VALUES (?, ?, ?, ?, ?)
        """, (code, name, email, phone, member_type))
        con.commit()
        rid = cur.lastrowid
        con.close()
        return rid
