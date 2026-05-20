"""
Lekhak — Marathi Grammar Checker (Rule-Based)
Basic grammar, punctuation, and structure checks.
"""

import re
from typing import List, Dict


def check_double_spaces(text: str) -> List[Dict]:
    """Detect multiple consecutive spaces."""
    errors = []
    matches = list(re.finditer(r" {2,}", text))
    for m in matches:
        errors.append({
            "type": "double_space",
            "position": m.start(),
            "message": "दोन किंवा अधिक spaces एकत्र आहेत.",
            "suggestion": "एकच space वापरा."
        })
    return errors


def check_missing_danda(text: str) -> List[Dict]:
    """
    Check if sentences end with danda (।) or proper punctuation.
    Marathi sentences should end with । not just .
    """
    errors = []
    sentences = re.split(r"[।\n]", text)
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
        # If a sentence ends with English period instead of danda
        if sentence.endswith(".") and not sentence.endswith(".."):
            errors.append({
                "type": "wrong_punctuation",
                "sentence_index": i,
                "message": f"वाक्य '.' ने संपते. मराठीत '।' वापरावे.",
                "suggestion": "वाक्याच्या शेवटी '।' वापरा."
            })
    return errors


def check_repeated_words(text: str) -> List[Dict]:
    """Detect consecutive repeated words."""
    errors = []
    tokens = text.split()
    
    for i in range(1, len(tokens)):
        if tokens[i] == tokens[i - 1]:
            errors.append({
                "type": "repeated_word",
                "word": tokens[i],
                "position": i,
                "message": f"'{tokens[i]}' हा शब्द सलग दोनदा आला आहे.",
                "suggestion": "एकच शब्द वापरा."
            })
    return errors


def check_sentence_start_capital(text: str) -> List[Dict]:
    """
    For mixed Marathi-English text:
    Check if English words at start of sentence are capitalized.
    """
    errors = []
    sentences = re.split(r"[।\.\n]", text)
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
        # Check if sentence starts with lowercase English letter
        if sentence and sentence[0].isalpha() and sentence[0] == sentence[0].lower() and sentence[0].isascii():
            errors.append({
                "type": "lowercase_start",
                "sentence_index": i,
                "message": "वाक्य लहान इंग्रजी अक्षराने सुरू होते.",
                "suggestion": "वाक्याची सुरुवात मोठ्या अक्षराने करा."
            })
    return errors


def check_grammar(text: str) -> Dict:
    """
    Run all grammar checks on input text.
    
    Returns:
        Dict with all grammar errors found.
    """
    errors = []
    errors.extend(check_double_spaces(text))
    errors.extend(check_missing_danda(text))
    errors.extend(check_repeated_words(text))
    errors.extend(check_sentence_start_capital(text))
    
    return {
        "errors": errors,
        "error_count": len(errors)
    }


if __name__ == "__main__":
    test_text = "मी शाळेत जातो.  मी मी घरी येतो।"
    result = check_grammar(test_text)
    for e in result["errors"]:
        print(e)