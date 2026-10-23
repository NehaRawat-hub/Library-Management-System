"""
tests/test_services.py
----------------------
Unit and integration tests for business logic services:
  - BookService: Add, Query, Delete
  - MemberService: Add, Query
  - IssueService: Issue with stock decrement, stock availability check,
                  return with stock increment, duplicate-return prevention.
"""

import unittest
import tempfile
import sqlite3
import gc
from pathlib import Path
from unittest.mock import patch

from database.database import SCHEMA
import config.config as cfg
from services.book_service import BookService
from services.member_service import MemberService
from services.issue_service import IssueService


class TestServices(unittest.TestCase):

    def setUp(self):
        # Create an isolated temporary directory ignoring Windows file lock cleanup errors
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.test_db_path = Path(self.temp_dir.name) / "test_library.db"

        # Apply schema to test DB
        con = sqlite3.connect(self.test_db_path)
        con.executescript(SCHEMA)
        con.commit()
        con.close()

        # Patch DB_PATH in config and database modules
        self.patcher1 = patch("config.config.DB_PATH", self.test_db_path)
        self.patcher2 = patch("database.database.DB_PATH", self.test_db_path)
        self.patcher1.start()
        self.patcher2.start()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        gc.collect()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_book_service_add_and_all(self):
        bs = BookService()
        bid = bs.add("TEST-ISBN-001", "Design Patterns", "GoF", "CS", "Addison", 1994, 3)
        self.assertIsNotNone(bid)

        books = bs.all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0][1], "TEST-ISBN-001")
        self.assertEqual(books[0][2], "Design Patterns")

        # Search test
        search_results = bs.all("Patterns")
        self.assertEqual(len(search_results), 1)
        no_results = bs.all("NonExistent")
        self.assertEqual(len(no_results), 0)

    def test_book_service_delete(self):
        bs = BookService()
        bid = bs.add("TEST-ISBN-002", "Refactoring", "Fowler", "CS", "Addison", 1999, 2)
        self.assertEqual(len(bs.all()), 1)

        bs.delete(bid)
        self.assertEqual(len(bs.all()), 0)

    def test_member_service_add_and_search(self):
        ms = MemberService()
        mid = ms.add("MEM-001", "Alice Student", "alice@example.com", "9876543210")
        self.assertIsNotNone(mid)

        members = ms.all()
        self.assertEqual(len(members), 1)
        self.assertEqual(members[0][1], "MEM-001")

        search_res = ms.all("Alice")
        self.assertEqual(len(search_res), 1)

    def test_issue_service_workflow(self):
        bs = BookService()
        ms = MemberService()
        iss = IssueService()

        # 1. Setup book with quantity 1
        bid = bs.add("ISBN-WORKFLOW", "TQM Handbook", "Juran", "Quality", "McGraw", 2010, 1)
        mid = ms.add("MEM-WORKFLOW", "Bob Tester", "bob@example.com", "9123456780")

        # 2. Issue book
        tx_id = iss.issue(bid, mid)
        self.assertIsNotNone(tx_id)

        # Check stock decremented to 0
        book_row = bs.all()[0]
        self.assertEqual(book_row[8], 0)  # available_quantity

        # Check active transactions
        active_txs = iss.active()
        self.assertEqual(len(active_txs), 1)
        self.assertEqual(active_txs[0][0], tx_id)

        # 3. Prevent issuing unavailable book (stock = 0)
        with self.assertRaises(ValueError) as ctx:
            iss.issue(bid, mid)
        self.assertIn("unavailable", str(ctx.exception).lower())

        # 4. Return book
        iss.return_book(tx_id)

        # Check stock incremented back to 1
        book_row_after = bs.all()[0]
        self.assertEqual(book_row_after[8], 1)

        # Check no active transactions
        self.assertEqual(len(iss.active()), 0)

        # 5. Prevent duplicate return
        with self.assertRaises(ValueError) as ctx2:
            iss.return_book(tx_id)
        self.assertIn("already been returned", str(ctx2.exception).lower())


if __name__ == "__main__":
    unittest.main()
