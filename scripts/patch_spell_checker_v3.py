from pathlib import Path

content = '''"""
Lekhak — Marathi Spell Checker
Rule-based spell checker using wordlist + morphological suffix stripping.
"""
import os
import re
import sys
import unicodedata
from typing import List, Dict, Optional

# Allow both direct execution and module import
if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.rules.suffix_stripper import is_valid_with_suffix

WORDLIST_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "marathi_wordlist.txt"
)

def load_wordlist() -> set:
    """Load wordlist from data/marathi_wordlist.txt with NFC normalization."""
    words = set()
    path = os.path.normpath(WORDLIST_PATH)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    words.add(unicodedata.normalize("NFC", word))
    return words

def normalize_word(word: str) -> str:
    """Strip punctuation edges and NFC normalize."""
    word = unicodedata.normalize("NFC", word)
    strip_chars = "।॥,.!?\\\"\'();:-—–\\u200b\\u200c\\u200d"
    word = word.strip(strip_chars)
    return word

def tokenize(text: str) -> List[str]:
    """Split Marathi text into word tokens."""
    tokens = re.split(r"[\\s।॥]+", text)
    return [t for t in tokens if t.strip()]

def check_spelling(text: str, wordlist: Optional[set] = None) -> Dict:
    """
    Main spell check function.
    Accepts optional pre-loaded wordlist (avoids disk read on every call).
    Uses suffix stripping to avoid false positives on inflected forms.
    """
    if wordlist is None:
        wordlist = load_wordlist()

    tokens = tokenize(text)
    errors = []

    for i, raw_token in enumerate(tokens):
        word = normalize_word(raw_token)
        if not word:
            continue
        if word.isdigit():
            continue
        if not is_valid_with_suffix(word, wordlist):
            errors.append({
                "word": word,
                "index": i,
                "message": f"\\'{word}\\' हे शब्द शब्दकोशात सापडले नाही."
            })

    return {
        "errors": errors,
        "total_words": len(tokens),
        "error_count": len(errors)
    }

if __name__ == "__main__":
    wl = load_wordlist()
    tests = [
        ("मी शाळेत जातो",     0),   # शाळा + ेत
        ("मी घरात आहे",       0),   # घर + ात
        ("मुलाला पुस्तक दे",  0),   # मुल + ाला
        ("मी घरि जातो",       1),   # no valid root — should fail
    ]
    print("Suffix stripping tests:")
    all_pass = True
    for text, expected_errors in tests:
        r = check_spelling(text, wl)
        actual = r["error_count"]
        status = "✓ PASS" if actual == expected_errors else f"✗ FAIL (expected {expected_errors} errors, got {actual})"
        if actual != expected_errors:
            all_pass = False
        print(f"  {text!r:35} → {status}")
    print()
    print("All tests passed." if all_pass else "Some tests FAILED — check suffix list.")
'''

Path("src/rules/spell_checker.py").write_text(content, encoding="utf-8")
print("src/rules/spell_checker.py written.")