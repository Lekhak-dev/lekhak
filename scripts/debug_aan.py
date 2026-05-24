import sys
sys.path.insert(0, '.')
from src.rules.spell_checker import load_wordlist, normalize_word
from src.rules.suffix_stripper import is_valid_with_suffix, strip_suffix

wl = load_wordlist()
word = 'आण'

print(f"in wordlist: {word in wl}")
print(f"strip_suffix: {strip_suffix(word)}")
print(f"is_valid: {is_valid_with_suffix(word, wl)}")

# Show all wordlist entries containing आण
matches = [w for w in wl if 'आण' in w]
print(f"wordlist entries with आण: {matches}")