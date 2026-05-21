# Lekhak

AI-powered Marathi proofreading platform focused on spelling, grammar, Unicode normalization, contextual correction, and long-term Marathi writing assistance.

## Project Mission

Lekhak is being built as a production-grade Marathi proofreading platform, similar in spirit to Grammarly, but specialized for Marathi language constraints such as Devanagari Unicode handling, morphology, inflections, and context-sensitive correction.

## Current Architecture

Lekhak follows a layered architecture:

1. Layer 1: Rule-based Marathi NLP engine
   - Wordlist validation
   - Grammar rules
   - Punctuation rules
   - Unicode NFC normalization

2. Layer 2: Contextual ML ranking
   - Model selected for exploration: `google/muril-base-cased`
   - Role: rank candidate corrections by context
   - Important decision: MuRIL is a ranker, not the primary error detector

3. Layer 3: Fine-tuned correction model
   - Future sequence correction layer
   - Long-term intelligent proofreading model

## Tech Stack

- Python 3.11.9
- FastAPI
- Uvicorn
- Gradio
- PyTorch
- HuggingFace Transformers
- MuRIL
- SQLite now, PostgreSQL later
- Railway, HuggingFace Spaces, and Vercel planned for deployment paths

## Day 1 Status

Completed:

- Created GitHub, HuggingFace, Railway, and Vercel accounts.
- Installed Python 3.11.9, Git, and VS Code.
- Created the Lekhak project folder.
- Created and activated Python virtual environment.
- Installed initial dependencies.
- Configured VS Code and PowerShell workflow.
- Created base project structure:
  - `data/`
  - `frontend/`
  - `logs/`
  - `models/`
  - `notebooks/`
  - `tests/`
  - `src/api/`
  - `src/rules/`
  - `src/utils/`

Result:

- Development environment ready.
- Project structure ready for backend, frontend, rules, tests, and ML experimentation.

## Day 2 Status

Completed:

- Built the initial rule-based Marathi spell checker.
- Built the initial grammar checker.
- Implemented Unicode NFC normalization.
- Implemented Marathi tokenization.
- Built FastAPI backend.
- Created the `/check` endpoint.
- Validated Swagger UI at `/docs`.
- Added and ran test suite.
- Fixed VS Code interpreter issue.
- Fixed Uvicorn/server startup issues.

Result:

- Backend functional.
- `/check` API working.
- Rule engine validated end to end.
- Latest Day 2 test result: `15 passed`.

Architecture decisions:

- Wordlist is a scaffold only, not production-grade.
- Marathi morphology requires more than a naive wordlist.
- Rule engine is Layer 1.
- Contextual ML is mandatory for long-term quality.
- Unicode NFC normalization is required across the whole pipeline.
- Gradio is the MVP frontend before React.

## Day 3 Status

Completed:

- Created Gradio frontend at `frontend/app.py`.
- Connected frontend to FastAPI backend.
- Added UI for full text checking.
- Added UI for single-word suggestions.
- Created `src/rules/suggester.py`.
- Implemented Levenshtein edit-distance suggestions.
- Added `/suggest` endpoint.
- Added dynamic suggestion threshold:
  - Word length <= 3: max distance 1
  - Word length <= 6: max distance 2
  - Word length > 6: max distance 3
- Fixed suggestion noise for short Marathi words.
- Moved wordlist into `data/marathi_wordlist.txt`.
- Loaded wordlist once at FastAPI startup.
- Expanded the wordlist with common Marathi words and inflections.
- Explored MuRIL locally through notebook experimentation.

Key ML findings:

- `ai4bharat/indic-bert` was gated, so MuRIL was selected for practical MVP exploration.
- Model used: `google/muril-base-cased`.
- Correct word tokenization: `ghari` equivalent Marathi word stayed as one token.
- Misspelled word behavior: Marathi misspelling split into subwords.
- Correct vs misspelled sentence cosine similarity: `0.9999`.

Architecture decision confirmed:

- MuRIL should not be used as the primary detector because it is highly robust to minor spelling errors.
- Layer 1 detects possible issues.
- Layer 1 generates candidate corrections.
- Layer 2 uses MuRIL to rank candidates contextually.

Result:

- Backend working on `localhost:8000`.
- Gradio frontend working on `localhost:7860`.
- `/check` endpoint working.
- `/suggest` endpoint working.
- ML direction clarified for Day 4.

## Current Project Structure

```text
C:\Users\Kshitij\lekhak\
|-- data\
|   `-- marathi_wordlist.txt
|-- frontend\
|   `-- app.py
|-- logs\
|-- models\
|-- notebooks\
|   `-- indicbert_explore.ipynb
|-- tests\
|   |-- test_spell_checker.py
|   |-- test_grammar_checker.py
|   `-- test_suggest.py
`-- src\
    |-- api\
    |   `-- main.py
    |-- rules\
    |   |-- spell_checker.py
    |   |-- grammar_checker.py
    |   `-- suggester.py
    `-- utils\
```

## Current Commands

Start backend:

```powershell
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Start frontend:

```powershell
python frontend/app.py
```

Run tests:

```powershell
pytest tests/ -v
```

## Day 4 Next Goals

- Expand Marathi wordlist toward 500+ words.
- Add more grammar rules.
- Deploy backend to Railway.
- Implement MuRIL candidate scoring.
- Add optional ML ranking to `/suggest`.
- Compare edit-distance ranking vs MuRIL contextual ranking.
