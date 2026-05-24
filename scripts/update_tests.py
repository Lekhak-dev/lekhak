from pathlib import Path

# ── test_api.py ───────────────────────────────────────────────────────────────
api_tests = '''from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_check_endpoint_valid_input():
    response = client.post("/check", json={"text": "मी घरी आहे"})
    assert response.status_code == 200
    data = response.json()
    assert "spelling_errors" in data
    assert "grammar_errors" in data
    assert "total_words" in data
    assert "spelling_error_count" in data
    assert "grammar_error_count" in data

def test_check_endpoint_empty_input():
    # Empty string is valid input — returns 200 with zero errors
    response = client.post("/check", json={"text": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["spelling_error_count"] == 0
    assert data["grammar_error_count"] == 0

def test_check_endpoint_detects_issues():
    # मी मी = repeated word (grammar), double space = grammar
    response = client.post("/check", json={"text": "मी मी घरी जातो.  "})
    assert response.status_code == 200
    data = response.json()
    assert data["grammar_error_count"] > 0

def test_check_spelling_error_has_suggestions():
    # घरि is misspelled — should return spelling error with suggestions
    response = client.post("/check", json={"text": "मी घरि जातो"})
    assert response.status_code == 200
    data = response.json()
    assert data["spelling_error_count"] >= 1
    err = data["spelling_errors"][0]
    assert err["word"] == "घरि"
    assert isinstance(err["suggestions"], list)
    assert isinstance(err["char_offset"], int)
    assert isinstance(err["index"], int)

def test_suggest_endpoint_basic():
    response = client.post("/suggest", json={"word": "घरि"})
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert "ranking_mode" in data
    assert data["ranking_mode"] == "edit_distance"
'''

# ── test_spell_checker.py ─────────────────────────────────────────────────────
spell_tests = '''import unicodedata
from src.rules.spell_checker import check_spelling, load_wordlist, normalize_word, tokenize

_wordlist = load_wordlist()

def test_correct_sentence_no_errors():
    result = check_spelling("मी घरी आहे", _wordlist)
    assert result["error_count"] == 0

def test_misspelled_word_detected():
    result = check_spelling("मी घरि जातो", _wordlist)
    assert result["error_count"] >= 1
    words = [e["word"] for e in result["errors"]]
    assert "घरि" in words

def test_normalize_word_strips_punctuation():
    assert normalize_word("घरी.") == "घरी"
    assert normalize_word("।मी।") == "मी"

def test_tokenize_splits_correctly():
    tokens = tokenize("मी घरी जातो।")
    assert "मी" in tokens
    assert "घरी" in tokens

def test_error_dict_has_index():
    result = check_spelling("मी घरि जातो", _wordlist)
    assert result["error_count"] >= 1
    err = result["errors"][0]
    assert "index" in err
    assert isinstance(err["index"], int)

def test_wordlist_accepts_preloaded():
    # Verify check_spelling works with pre-loaded wordlist (no disk read)
    wl = load_wordlist()
    result = check_spelling("मी घरी आहे", wl)
    assert result["error_count"] == 0
'''

Path("tests/test_api.py").write_text(api_tests, encoding="utf-8")
print("tests/test_api.py updated.")

Path("tests/test_spell_checker.py").write_text(spell_tests, encoding="utf-8")
print("tests/test_spell_checker.py updated.")