"""
main.py
--------
Single, tiny entry point for the Library Management System.
All real logic lives in dedicated packages:

    config/    -> settings & paths
    database/  -> schema + connection
    services/  -> business logic (books, members, issues, reports)
    utils/     -> validation, logging, error handling
    screens/   -> one file per UI screen + the app shell

This file's only job is to start the application.
"""

from screens.app_shell import LibraryApp

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
