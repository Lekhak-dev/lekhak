from pathlib import Path

content = '''import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.rules.grammar_checker import (
    check_grammar,
    check_double_spaces,
    check_repeated_words,
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
    # Rule removed Day 5 — period vs danda is user preference in digital Marathi
    pass

def test_full_grammar_check():
    text = "मी मी घरी जातो.  तू शाळेत जातो।"
    result = check_grammar(text)
    assert result["error_count"] > 0

def test_missing_question_mark_detected():
    result = check_grammar("तू कुठे जातो")
    types = [e["type"] for e in result["errors"]]
    assert "missing_question_mark" in types

def test_question_with_mark_no_error():
    result = check_grammar("तू कुठे जातो?")
    types = [e["type"] for e in result["errors"]]
    assert "missing_question_mark" not in types

def test_double_danda_detected():
    result = check_grammar("वाक्य संपले।।")
    types = [e["type"] for e in result["errors"]]
    assert "multiple_punctuation" in types

def test_space_before_danda_detected():
    result = check_grammar("मी घरी आहे ।")
    types = [e["type"] for e in result["errors"]]
    assert "space_before_danda" in types

def test_no_space_before_danda():
    result = check_grammar("मी घरी आहे।")
    types = [e["type"] for e in result["errors"]]
    assert "space_before_danda" not in types

def test_mixed_script_no_space_detected():
    result = check_grammar("मीschool जातो।")
    types = [e["type"] for e in result["errors"]]
    assert "mixed_script_no_space" in types
'''

Path("tests/test_grammar_checker.py").write_text(content, encoding="utf-8")
print("tests/test_grammar_checker.py fixed.")