"""
Lekhak — Marathi Suggestion Engine
Edit-distance based suggestions for Layer 1.
ML ranking will replace this in Layer 2.
"""

import unicodedata
from typing import List, Dict


def normalize(text: str) -> str:
    return unicodedata.normalize('NFC', text)


def edit_distance(a: str, b: str) -> int:
    """Levenshtein distance between two strings."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]


def get_suggestions(word: str, wordlist: set, max_suggestions: int = 5) -> List[Dict]:
    """Return ranked suggestions for a Marathi word using edit distance."""
    word = normalize(word)
    
    # Dynamic threshold — short words need stricter matching
    if len(word) <= 3:
        max_distance = 1
    elif len(word) <= 6:
        max_distance = 2
    else:
        max_distance = 3

    candidates = []

    for candidate in wordlist:
        if abs(len(candidate) - len(word)) > max_distance:
            continue
        dist = edit_distance(word, candidate)
        if dist <= max_distance:
            candidates.append({"word": candidate, "distance": dist})

    candidates.sort(key=lambda x: x["distance"])
    return candidates[:max_suggestions]