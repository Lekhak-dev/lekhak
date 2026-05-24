from pathlib import Path

content = '''"""
Lekhak — Marathi Grammar Checker (Rule-Based)
Day 5: 7 rules (removed wrong_punctuation — period vs danda is user preference)
"""

import re
from typing import List, Dict


def check_double_spaces(text: str) -> List[Dict]:
    errors = []
    for m in re.finditer(r" {2,}", text):
        errors.append({
            "type": "double_space",
            "position": m.start(),
            "message": "दोन किंवा अधिक spaces एकत्र आहेत.",
            "suggestion": "एकच space वापरा."
        })
    return errors


def check_repeated_words(text: str) -> List[Dict]:
    errors = []
    tokens = text.split()
    for i in range(1, len(tokens)):
        if tokens[i] == tokens[i - 1]:
            errors.append({
                "type": "repeated_word",
                "word": tokens[i],
                "position": i,
                "message": f"\\'{tokens[i]}\\' हा शब्द सलग दोनदा आला आहे.",
                "suggestion": "एकच शब्द वापरा."
            })
    return errors


def check_sentence_start_capital(text: str) -> List[Dict]:
    errors = []
    for i, sentence in enumerate(re.split(r"[।.\\n]", text)):
        sentence = sentence.strip()
        if sentence and sentence[0].isalpha() and sentence[0] == sentence[0].lower() and sentence[0].isascii():
            errors.append({
                "type": "lowercase_start",
                "sentence_index": i,
                "message": "वाक्य लहान इंग्रजी अक्षराने सुरू होते.",
                "suggestion": "वाक्याची सुरुवात मोठ्या अक्षराने करा."
            })
    return errors


def check_question_mark(text: str) -> List[Dict]:
    errors = []
    question_words = ["कोण", "काय", "कुठे", "केव्हा", "कसे", "किती", "का"]
    for i, sentence in enumerate(re.split(r"[।\\n]", text)):
        sentence = sentence.strip()
        if not sentence:
            continue
        has_q = any(qw in sentence for qw in question_words)
        if has_q and not sentence.endswith("?"):
            errors.append({
                "type": "missing_question_mark",
                "sentence_index": i,
                "message": "प्रश्नार्थक वाक्याच्या शेवटी \'?\' नाही.",
                "suggestion": "वाक्याच्या शेवटी \'?\' वापरा."
            })
    return errors


def check_multiple_punctuation(text: str) -> List[Dict]:
    errors = []
    patterns = [
        (r"।।+", "दुहेरी दंड (।।) वापरू नका."),
        (r"\\?\\?+", "दुहेरी प्रश्नचिन्ह (??) वापरू नका."),
        (r"!!+", "दुहेरी उद्गारचिन्ह (!!) वापरू नका."),
    ]
    for pattern, message in patterns:
        for m in re.finditer(pattern, text):
            errors.append({
                "type": "multiple_punctuation",
                "position": m.start(),
                "found": m.group(),
                "message": message,
                "suggestion": "एकच विरामचिन्ह वापरा."
            })
    return errors


def check_space_before_danda(text: str) -> List[Dict]:
    errors = []
    for m in re.finditer(r" ।", text):
        errors.append({
            "type": "space_before_danda",
            "position": m.start(),
            "message": "दंडाआधी (।) space नको.",
            "suggestion": "दंडापूर्वीची space काढा."
        })
    return errors


def check_mixed_script_spacing(text: str) -> List[Dict]:
    errors = []
    pattern = r"([\\u0900-\\u097F])([A-Za-z])|([A-Za-z])([\\u0900-\\u097F])"
    for m in re.finditer(pattern, text):
        errors.append({
            "type": "mixed_script_no_space",
            "position": m.start(),
            "found": m.group(),
            "message": "देवनागरी आणि इंग्रजी अक्षरांमध्ये space नाही.",
            "suggestion": "दोन लिपींमध्ये space द्या."
        })
    return errors


def check_grammar(text: str) -> Dict:
    errors = []
    errors.extend(check_double_spaces(text))
    errors.extend(check_repeated_words(text))
    errors.extend(check_sentence_start_capital(text))
    errors.extend(check_question_mark(text))
    errors.extend(check_multiple_punctuation(text))
    errors.extend(check_space_before_danda(text))
    errors.extend(check_mixed_script_spacing(text))
    return {"errors": errors, "error_count": len(errors)}
'''

Path("src/rules/grammar_checker.py").write_text(content, encoding="utf-8")
print("grammar_checker.py updated — wrong_punctuation rule removed. 7 rules active.")