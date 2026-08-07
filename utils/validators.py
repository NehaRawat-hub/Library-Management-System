import re

def required(*values):
    return all(str(v).strip() for v in values)

def positive_int(value):
    try:
        return int(value) > 0
    except (TypeError, ValueError):
        return False

def valid_email(value):
    if not value:
        return True
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))

def validate_book(isbn, title, author, category, quantity):
    if not required(isbn, title, author, category):
        return False, "Please fill all required book fields."
    if not positive_int(quantity):
        return False, "Quantity must be a positive whole number."
    return True, ""

def validate_member(code, name, email):
    if not required(code, name):
        return False, "Member code and name are required."
    if not valid_email(email):
        return False, "Please enter a valid email address."
    return True, ""
