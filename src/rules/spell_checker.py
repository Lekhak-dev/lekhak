"""
Lekhak — Marathi Spell Checker
Rule-based spell checker using wordlist dictionary.
"""

import os
import re
import unicodedata
from difflib import get_close_matches
from typing import List, Dict


WORDLIST_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "marathi_wordlist.txt"
)


def load_wordlist() -> set:
    """Load wordlist from data/marathi_wordlist.txt with NFC normalization."""
    words = set()
    path = os.path.normpath(WORDLIST_PATH)

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    words.add(unicodedata.normalize('NFC', word))
    return words


def normalize_word(word: str) -> str:
    """Strip punctuation edges and NFC normalize."""
    word = unicodedata.normalize("NFC", word)
    strip_chars = "।॥,.!?\"'();:-—–\u200b\u200c\u200d"
    word = word.strip(strip_chars)
    return word


def tokenize(text: str) -> List[str]:
    """Split Marathi text into word tokens."""
    tokens = re.split(r"[\s।॥]+", text)
    return [t for t in tokens if t.strip()]


def get_suggestions(word: str, wordlist: set, n: int = 3) -> List[str]:
    """Get close match suggestions for a misspelled word."""
    return get_close_matches(word, wordlist, n=n, cutoff=0.6)


def check_spelling(text: str) -> Dict:
    """
    Main spell check function.
    Returns errors list, total_words, error_count.
    """
    wordlist = load_wordlist()      # <-- no argument, fixed
    tokens = tokenize(text)
    errors = []

    for i, raw_token in enumerate(tokens):
        word = normalize_word(raw_token)

        if not word:
            continue
        if word.isdigit():
            continue

        if word not in wordlist:
            suggestions = get_suggestions(word, wordlist)
            errors.append({
                "word": word,
                "position": i,
                "suggestions": suggestions,
                "message": f"'{word}' हे शब्द शब्दकोशात सापडले नाही."
            })

    return {
        "errors": errors,
        "total_words": len(tokens),
        "error_count": len(errors)
    }


if __name__ == "__main__":
    test_text = "मी शाळेत जातो आणि पुस्तक वाचतो"
    result = check_spelling(test_text)
    print(result)