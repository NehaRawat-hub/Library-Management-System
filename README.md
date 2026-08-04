# Library Management System — BBAT104 TQM Course Project

**Student:** Neha Rawat &nbsp;|&nbsp; **Reg. No.:** 2410302041 &nbsp;|&nbsp; **Section:** B
**Baseline System:** Library Management System
**Assigned Quality Goal:** Q11 — Improve Maintainability
**Suggested Q11 features implemented:** Modular Structure, Config Files, System Settings, Activity Logs, Code Comments

A Python + Tkinter + SQLite Library Management System built for the BBAT104
Fundamentals of TQM course project, with Total Quality Management tools
(SIPOC, CTQ tree, FMEA, Pareto, Fishbone, PDCA) applied throughout.

---

## 1. Project structure

The system is organised as small, single-purpose modules rather than one
large file, which is itself the core evidence for the assigned **Q11 —
Improve Maintainability** goal.

```
├── main.py                  # tiny entry point — only starts the app
├── requirements.txt
├── config/                  # Q11: centralized configuration & system settings
│   ├── config.py            #   paths + load_settings()/save_settings()
│   └── settings.json        #   editable system settings (no code changes needed)
├── database/
│   ├── database.py          # schema + connect()/initialize()
│   └── seed_data.py         # demo data for the live walkthrough
├── services/                # business logic, no UI code
│   ├── book_service.py
│   ├── member_service.py
│   ├── issue_service.py
│   └── report_service.py
├── screens/                 # one file per UI screen (Q11: modular structure)
│   ├── app_shell.py         #   Tk root window, header/nav bar, shared layout helpers
│   ├── dashboard_screen.py
│   ├── books_screen.py
│   ├── members_screen.py
│   ├── transactions_screen.py
│   ├── quality_screen.py
│   └── logs_screen.py
├── utils/                   # cross-cutting concerns
│   ├── validators.py        # Poka-Yoke input validation
│   ├── logger.py             # activity/audit + error logging
│   └── error_handler.py
├── tests/
│   └── test_validation.py
├── docs/                    # SRS, CTQ tree, SIPOC, FMEA, user manual, etc.
├── atqm/                    # applied TQM evidence: PDCA log, Pareto/Fishbone, checksheets
└── reference_material/      # the course's own guideline docs, kept for the record
```

**Why this shape?** Every screen only needs to know how to draw itself and
call into `services/`; every service only needs to know how to talk to
`database/`. Adding a 7th screen, or swapping SQLite for another database,
touches one file at a time instead of a single monolith — the direct,
demonstrable outcome of the Q11 quality goal.

## 2. Running the app

```bash
pip install -r requirements.txt
python main.py
```

Demo credentials seeded into the `users` table (login screen not wired up
in this build — the session is fixed to `admin` for the live demo):
- `admin` / `admin123`
- `staff` / `staff123`

## 3. Q11 — Improve Maintainability: evidence map

| Suggested feature | Where it lives |
|---|---|
| Modular structure | `services/`, `screens/`, `utils/`, `database/`, `config/` — each with one responsibility |
| Config files | `config/config.py`, `config/settings.json` |
| System settings | `config.load_settings()` / `save_settings()`, backed by `settings.json` |
| Activity logs | `utils/logger.py` → `activity_logs` table + `logs/activity.log`, viewable on the **Audit Logs** screen |
| Code comments / docstrings | Module-level docstrings in every file explaining its single responsibility |

## 4. TQM tool evidence (for the 4 reviews + viva)

| Review | Artefacts | Location |
|---|---|---|
| Review 1 — Setup & SRS | System architecture, SRS, CTQ tree | `docs/system_architecture.md`, `docs/SRS.md`, `docs/CTQ_tree.md` |
| Review 2 — Base CRUD + Q11 features | Working CRUD screens + Q11 evidence above | `screens/`, `services/`, section 3 above |
| Review 3 — FMEA & risk audit | SIPOC diagram, FMEA matrix with RPN | `docs/SIPOC.md`, `docs/FMEA.md`, `atqm/FMEA.md` |
| Review 4 — SQC & continuous improvement | Checksheet, Pareto chart, Fishbone diagram, PDCA log | `atqm/checksheet.md`, `atqm/pareto_analysis.py`, `atqm/fishbone_analysis.md`, `atqm/PDCA_log.md` |
| Documentation & GitHub health | This README, `docs/user_manual.md`, full commit history | repo root, `docs/`, `git log` |

## 5. Important notes

- This is a local academic/demo system. Change the demo credentials before
  any real deployment.
- Quality statistics shown on the **Quality Monitor** screen are computed
  live from actual application data (`services/report_service.py`) — no
  fabricated numbers, in line with the "Fact-Based Decision Making" TQM
  principle.
- `library.db`, `logs/*.log` and `__pycache__/` are intentionally untracked
  (see `.gitignore`) since they are generated at runtime, not source.
- `CONTEXT_HANDOFF.md` at the repo root captures the full project context
  (assignment details, decisions made, and what's left to do) so the work
  can be picked up in a new chat or handed to a different AI assistant
  without losing continuity.
