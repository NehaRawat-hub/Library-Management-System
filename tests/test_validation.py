from utils.validators import validate_book, validate_member

def test_book_required():
    ok, _ = validate_book("", "Title", "Author", "Cat", "1")
    assert not ok

def test_book_quantity():
    ok, _ = validate_book("1", "Title", "Author", "Cat", "0")
    assert not ok

def test_member_email():
    ok, _ = validate_member("M1", "Name", "bad-email")
    assert not ok
