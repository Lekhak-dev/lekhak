import unicodedata
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
