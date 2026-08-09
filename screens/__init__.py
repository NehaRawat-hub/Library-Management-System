"""
screens package
----------------
Every screen (view) of the Library Management System lives in its own
module in this package. This is part of the Q11 "Improve Maintainability"
quality goal: instead of one large UI file, each screen is a small,
independently readable/testable unit that only knows how to render itself
using the shared services layer.

Each screen module exposes a single public function:

    render(app) -> None

`app` is the running LibraryApp (screens/app_shell.py) instance. Screens
use the shared helpers on `app` (app.base(), app.table(), app.username,
app.role, ...) so there is one consistent look and feel across the system.
"""
