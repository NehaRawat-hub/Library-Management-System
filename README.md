# Library Management System — BBAT104 TQM Course Project

**Student:** Neha Rawat &nbsp;|&nbsp; **Reg. No.:** 2410302041 &nbsp;|&nbsp; **Section:** B  
**Course:** BBAT104 — Fundamentals of TQM, Academic Session 2026–27  
**Baseline System:** Library Management System  
**Assigned Quality Goal:** Q11 — Improve Maintainability  
**Suggested Q11 Features Implemented:** Modular Structure, Config Files, System Settings, Activity Logs, Code Comments  

---

## 1. Overview & Modern Architecture

A Python 3 + Tkinter + SQLite desktop Library Management System built with a strict layered architecture (UI screens, business services, database persistence, centralized configuration, and utility cross-cutting concerns).

### Key Highlights
- **Role-Based Portals**:
  - **Admin / Staff**: Full circulation desk, book catalog management, member directory, audit logs, system settings, and analytics.
  - **Student / Faculty Self-Service Portal**: Personal borrowing dashboard, active loans with due-date countdowns and automatic fine calculation, library catalog live search, and borrowing history.
- **Modern User Experience**:
  - **Vertical Sidebar Navigation**: Sleek enterprise-style sidebar on the left with active tab highlighting and role badges.
  - **Dark / Light Mode**: Instant one-click toggle with persistent user preference storage in `config/settings.json`.
  - **Clean Presentation**: Dedicated to real-world library operations without cluttering end-user screens with internal course rubric tags.
- **Robust Engineering & TQM Controls**:
  - **Poka-Yoke Input Validation** at every form layer to prevent invalid entries.
  - **Comprehensive Audit Trail** recording user, timestamp, module, and action attribution.
  - **Dual-Persisted System Settings** (JSON + SQLite) allowing zero-downtime reconfiguration of loan durations, overdue fines, and quotas.

---

## 2. Repository Structure

```
├── main.py                     # Single entry point: boots LibraryApp shell
├── requirements.txt
├── .gitignore
├── README.md
├── CONTEXT_HANDOFF.md
├── config/                     # Q11: Centralized configuration layer
│   ├── config.py               #   Settings loader, paths & defaults
│   └── settings.json           #   Editable runtime system settings (JSON)
├── database/                   # Q11: Persistence layer
│   ├── database.py             #   Schema, foreign-key enforcement & migrations
│   └── seed_data.py            #   26+ books, 12 members (students & faculty), loans
├── services/                   # Business logic layer (No UI code)
│   ├── book_service.py         #   CRUD + multi-field catalog search
│   ├── member_service.py       #   Member registration & directory queries
│   ├── issue_service.py        #   Issue, return, availability & duplicate check
│   └── report_service.py       #   Live operational statistics & telemetry
├── screens/                    # Q11: Modular UI layer (One file per screen)
│   ├── __init__.py             #   render(app) contract definition
│   ├── app_shell.py            #   Sidebar navigation, Dark/Light mode & chrome
│   ├── dashboard_screen.py     #   KPI metrics, quick operations, circulation feed
│   ├── student_portal_screen.py#   Student/Faculty self-service portal
│   ├── books_screen.py         #   Book catalog, search, add, delete
│   ├── members_screen.py       #   Student & faculty membership directory
│   ├── transactions_screen.py  #   Issue & return circulation desk
│   ├── quality_screen.py       #   Analytics & system health telemetry
│   ├── logs_screen.py          #   Audit trail & exception logs with CSV export
│   ├── settings_screen.py      #   System settings & circulation policy UI
│   └── login_screen.py         #   Role-based sign in & profile switcher
├── utils/                      # Cross-cutting utilities
│   ├── validators.py           #   Poka-Yoke error prevention validators
│   ├── logger.py               #   Activity & error logging to DB and file
│   └── error_handler.py        #   Centralized exception handling
├── tests/                      # Automated test suite (18 unit tests)
│   ├── test_validation.py      #   Poka-Yoke validator assertions
│   ├── test_services.py        #   Isolated business logic & stock tests
│   └── test_config.py          #   Settings persistence & defaults tests
├── atqm/                       # Applied TQM evidence for Reviews 3 & 4
│   ├── pareto_analysis.py      #   Statistical Quality Control 80/20 script
│   ├── pareto_chart.png        #   Generated Pareto defect frequency chart
│   ├── quality_monitor.py      #   Automated metrics & architecture auditor
│   ├── quality_report.txt      #   Generated quality report
│   └── FMEA.md, checksheet.md, PDCA_log.md, SIPOC.md, etc.
└── reference_material/         # Official course allotment and guidelines
```

---

## 3. Getting Started

### Prerequisites
- Python 3.10+
- Tkinter (included with standard Python on Windows/macOS)

### Installation & Execution
```bash
# Clone or navigate to the repository directory
cd Neha_Rawat_Library_Management_TQM

# Install optional dependencies
pip install -r requirements.txt

# Launch the Library Management System
python main.py
```

### Running Automated Tests
```bash
python -m unittest discover tests
```
*All 18 unit tests run in <0.3s against isolated in-memory/temporary test stores.*

---

## 4. Default Seed Accounts for Testing & Viva

| Role | Username | Password | Member Code | Linked Identity |
|:---|:---|:---|:---|:---|
| **Administrator** | `admin` | `admin123` | *N/A* | Full system access & settings |
| **Staff / Librarian** | `staff` | `staff123` | *N/A* | Circulation desk & inventory |
| **Student** | `neha` | `student123` | `M001` | Neha Rawat (Student Portal) |
| **Student** | `aarav` | `student123` | `M002` | Aarav Sharma (Student Portal) |
| **Student** | `priya` | `student123` | `M003` | Priya Patel (Student Portal) |
| **Faculty** | `prof_verma`| `faculty123` | `F001` | Prof. K. Verma (Faculty Portal)|
| **Faculty** | `dr_gupta`  | `faculty123` | `F002` | Dr. Shalini Gupta (Faculty Portal)|

*(The login screen also provides a **Student & Faculty Direct Access** dropdown for instant, one-click profile switching during live evaluation.)*

---

## 5. Statistical Quality Control (SQC) Tools

To generate or refresh the Pareto 80/20 chart and quality telemetry report:
```bash
# Generate Pareto Chart (saved to atqm/pareto_chart.png)
python atqm/pareto_analysis.py

# Generate Maintainability & Quality Report (saved to atqm/quality_report.txt)
python atqm/quality_monitor.py
```
