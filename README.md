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
- Railway live for API deployment
- HuggingFace Spaces and Vercel planned for later deployment paths

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

## Day 4 Status

Completed:

- Expanded the Marathi wordlist to 626 words.
- Added wordlist builder scripts:
  - `scripts/build_wordlist.py`
  - `scripts/topup_wordlist.py`
- Added 4 new grammar rules:
  - missing question mark detection
  - multiple punctuation detection
  - space before danda detection
  - mixed Devanagari/English spacing detection
- Increased grammar coverage from 4 rules to 8 rules.
- Expanded the test suite from 15 tests to 21 tests.
- Created `src/rules/muril_ranker.py` for Layer 2 contextual ranking.
- Upgraded `/suggest` to support:
  - default edit-distance ranking
  - optional MuRIL ranking with `ml_ranking=true`
  - required sentence context for ML ranking
  - `ranking_mode` in the API response
- Created a Railway `Procfile`.
- Replaced `pip freeze` output with a curated Railway-safe `requirements.txt`.
- Deployed the API to Railway.

Key ML/API behavior:

- Default `/suggest` behavior remains lightweight edit-distance ranking.
- MuRIL ranking is available locally through `ml_ranking=true`.
- MuRIL requires a `sentence` field because contextual ranking is impossible without context.
- If `ml_ranking=true` is sent without a sentence, the API returns a `400` error.

Deployment result:

- Railway API is live at `https://web-production-9e1c4.up.railway.app`.
- `/health` validated successfully.
- `/check` validated successfully on the live deployment.
- MuRIL is intentionally not relied on for Railway production because the model is large and better suited to HuggingFace Spaces or a larger deployment target.

Latest verified test result:

- `21 passed in 0.56s`

Architecture decisions:

- Curated `requirements.txt` is required for deployment.
- Do not use `pip freeze > requirements.txt` for Railway because it captures Windows-only and development packages.
- MuRIL remains a local Layer 2 ranker for now.
- Railway production deployment currently prioritizes the stable rule engine.
- PowerShell API tests with Marathi text should use explicit UTF-8 byte bodies.

## Current Project Structure

```text
C:\Users\Kshitij\lekhak\
|-- data\
|   `-- marathi_wordlist.txt
|-- frontend\
|   `-- app.py
|-- logs\
|   |-- day1.md
|   |-- day2.md
|   |-- day3.md
|   `-- day4.md
|-- models\
|-- notebooks\
|   `-- indicbert_explore.ipynb
|-- scripts\
|   |-- build_wordlist.py
|   |-- topup_wordlist.py
|   |-- update_main.py
|   |-- write_grammar_checker.py
|   |-- write_grammar_tests.py
|   |-- write_muril_ranker.py
|   |-- write_procfile.py
|   |-- write_requirements.py
|   `-- test_suggest.py
|-- tests\
|   |-- test_api.py
|   |-- test_spell_checker.py
|   |-- test_grammar_checker.py
|   `-- test_suggest.py
|-- Procfile
|-- README.md
|-- requirements.txt
`-- src\
    |-- api\
    |   `-- main.py
    |-- rules\
    |   |-- spell_checker.py
    |   |-- grammar_checker.py
    |   |-- suggester.py
    |   `-- muril_ranker.py
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
.\venv\Scripts\python.exe -m pytest tests/ -v
```

Test live API:

```powershell
Invoke-RestMethod -Uri "https://web-production-9e1c4.up.railway.app/health"
```

For Marathi JSON bodies in PowerShell, send UTF-8 bytes:

```powershell
$body = [System.Text.Encoding]::UTF8.GetBytes('{"text": "मी शाळेत जातो।"}')
Invoke-RestMethod -Uri "https://web-production-9e1c4.up.railway.app/check" -Method POST -ContentType "application/json; charset=utf-8" -Body $body
```

## Day 5 Next Goals

- Update Gradio frontend to support local vs Railway backend.
- Return spelling suggestions inline in `/check` results.
- Add character offsets and word indexes for frontend highlighting.
- Add Marathi morphological suffix handling to reduce false positives.
- Explore HuggingFace Spaces deployment for Gradio and MuRIL-friendly hosting.
