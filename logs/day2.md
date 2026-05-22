## Day 2 Log — Lekhak

### Completed
- Created Marathi wordlist (data/marathi_wordlist.txt)
- Built rule-based spell checker (src/rules/spell_checker.py)
  - Unicode NFC normalization for Devanagari
  - Wordlist-based detection
  - difflib suggestions
- Built rule-based grammar checker (src/rules/grammar_checker.py)
  - Double space detection
  - Danda vs period check
  - Repeated word detection
  - Sentence start capitalization
- Built FastAPI app (src/api/main.py)
  - GET / and GET /health
  - POST /check with full proofreading response
  - Pydantic v2 compliant
  - CORS enabled
- 15/15 pytest tests passing, 0 warnings
- API tested via Swagger UI at /docs
- Fixed VS Code interpreter (3.12 -> 3.11.9 venv)

### Key Learning
- Wordlist only covers base forms, not inflections (घर vs घरी)
- Marathi morphology problem confirmed — ML layer needed in future
- Rule-based engine is solid foundation for IndicBERT layer

### Day 3 Focus
- Build Gradio frontend UI
- Connect Gradio to FastAPI backend
- Begin exploring IndicBERT

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
│       marathi_wordlist.txt
├───frontend
├───logs
│       day1.md
│       day2.md
├───models
├───notebooks
├───tests
│       __init__.py
│       test_api.py
│       test_spell_checker.py
│       test_grammar_checker.py
└───src
    │   __init__.py
    ├───api
    │       __init__.py
    │       main.py
    ├───rules
    │       __init__.py
    │       spell_checker.py
    │       grammar_checker.py
    └───utils
            __init__.py
```
