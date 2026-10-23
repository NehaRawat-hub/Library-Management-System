"""
tests/test_validation.py
------------------------
Unit tests for Poka-Yoke input validators (utils/validators.py).
Ensures input mistakes are caught before database writes.
"""

import unittest
from utils.validators import validate_book, validate_member, valid_email


class TestValidation(unittest.TestCase):

    def test_book_valid(self):
        ok, msg = validate_book("9780132350884", "Clean Code", "Robert C. Martin", "Programming", "5")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_book_missing_isbn(self):
        ok, msg = validate_book("", "Title", "Author", "Cat", "1")
        self.assertFalse(ok)
        self.assertIn("required", msg.lower())

    def test_book_missing_title(self):
        ok, msg = validate_book("123456", "", "Author", "Cat", "1")
        self.assertFalse(ok)
        self.assertIn("required", msg.lower())

    def test_book_missing_author(self):
        ok, msg = validate_book("123456", "Title", "", "Cat", "1")
        self.assertFalse(ok)
        self.assertIn("required", msg.lower())

    def test_book_quantity_zero(self):
        ok, msg = validate_book("123456", "Title", "Author", "Cat", "0")
        self.assertFalse(ok)
        self.assertIn("positive whole number", msg.lower())

    def test_book_quantity_negative(self):
        ok, msg = validate_book("123456", "Title", "Author", "Cat", "-3")
        self.assertFalse(ok)
        self.assertIn("positive whole number", msg.lower())

    def test_book_quantity_non_numeric(self):
        ok, msg = validate_book("123456", "Title", "Author", "Cat", "abc")
        self.assertFalse(ok)
        self.assertIn("positive whole number", msg.lower())

    def test_member_valid(self):
        ok, msg = validate_member("M001", "Neha Rawat", "neha@example.com")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_member_missing_code(self):
        ok, msg = validate_member("", "Neha Rawat", "neha@example.com")
        self.assertFalse(ok)
        self.assertIn("required", msg.lower())

    def test_member_missing_name(self):
        ok, msg = validate_member("M001", "", "neha@example.com")
        self.assertFalse(ok)
        self.assertIn("required", msg.lower())

    def test_member_bad_email(self):
        ok, msg = validate_member("M001", "Name", "invalid-email-string")
        self.assertFalse(ok)
        self.assertIn("valid email", msg.lower())

    def test_valid_email_helper(self):
        self.assertTrue(valid_email("user@example.com"))
        self.assertTrue(valid_email("first.last@dept.univ.edu"))
        self.assertFalse(valid_email("missing-at.com"))
        self.assertFalse(valid_email("missing-domain@"))
        self.assertFalse(valid_email("@no-user.com"))


if __name__ == "__main__":
    unittest.main()
