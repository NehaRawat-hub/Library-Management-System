# Q11 Maintainability Evidence — BBAT104 TQM Course Project

**Student:** Neha Rawat &nbsp;|&nbsp; **Reg. No.:** 2410302041 &nbsp;|&nbsp; **Section:** B  
**Baseline System:** Library Management System  
**Assigned Quality Goal:** Q11 — Improve Maintainability  
**Requirement:** Implement and provide verifiable engineering evidence for 5 maintainability features.  

---

## 1. Executive Summary & Maintainability Scorecard

In software engineering and Total Quality Management (TQM), **maintainability** represents the ease with which a software system can be modified to correct defects, adapt to environmental changes, incorporate new user capabilities, and improve performance (ISO/IEC 25010).

All **5 assigned Q11 features** have been engineered, verified, and integrated into the repository:

| Feature # | Feature Name | Primary Implementation Location | Status | Verifiable Evidence |
|:---:|:---|:---|:---:|:---|
| **1** | **Modular Structure** | `screens/`, `services/`, `database/`, `config/`, `utils/` | **Verified** | Strict 5-tier separation; 11 standalone screen modules; zero UI code in business logic. |
| **2** | **Config Files** | `config/config.py`, `config/settings.json` | **Verified** | Externalized JSON file; environment paths and default fallback dictionaries. |
| **3** | **System Settings** | `screens/settings_screen.py`, `system_settings` table | **Verified** | Live runtime administrative UI to update loan duration, fines, and UI themes without code restarts. |
| **4** | **Activity Logs** | `utils/logger.py`, `screens/logs_screen.py`, `audit_logs` | **Verified** | Comprehensive event stream logging user, timestamp, module, action, and status; CSV export supported. |
| **5** | **Code Comments & Docstrings** | Entire codebase (`.py` files), `tests/` | **Verified** | Standardized Google/Sphinx docstrings, type annotations, and module contract documentation. |

---

## 2. Feature 1: Modular Structure (Cohesion & Coupling Evidence)

### Architecture Layers
1. **Presentation / UI Layer (`screens/`)**:
   - Organized as 11 distinct, single-purpose screens: [`app_shell.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/app_shell.py), [`dashboard_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/dashboard_screen.py), [`student_portal_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/student_portal_screen.py), [`books_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/books_screen.py), [`members_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/members_screen.py), [`transactions_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/transactions_screen.py), [`quality_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/quality_screen.py), [`logs_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/logs_screen.py), [`settings_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/settings_screen.py), and [`login_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/login_screen.py).
   - Every screen satisfies the uniform rendering contract: `render(app) -> None`.
   - Modifying a single screen's layout or controls never breaks other screens.
2. **Business Services Layer (`services/`)**:
   - [`book_service.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/services/book_service.py), [`member_service.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/services/member_service.py), [`issue_service.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/services/issue_service.py), [`report_service.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/services/report_service.py).
   - Completely free of Tkinter or GUI widgets. Services can be run headless, tested via CLI, or reused in an API backend.
3. **Data Persistence Layer (`database/`)**:
   - Schema creation, foreign key enforcement (`PRAGMA foreign_keys = ON`), automated database migrations, and demographic seed data.
4. **Cross-Cutting Utilities (`utils/`)**:
   - Poka-Yoke input validators, centralized logging, and exception management.

---

## 3. Feature 2: Centralized Config Files

- Configuration file: [`config/settings.json`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/config/settings.json)
- Config manager: [`config/config.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/config/config.py)
- **Maintainability Value:**
  - Hardcoded magic numbers (such as default 14-day loan duration, ₹5.00 daily fine, date formats) are extracted from source code into external JSON.
  - If `settings.json` is deleted or corrupted, [`config/config.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/config/config.py) gracefully recreates it using safe fallback defaults.

---

## 4. Feature 3: Runtime System Settings

- UI Module: [`screens/settings_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/settings_screen.py)
- Database Table: `system_settings`
- **Maintainability Value:**
  - Administrators can adjust institutional policies (e.g., extend loan periods during exams, update late fines) directly through the graphical user interface.
  - Changes persist immediately to both `settings.json` and SQLite, allowing real-time reconfiguration without system redeployment or server restarts.

---

## 5. Feature 4: Centralized Activity & Audit Logs

- Logging utilities: [`utils/logger.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/utils/logger.py)
- Telemetry viewer: [`screens/logs_screen.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/screens/logs_screen.py)
- **Maintainability Value:**
  - 100% traceability for all critical operations (`BOOK_ADDED`, `BOOK_DELETED`, `BOOK_ISSUED`, `BOOK_RETURNED`, `USER_LOGIN`, `SYSTEM_SETTINGS_UPDATED`).
  - Dual recording: Written structured to SQLite (`audit_logs` table) and appended to flat file logs (`logs/activity.log`).
  - Built-in CSV export for external reporting and quality audits.

---

## 6. Feature 5: Code Comments & Maintainability Standards

- Explanatory docstrings at the top of every module specifying responsibility, exports, and dependencies.
- Clear inline comments explaining Poka-Yoke error prevention rules and foreign-key constraints.
- Automated code metrics audit executed via [`atqm/quality_monitor.py`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/atqm/quality_monitor.py) confirming clean module sizing and separation of concerns.

---

## 7. Automated Test Suite Verification

18 comprehensive unit tests located in [`tests/`](file:///c:/Users/Jaya%20Rawat/Downloads/Neha_Rawat_Library_Management_TQM/tests/):
```powershell
python -m unittest discover tests
```
- `test_validation.py`: 12 test assertions validating Poka-Yoke controls (ISBN, title, author, negative quantities, email regex).
- `test_services.py`: 4 end-to-end integration tests validating stock decrement, stock restoration, and duplicate-return prevention.
- `test_config.py`: 2 test assertions validating default generation and persistence round-trips.
