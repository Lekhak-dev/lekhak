## Day 1 Log - Lekhak

### Completed

- Full dev environment setup on Windows
- Project scaffold created
- GitHub repo live at github.com/Lekhak-dev/lekhak
- Base Python packages installed
- Virtual environment configured

### Pending (Day 2)

- Build rule-based Marathi spell checker
- Create first Marathi wordlist
- Write first FastAPI endpoint
- Test basic proofreading pipeline

### Architecture Decisions

- Using venv for environment management
- Gradio for MVP frontend before React
- SQLite for initial storage

### Day 2 Focus

Rule-based engine - the foundation before any ML

---

## Current Project Structure

```text
C:\Users\Kshitij\lekhak\
│   .env
│   .gitignore
│   README.md
│   requirements.txt
│
├───data
│
├───frontend
│
├───logs
│       day1.md
│
├───models
│
├───notebooks
│
└───src
    │   __init__.py
    │
    ├───api
    │       __init__.py
    │
    ├───rules
    │       __init__.py
    │
    └───utils
            __init__.py
```
