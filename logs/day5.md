# Lekhak - Day 5 Log

Date: 2026-05-24

End-of-day status:

- Tests: `24 passed in 0.52s`
- API version: `0.3.0`
- Wordlist: 641 words
- Grammar rules: 7 active rules
- Railway API: `https://web-production-9e1c4.up.railway.app`

---

## Work Completed

### 1. API v0.3.0

Updated `src/api/main.py`:

- `/check` now returns inline spelling suggestions.
- `/check` now returns word index and character offset for spelling errors.
- Added `SpellingErrorDetail` response shape:
  - `word`
  - `index`
  - `char_offset`
  - `suggestions`
- Added `_find_char_offset()` helper for frontend highlighting work later.
- Kept `_wordlist` loaded once at startup and passed into `check_spelling()`.
- `/suggest` still supports edit-distance ranking and optional MuRIL ranking.
- MuRIL failures fall back to edit-distance suggestions.

Important implementation detail:

- `src.rules.suggester.get_suggestions()` returns `list[dict]` with `word` and `distance`.
- The API unwraps those dicts into `list[str]` before returning frontend-facing suggestion lists.

### 2. Spell Checker Refactor

Updated `src/rules/spell_checker.py`:

- `check_spelling(text, wordlist=None)` now accepts an optional pre-loaded wordlist.
- This avoids reading `data/marathi_wordlist.txt` from disk on every request.
- Spell checker now detects errors only.
- Suggestions are no longer produced inside `spell_checker.py`.
- Error dict now contains:
  - `word`
  - `index`
  - `message`

Architecture result:

- Detection is handled by `spell_checker.py`.
- Suggestion generation is handled by `suggester.py`.
- API composition happens in `main.py`.

### 3. Morphological Suffix Stripping

Created `src/rules/suffix_stripper.py`.

Core functions:

- `strip_suffix(word)`
- `is_valid_with_suffix(word, wordlist)`

Design:

- 40+ Marathi suffixes.
- Suffixes ordered longest-first.
- Minimum root length: 2 characters.
- Prevents false positives for common inflected forms.

Examples validated:

- `घरात` can validate through root `घर`.
- `शाळेत` can validate through root `शाळा`.
- `मुलाला` is accepted from the wordlist.
- `घरि` remains a spelling error.

Key lesson:

- Suffix stripping fixes inflected-form false positives.
- Missing root words are a separate wordlist coverage problem.
- `दे` and `आण` were failures because the root words were missing, not because suffix stripping was broken.

### 4. Wordlist Updates

Updated `data/marathi_wordlist.txt`.

Added common missing words discovered during testing, including:

- `दे`
- `घे`
- `ये`
- `जा`
- `छान`
- `नाही`
- `आज`
- `आण`

Final Day 5 wordlist count: 641 words.

### 5. Grammar Rule Update

Removed the `wrong_punctuation` / missing danda rule.

Reason:

- Period vs danda is a user preference in digital Marathi.
- The rule created too many false positives for casual users.
- It may return later as an optional "formal writing mode".

Active grammar rules after Day 5:

- double space
- repeated word
- sentence start capitalization for English text
- missing question mark
- multiple punctuation
- space before danda
- mixed-script spacing

### 6. Frontend v2

Updated `frontend/app.py`:

- Added backend toggle:
  - Local: `http://localhost:8000`
  - Production: `https://web-production-9e1c4.up.railway.app`
- Displays inline spelling suggestions from `/check`.
- Displays `char_offset` for each spelling error.
- Displays grammar messages and suggestions.
- Uses defensive `.get()` reads so it can tolerate old and new API response shapes.
- Uses `gr.themes.Soft()`.
- Uses double newlines in Markdown output so results render cleanly.

### 7. Test Suite Update

Updated tests to match API v0.3.0:

- `tests/test_api.py`
- `tests/test_spell_checker.py`
- `tests/test_grammar_checker.py`

Added coverage for:

- `/check` spelling errors with suggestions.
- spelling error `index`.
- pre-loaded wordlist support.
- `/suggest` basic response shape.

Latest result:

```text
24 passed in 0.52s
```

---

## Bugs Fixed

| Bug | Root Cause | Fix |
|-----|------------|-----|
| Frontend showed no output | Frontend process was not running / later hit schema errors | Started frontend and fixed response handling |
| `KeyError: rule` | Grammar errors use `type`, not `rule` | Frontend now reads `type` with fallback |
| `KeyError: total_words` | Railway still served older schema during local testing | Frontend uses defensive `.get()` |
| Pydantic suggestion validation failed | API expected `list[str]`, suggester returns `list[dict]` | API unwraps `s["word"]` |
| `check_spelling()` argument error | Old signature only accepted `text` | Added optional `wordlist` parameter |
| `ModuleNotFoundError: src` | Running package file directly | Use `python -m src.rules.spell_checker` |
| `मुलाला` test seemed to fail | Actual missing words were `दे` and `आण` | Added missing root words |
| Markdown output collapsed lines | Single newline collapsed in Markdown | Switched to double newline spacing |

---

## Architecture Decisions

1. Spell checker detects only.
2. Suggester generates candidates.
3. API composes detection and suggestions.
4. Suffix stripping is the validation gate before marking a word wrong.
5. False positives are worse than missing optional style suggestions.
6. Period vs danda is not treated as an error in the MVP.
7. Frontend should tolerate both old and new API schemas during deployment transitions.

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
|   |-- day4.md
|   `-- day5.md
|-- models\
|-- notebooks\
|   `-- indicbert_explore.ipynb
|-- scripts\
|   |-- build_wordlist.py
|   |-- debug_aan.py
|   |-- debug_unicode.py
|   |-- fix_frontend.py
|   |-- fix_frontend_v2.py
|   |-- fix_grammar_tests.py
|   |-- fix_main_suggestions.py
|   |-- fix_suffix_test.py
|   |-- patch_spell_checker.py
|   |-- patch_spell_checker_v2.py
|   |-- patch_spell_checker_v3.py
|   |-- remove_danda_rule.py
|   |-- topup_wordlist.py
|   |-- update_main.py
|   |-- update_main_v3.py
|   |-- update_tests.py
|   |-- write_frontend_v2.py
|   |-- write_main_v3.py
|   |-- write_procfile.py
|   |-- write_requirements.py
|   |-- write_suffix_stripper.py
|   |-- write_test_suggest.py
|   `-- test_suggest.py
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
    |   |-- suffix_stripper.py
    |   `-- suggester.py
    `-- utils\
```

---

## Pending for Day 6

- Validate Railway v0.3.0 deployment.
- Test Gradio production backend toggle after Railway redeploy.
- Expand wordlist systematically to 1000+ words.
- Add dedicated pytest coverage for `suffix_stripper.py`.
- Add in-text frontend highlighting using `char_offset`.
- Explore HuggingFace Spaces for MuRIL-friendly deployment.
