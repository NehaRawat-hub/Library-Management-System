from datetime import date, timedelta
from database.database import connect

def seed():
    con = connect()

    # 1. Diverse Book Catalog (25+ books across genres)
    books = [
        # Computer Science & Software Engineering
        ("9780132350884", "Clean Code: A Handbook of Agile Software Craftsmanship", "Robert C. Martin", "Computer Science", "Prentice Hall", 2008, 6, 6),
        ("9781491950296", "Fluent Python: Clear, Concise, and Effective Programming", "Luciano Ramalho", "Computer Science", "O'Reilly", 2022, 4, 4),
        ("9780262033848", "Introduction to Algorithms (4th Edition)", "Thomas H. Cormen, Charles E. Leiserson", "Computer Science", "MIT Press", 2022, 5, 5),
        ("9780134685991", "Effective Java (3rd Edition)", "Joshua Bloch", "Computer Science", "Addison-Wesley", 2018, 4, 4),
        ("9780135957059", "The Pragmatic Programmer: Your Journey to Mastery", "David Thomas, Andrew Hunt", "Computer Science", "Addison-Wesley", 2019, 5, 5),
        ("9780321356680", "Design Patterns: Elements of Reusable Object-Oriented Software", "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides", "Computer Science", "Addison-Wesley", 1994, 4, 4),
        ("9781119456339", "Operating System Concepts (10th Edition)", "Abraham Silberschatz, Peter B. Galvin", "Computer Science", "Wiley", 2018, 6, 6),
        ("9780133594140", "Computer Networking: A Top-Down Approach", "James F. Kurose, Keith W. Ross", "Computer Science", "Pearson", 2020, 5, 5),
        ("9780136042594", "Artificial Intelligence: A Modern Approach", "Stuart Russell, Peter Norvig", "Computer Science", "Pearson", 2020, 4, 4),
        ("9780078022159", "Database System Concepts (7th Edition)", "Abraham Silberschatz, Henry F. Korth", "Computer Science", "McGraw-Hill", 2019, 5, 5),

        # Management, Quality & Operations
        ("9780071629737", "Juran's Quality Handbook: The Complete Guide to Performance Excellence", "Joseph M. Juran, Joseph A. De Feo", "Management & Quality", "McGraw-Hill", 2010, 3, 3),
        ("9780071392310", "The Toyota Way: 14 Management Principles", "Jeffrey K. Liker", "Management & Quality", "McGraw-Hill", 2004, 4, 4),
        ("9789332534452", "Total Quality Management (4th Edition)", "Dale H. Besterfield", "Management & Quality", "Pearson India", 2014, 6, 6),
        ("9780071441193", "The Lean Six Sigma Pocket Toolbook", "Michael L. George, John Maxey", "Management & Quality", "McGraw-Hill", 2004, 5, 5),
        ("9781260565874", "Operations Management (14th Edition)", "William J. Stevenson", "Management & Quality", "McGraw-Hill", 2021, 4, 4),
        ("9781119385974", "Project Management: A Systems Approach", "Harold Kerzner", "Management & Quality", "Wiley", 2017, 3, 3),

        # Mathematics, Data Science & Statistics
        ("9780387842929", "The Elements of Statistical Learning", "Trevor Hastie, Robert Tibshirani", "Data Science", "Springer", 2009, 4, 4),
        ("9780262035612", "Deep Learning", "Ian Goodfellow, Yoshua Bengio, Aaron Courville", "Data Science", "MIT Press", 2016, 4, 4),
        ("9781098104030", "Python for Data Analysis (3rd Edition)", "Wes McKinney", "Data Science", "O'Reilly", 2022, 5, 5),
        ("9780073383095", "Discrete Mathematics and Its Applications", "Kenneth H. Rosen", "Mathematics", "McGraw-Hill", 2019, 5, 5),

        # General Science, Humanities & Literature
        ("9780553380163", "A Brief History of Time", "Stephen Hawking", "General Science", "Bantam", 1998, 4, 4),
        ("9780062316097", "Sapiens: A Brief History of Humankind", "Yuval Noah Harari", "Humanities", "Harper", 2015, 6, 6),
        ("9780061120084", "To Kill a Mockingbird", "Harper Lee", "Literature", "Harper Perennial", 2006, 5, 5),
        ("9780451524935", "1984", "George Orwell", "Literature", "Signet Classic", 1950, 6, 6),
        ("9780374533557", "Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", "Farrar, Straus and Giroux", 2011, 4, 4),
    ]

    for b in books:
        con.execute("""INSERT INTO books
            (isbn, title, author, category, publisher, year, quantity, available_quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(isbn) DO UPDATE SET
            title=excluded.title, author=excluded.author, category=excluded.category,
            publisher=excluded.publisher, year=excluded.year""", b)

    # 2. Members (Students & Faculty / Teachers)
    members = [
        # Students
        ("M001", "Neha Rawat", "neha.rawat@example.edu", "9876543210", "Student"),
        ("M002", "Aarav Sharma", "aarav.sharma@example.edu", "9812345678", "Student"),
        ("M003", "Priya Patel", "priya.patel@example.edu", "9834567890", "Student"),
        ("M004", "Rohan Mehta", "rohan.mehta@example.edu", "9845678901", "Student"),
        ("M005", "Ananya Sen", "ananya.sen@example.edu", "9856789012", "Student"),
        ("M006", "Vikram Singh", "vikram.singh@example.edu", "9867890123", "Student"),
        ("M007", "Sneha Kulkarni", "sneha.k@example.edu", "9878901234", "Student"),

        # Faculty / Teachers
        ("F001", "Prof. K. Verma", "k.verma@example.edu", "9823456789", "Faculty"),
        ("F002", "Dr. Shalini Gupta", "s.gupta@example.edu", "9834567812", "Faculty"),
        ("F003", "Dr. Rajesh Nair", "r.nair@example.edu", "9845678923", "Faculty"),
        ("F004", "Prof. Amit Joshi", "a.joshi@example.edu", "9856789034", "Faculty"),
        ("F005", "Dr. M. Sundaram", "m.sundaram@example.edu", "9867890145", "Faculty"),
    ]

    for m in members:
        con.execute("""INSERT INTO members(member_code, name, email, phone, member_type)
                       VALUES(?, ?, ?, ?, ?)
                       ON CONFLICT(member_code) DO UPDATE SET
                       name=excluded.name, email=excluded.email, phone=excluded.phone, member_type=excluded.member_type""", m)

    # 3. User Accounts with explicit roles and member linkages
    users = [
        ("admin", "admin123", "Admin", None),
        ("staff", "staff123", "Staff", None),
        ("neha", "student123", "Student", "M001"),
        ("aarav", "student123", "Student", "M002"),
        ("priya", "student123", "Student", "M003"),
        ("prof_verma", "faculty123", "Faculty", "F001"),
        ("dr_gupta", "faculty123", "Faculty", "F002"),
    ]

    for u in users:
        con.execute("""INSERT INTO users(username, password, role, member_code)
                       VALUES(?, ?, ?, ?)
                       ON CONFLICT(username) DO UPDATE SET
                       password=excluded.password, role=excluded.role, member_code=excluded.member_code""", u)

    # 4. Realistic Transactions resolved dynamically via ISBN and Member Code
    today = date.today()
    tx_scenarios = [
        # (isbn, member_code, issue_date, due_date, return_date, status)
        ("9780132350884", "M001", (today - timedelta(days=5)).isoformat(), (today + timedelta(days=9)).isoformat(), None, "ISSUED"),   # Neha: Clean Code (On-time)
        ("9780262033848", "M001", (today - timedelta(days=20)).isoformat(), (today - timedelta(days=6)).isoformat(), None, "ISSUED"), # Neha: Algorithms (Overdue by 6 days -> fine demonstration!)
        ("9780071629737", "F001", (today - timedelta(days=7)).isoformat(), (today + timedelta(days=23)).isoformat(), None, "ISSUED"), # Prof. Verma: Juran Quality
        ("9781491950296", "M001", (today - timedelta(days=35)).isoformat(), (today - timedelta(days=21)).isoformat(), (today - timedelta(days=22)).isoformat(), "RETURNED"), # Neha: Fluent Python returned
        ("9780134685991", "M002", (today - timedelta(days=25)).isoformat(), (today - timedelta(days=11)).isoformat(), (today - timedelta(days=12)).isoformat(), "RETURNED"), # Aarav: Effective Java returned
        ("9780071392310", "M001", (today - timedelta(days=40)).isoformat(), (today - timedelta(days=26)).isoformat(), (today - timedelta(days=27)).isoformat(), "RETURNED"), # Neha: Toyota Way returned
    ]

    tx_count = con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    if tx_count == 0:
        for isbn, mcode, iss_d, due_d, ret_d, status in tx_scenarios:
            b_row = con.execute("SELECT id, available_quantity FROM books WHERE isbn=?", (isbn,)).fetchone()
            m_row = con.execute("SELECT id FROM members WHERE member_code=?", (mcode,)).fetchone()
            if b_row and m_row:
                con.execute("""
                    INSERT INTO transactions (book_id, member_id, issue_date, due_date, return_date, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (b_row[0], m_row[0], iss_d, due_d, ret_d, status))
                if status == "ISSUED" and b_row[1] > 0:
                    con.execute("UPDATE books SET available_quantity = available_quantity - 1 WHERE id = ?", (b_row[0],))

    con.commit()
    con.close()

if __name__ == "__main__":
    seed()
