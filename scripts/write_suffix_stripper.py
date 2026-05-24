from pathlib import Path

content = '''"""
Lekhak — Marathi Morphological Suffix Stripper
Strips common Marathi inflectional suffixes to find root words.
Used by spell checker to avoid false positives on inflected forms.
"""

import unicodedata
from typing import Optional

# Suffixes ordered longest-first — critical for correct greedy matching.
# Trying "ांमध्ये" before "मध्ये" ensures we strip the full suffix, not a partial one.
MARATHI_SUFFIXES = [
    # Locative / postpositional (longest first)
    "ांमध्ये", "ांसाठी", "ांवरून", "ांनंतर",
    "मध्ये", "साठी", "वरून", "नंतर", "सोबत", "बद्दल",
    "ातून", "ातला", "ातली", "ातले",
    # Dative / accusative
    "ांना", "ाला", "ीला",
    # Instrumental
    "ांनी", "ाने", "ीने", "ेने",
    # Genitive (possessive)
    "ांचा", "ांची", "ांचे", "ांच्या",
    "ाचा", "ाची", "ाचे", "ाच्या",
    "ीचा", "ीची", "ीचे", "ीच्या",
    "चा", "ची", "चे", "च्या", "चं",
    # Locative short
    "ात", "ीत",
    # Comitative
    "ाशी", "ीशी",
    # Ablative
    "ाहून", "ीहून",
    # Verbal noun / adjectival
    "णारा", "णारी", "णारे",
    "लेला", "लेली", "लेले",
    "तो", "ते", "ती",
    # Short suffixes last
    "ला", "ना", "ने", "शी",
    "ां", "ी", "े", "ा",
]


def strip_suffix(word: str) -> Optional[str]:
    """
    Try stripping each suffix (longest first) from word.
    Returns the root if a suffix was stripped, else None.
    Minimum root length: 2 characters (avoids stripping too aggressively).
    """
    word = unicodedata.normalize("NFC", word)
    for suffix in MARATHI_SUFFIXES:
        if word.endswith(suffix):
            root = word[: len(word) - len(suffix)]
            if len(root) >= 2:
                return unicodedata.normalize("NFC", root)
    return None


def is_valid_with_suffix(word: str, wordlist: set) -> bool:
    """
    Returns True if:
    - word is directly in wordlist, OR
    - stripping a suffix yields a root that is in wordlist
    """
    if word in wordlist:
        return True
    root = strip_suffix(word)
    if root and root in wordlist:
        return True
    return False
'''

Path("src/rules/suffix_stripper.py").write_text(content, encoding="utf-8")
print("src/rules/suffix_stripper.py written.")