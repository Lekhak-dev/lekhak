# Lekhak — Day 3 Log

Date: 21-05-2026

---

## Work Completed

### 1. Gradio Frontend
- Created frontend/app.py
- Two tabs: मजकूर तपासा + शब्द सुचवणे
- Tab 1 calls POST /check → displays spelling + grammar results
- Tab 2 calls POST /suggest → displays ranked suggestions
- Runs on localhost:7860
- Tested with "तो घरि गेला होता." — error detected correctly

### 2. /suggest Endpoint
- Created src/rules/suggester.py
- Levenshtein edit distance implementation
- Dynamic threshold:
  - word length <= 3 → max_distance = 1
  - word length <= 6 → max_distance = 2
  - word length > 6  → max_distance = 3
- Length filter: skip candidates where abs(len difference) > max_distance
- Added POST /suggest to src/api/main.py
- _wordlist loaded once at startup (not per request)
- Tests written in tests/test_suggest.py

### 3. Wordlist Expansion
- Moved wordlist to data/marathi_wordlist.txt
- File-driven loading with NFC normalization on load
- Expanded vocabulary with inflections, verbs, nouns

### 4. Bug Fixes
- load_wordlist() was being called with argument → fixed (uses module-level WORDLIST_PATH)
- Duplicate load_wordlist definition → removed
- Garbled Unicode in strip_chars → fixed
- Suggestion noise (आणि, तर, जर for घरि) → fixed with dynamic threshold

### 5. MuRIL Exploration (notebooks/indicbert_explore.ipynb)
- Model: google/muril-base-cased
- Reason for switch: ai4bharat/indic-bert is gated repo (401 error)
- Model downloaded and cached locally (~900MB)
- Tokenization confirmed working for Marathi

---

## Key Findings

### Tokenization
- Known words stay intact: घरी → ['घरी']
- Unknown/misspelled words split into subwords: घरि → ['घर', '##ि']
- This is WordPiece tokenization — standard BERT behavior

### Cosine Similarity
- Correct sentence:    तो घरी गेला होता. → CLS norm: 0.6278
- Misspelled sentence: तो घरि गेला होता. → CLS norm: 0.6280
- Cosine similarity: 0.9999

### Architectural Decision
- MuRIL is too robust to USE for error detection
- MuRIL role confirmed: contextual RANKER of Layer 1 candidates
- Flow: Layer 1 detects → Layer 1 generates candidates → Layer 2 ranks

---

## Architecture Decisions Taken

| Decision | Rationale |
|----------|-----------|
| Use google/muril-base-cased not ai4bharat/indic-bert | IndicBERT is gated, MuRIL is ungated and comparable quality |
| MuRIL = ranker not detector | Cosine similarity 0.9999 — model too robust to catch errors |
| Dynamic threshold in suggester | Fixed noise from short word false matches |
| _wordlist loaded once at startup | Performance — avoid reloading on every request |
| Wordlist is file-driven | Enables wordlist updates without touching source code |

---

## Test Results
- All existing tests passing
- New tests added: tests/test_suggest.py

---

## Pending for Day 4

### Block 1 — Product
- [ ] Expand wordlist to 500+ words
- [ ] Add 3-4 new grammar rules
- [ ] Deploy to Railway — get live URL

### Block 2 — ML
- [ ] Implement MuRIL candidate scoring function
- [ ] Integrate into /suggest as ml_ranking=true parameter
- [ ] Test edit distance vs MuRIL ranking side by side

---

## Commands Reference

# Start backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend
python frontend/app.py

# Run tests
pytest tests/ -v

# Git
git add .
git commit -m "message"
git push