import sys
sys.path.insert(0, '.')
from src.rules.spell_checker import load_wordlist, normalize_word, tokenize
from src.rules.suffix_stripper import is_valid_with_suffix

wl = load_wordlist()
text = "मुलाला पुस्तक दे"

tokens = tokenize(text)
print(f"tokens: {tokens}")

for raw in tokens:
    normalized = normalize_word(raw)
    valid = is_valid_with_suffix(normalized, wl)
    print(f"  raw={raw!r}  normalized={normalized!r}  valid={valid}  in_wl={normalized in wl}")