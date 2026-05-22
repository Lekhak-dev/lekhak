# Lekhak — Day 4 Log

Date: 22-05-2026

---

## Work Completed

### 1. Wordlist Expansion

- Created `scripts/build_wordlist.py` to write the canonical Marathi wordlist safely with UTF-8.
- Created `scripts/topup_wordlist.py` to append additional words without duplicates.
- Expanded the wordlist to 626 words.
- Added categories such as verb inflections, noun case forms, postpositions, adjective forms, days, months, body parts, food, education, work, and nature.

### 2. Grammar Rule Expansion

Added 4 new grammar rules:

- `check_question_mark()` detects question words without a trailing `?`.
- `check_multiple_punctuation()` detects repeated punctuation such as `।।`, `??`, `!!`, and `..`.
- `check_space_before_danda()` detects a space before the Marathi danda.
- `check_mixed_script_spacing()` detects Devanagari and ASCII text touching without a space.

Total grammar rules after Day 4: 8.

### 3. Test Suite Expansion

- Added 6 new grammar tests through `scripts/write_grammar_tests.py`.
- Test count increased from 15 to 21.
- Latest verified result: `21 passed in 0.56s`.

### 4. MuRIL Layer 2 Integration

- Created `src/rules/muril_ranker.py`.
- Implemented `rank_candidates_by_context(word, sentence, candidates)`.
- MuRIL is lazy-loaded only on the first ML-ranking request.
- Candidate scoring flow:
  - take Layer 1 edit-distance candidates
  - substitute each candidate into the sentence
  - generate MuRIL embeddings
  - compute cosine similarity
  - sort candidates by `ml_score`

Validated behavior:

- Edit-distance mode for `घरि` returned `घर` and `घरी`.
- MuRIL mode for sentence `मी घरि जातो` returned scores:
  - `घर`: `0.998436`
  - `घरी`: `0.997483`
- In this context, `घर` ranking higher is reasonable because `मी घर जातो` is closer to the intended sentence structure than `मी घरी जातो`.

### 5. `/suggest` Endpoint Upgrade

Updated `src/api/main.py`:

- `SuggestRequest` now supports:
  - `word`
  - optional `sentence`
  - `ml_ranking`
- `SuggestResponse` now includes `ranking_mode`.
- `ml_ranking=false` uses edit-distance ranking.
- `ml_ranking=true` uses MuRIL contextual ranking and requires `sentence`.
- If `ml_ranking=true` is sent without a sentence, the API returns `400`.

Confirmed cases:

- Edit-distance mode works.
- MuRIL mode works locally.
- Missing sentence correctly returns `400`.

### 6. Railway Deployment

- Created `Procfile`.
- Created curated `requirements.txt`.
- First Railway deploy failed because `pip freeze` included `pywinpty`, a Windows-only package.
- Created `scripts/write_requirements.py` to write a clean Railway-safe dependency list.
- Railway deployment succeeded after removing Windows-only and development packages.

Live API:

- `https://web-production-9e1c4.up.railway.app`

Validated live endpoints:

- `/health`
- `/`
- `/check`

---

## Key Findings

### PowerShell Encoding

- PowerShell can display Marathi text as mojibake even when the underlying API behavior is correct.
- Direct `-Body '{"text": "मराठी"}'` is unsafe for API tests.
- Use explicit UTF-8 bytes:

```powershell
$body = [System.Text.Encoding]::UTF8.GetBytes('{"text": "मी शाळेत जातो।"}')
Invoke-RestMethod -Uri "https://web-production-9e1c4.up.railway.app/check" -Method POST -ContentType "application/json; charset=utf-8" -Body $body
```

### Deployment Requirements

- Do not use `pip freeze > requirements.txt` for deployment.
- `pip freeze` captures local Windows and notebook dependencies that do not belong on Railway.
- Keep `requirements.txt` curated and production-focused.

### MuRIL Hosting

- MuRIL is large and not ideal for Railway free-tier deployment.
- MuRIL remains local-only for now.
- HuggingFace Spaces is the better future target for ML-heavy Gradio/MuRIL deployment.

---

## Architecture Decisions

| Decision | Reason |
|----------|--------|
| Wordlist expanded to 626 words | Better MVP coverage while preserving rule-engine simplicity |
| Grammar rules expanded to 8 | Better punctuation and mixed-script coverage |
| MuRIL used as ranker, not detector | Model is robust to minor misspellings and better suited for contextual ranking |
| `/suggest` requires sentence for ML ranking | Contextual ranking needs sentence context |
| `ranking_mode` added to response | Frontend needs to know whether ranking was edit-distance or MuRIL |
| Curated `requirements.txt` | Railway deploys Linux; local Windows/dev packages caused build failure |
| MuRIL local-only for now | Railway memory/startup constraints make full ML deployment risky |

---

## Bugs Fixed

| Bug | Root Cause | Fix |
|-----|------------|-----|
| New grammar checker was not active | File update did not land correctly | Wrote file through a Python script |
| PowerShell `curl -H` failed | `curl` maps to `Invoke-WebRequest` in PowerShell | Used `Invoke-RestMethod` |
| Devanagari request body was garbled | PowerShell body encoding issue | Used `UTF8.GetBytes()` |
| Railway build failed on `pywinpty` | `pip freeze` captured Windows-only package | Replaced with curated requirements |
| Procfile command lost `$PORT` | PowerShell interpreted `$PORT` | Wrote Procfile through Python |

---

## Test Results

```text
21 passed in 0.56s
```

No regressions after Day 4 changes.

---

## Pending for Day 5

- Update `frontend/app.py` to support local vs Railway backend.
- Return suggestions inline from `/check`.
- Add character offsets and word indexes to spelling errors.
- Add Marathi suffix handling for common inflections.
- Explore HuggingFace Spaces for Gradio and MuRIL-friendly deployment.

---

## Commands Reference

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

Test live health endpoint:

```powershell
Invoke-RestMethod -Uri "https://web-production-9e1c4.up.railway.app/health"
```

Git:

```powershell
git add .
git commit -m "message"
git push origin main
```

---

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
|   |-- test_suggest.py
|   |-- topup_wordlist.py
|   |-- update_main.py
|   |-- write_grammar_checker.py
|   |-- write_grammar_tests.py
|   |-- write_muril_ranker.py
|   |-- write_procfile.py
|   |-- write_requirements.py
|   `-- write_test_suggest.py
|-- tests\
|   |-- test_api.py
|   |-- test_grammar_checker.py
|   |-- test_spell_checker.py
|   `-- test_suggest.py
|-- Procfile
|-- README.md
|-- requirements.txt
`-- src\
    |-- api\
    |   `-- main.py
    |-- rules\
    |   |-- grammar_checker.py
    |   |-- muril_ranker.py
    |   |-- spell_checker.py
    |   `-- suggester.py
    `-- utils\
```
