from pathlib import Path

content = '''"""
Lekhak — Marathi Spell Checker
Rule-based spell checker using wordlist dictionary.
"""
import os
import re
import unicodedata
from typing import List, Dict, Optional

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
    strip_chars = "।॥,.!?\\"\'();:-—–\\u200b\\u200c\\u200d"
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
    Returns errors list with index + char_offset, total_words, error_count.
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
        if word not in wordlist:
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
    test_text = "मी शाळेत जातो आणि पुस्तक वाचतो"
    result = check_spelling(test_text)
    print(result)
'''

Path("src/rules/spell_checker.py").write_text(content, encoding="utf-8")
print("src/rules/spell_checker.py patched.")