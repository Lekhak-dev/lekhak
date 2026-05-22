from pathlib import Path

content = '''"""
Lekhak — API test script for /suggest endpoint.
Tests both edit_distance and muril ranking modes.
Run from project root: python scripts/test_suggest.py
"""

import requests
import json

BASE = "http://localhost:8000"

def test(label, payload):
    print(f"\\n{'='*50}")
    print(f"TEST: {label}")
    print(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
    r = requests.post(f"{BASE}/suggest", json=payload)
    if r.status_code == 200:
        data = r.json()
        print(f"Mode: {data['ranking_mode']}")
        print(f"Word: {data['word']}")
        print(f"Suggestions ({len(data['suggestions'])}):")
        for s in data['suggestions']:
            print(f"  {s}")
    else:
        print(f"ERROR {r.status_code}: {r.text}")

# Test 1 — edit distance
test("Edit distance ranking", {
    "word": "घरि",
    "ml_ranking": False
})

# Test 2 — MuRIL ranking
test("MuRIL ranking", {
    "word": "घरि",
    "sentence": "मी घरि जातो",
    "ml_ranking": True
})

# Test 3 — MuRIL without sentence (should return 400)
test("MuRIL without sentence (expect 400)", {
    "word": "घरि",
    "ml_ranking": True
})
'''

Path("scripts/test_suggest.py").write_text(content, encoding="utf-8")
print("scripts/test_suggest.py written.")