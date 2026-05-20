import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rules.grammar_checker import (
    check_grammar,
    check_double_spaces,
    check_repeated_words,
    check_missing_danda
)


def test_double_space_detected():
    result = check_double_spaces("मी  घरी आहे")
    assert len(result) == 1
    assert result[0]["type"] == "double_space"


def test_no_double_space():
    result = check_double_spaces("मी घरी आहे")
    assert len(result) == 0


def test_repeated_word_detected():
    result = check_repeated_words("मी मी घरी जातो")
    assert len(result) >= 1
    assert result[0]["type"] == "repeated_word"


def test_missing_danda_detected():
    result = check_missing_danda("मी घरी जातो.")
    assert any(e["type"] == "wrong_punctuation" for e in result)


def test_full_grammar_check():
    text = "मी मी घरी जातो.  तू शाळेत जातो।"
    result = check_grammar(text)
    assert result["error_count"] > 0