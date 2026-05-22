from pathlib import Path

new_tests = '''

# ── Day 4: New rule tests ──────────────────────────────────────────────────────

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

path = Path("tests/test_grammar_checker.py")
current = path.read_text(encoding="utf-8")

if "test_missing_question_mark_detected" in current:
    print("Tests already present — skipping.")
else:
    path.write_text(current + new_tests, encoding="utf-8")
    print("6 new tests appended to test_grammar_checker.py")