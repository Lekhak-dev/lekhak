import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rules.spell_checker import check_spelling, normalize_word, tokenize


def test_correct_sentence_no_errors():
    text = "मी घरी आहे"
    result = check_spelling(text)
    assert result["error_count"] == 0


def test_misspelled_word_detected():
    text = "मी घरि आहे"   # घरि is wrong, घरी is correct
    result = check_spelling(text)
    assert result["error_count"] >= 1


def test_normalize_word_strips_punctuation():
    assert normalize_word("शाळा।") == "शाळा"
    assert normalize_word("घर,") == "घर"


def test_tokenize_splits_correctly():
    tokens = tokenize("मी जातो। तू येतो।")
    assert "मी" in tokens
    assert "जातो" in tokens


def test_suggestions_returned_for_typo():
    text = "मि शाळेत जातो"   # मि instead of मी
    result = check_spelling(text)
    errors = result["errors"]
    if errors:
        assert isinstance(errors[0]["suggestions"], list)