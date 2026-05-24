from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import unicodedata

from src.rules.spell_checker import check_spelling, load_wordlist
from src.rules.grammar_checker import check_grammar
from src.rules.suggester import get_suggestions

app = FastAPI(
    title="Lekhak API",
    description="Marathi proofreading engine",
    version="0.3.0"
)

_wordlist = load_wordlist()

# ── Request/Response models ──────────────────────────────────────────────────

class CheckRequest(BaseModel):
    text: str

class SpellingErrorDetail(BaseModel):
    word: str
    index: int
    char_offset: int
    suggestions: list[str]

class CheckResponse(BaseModel):
    spelling_errors: list[SpellingErrorDetail]
    grammar_errors: list[dict]
    total_words: int
    spelling_error_count: int
    grammar_error_count: int

class SuggestRequest(BaseModel):
    word: str
    sentence: Optional[str] = None
    ml_ranking: bool = False

class SuggestResponse(BaseModel):
    word: str
    suggestions: list[str]
    ranking_mode: str

# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Lekhak API v0.3.0", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.3.0"}

@app.post("/check", response_model=CheckResponse)
def check(request: CheckRequest):
    text = unicodedata.normalize("NFC", request.text)

    spell_result = check_spelling(text, _wordlist)
    grammar_result = check_grammar(text)

    # Build enriched spelling errors with suggestions + char offsets
    enriched_errors = []
    for err in spell_result["errors"]:
        word = err["word"]
        word_index = err["index"]

        # Compute char_offset: find position of this word occurrence in text
        # We find the nth occurrence matching word_index
        char_offset = _find_char_offset(text, word, word_index)

        suggestions = get_suggestions(word, list(_wordlist))

        enriched_errors.append(SpellingErrorDetail(
            word=word,
            index=word_index,
            char_offset=char_offset,
            suggestions=suggestions[:5]  # top 5 only
        ))

    return CheckResponse(
        spelling_errors=enriched_errors,
        grammar_errors=grammar_result["errors"],
        total_words=spell_result["total_words"],
        spelling_error_count=spell_result["error_count"],
        grammar_error_count=grammar_result["error_count"]
    )

@app.post("/suggest", response_model=SuggestResponse)
def suggest(request: SuggestRequest):
    word = unicodedata.normalize("NFC", request.word)

    if request.ml_ranking and request.sentence:
        try:
            from src.rules.muril_ranker import rank_candidates_by_context
            candidates = get_suggestions(word, list(_wordlist))
            ranked = rank_candidates_by_context(word, request.sentence, candidates)
            return SuggestResponse(
                word=word,
                suggestions=[r["word"] for r in ranked],
                ranking_mode="ml_contextual"
            )
        except Exception as e:
            # Fallback to edit distance if MuRIL unavailable (Railway)
            suggestions = get_suggestions(word, list(_wordlist))
            return SuggestResponse(
                word=word,
                suggestions=suggestions,
                ranking_mode="edit_distance_fallback"
            )

    suggestions = get_suggestions(word, list(_wordlist))
    return SuggestResponse(
        word=word,
        suggestions=suggestions,
        ranking_mode="edit_distance"
    )

# ── Helpers ──────────────────────────────────────────────────────────────────

def _find_char_offset(text: str, word: str, word_index: int) -> int:
    """
    Find the character offset of the word at position word_index in text.
    Tokenizes by whitespace + danda to match spell checker tokenization.
    """
    import re
    # Split on whitespace and danda (।), keeping track of positions
    tokens_with_pos = []
    for m in re.finditer(r'[^\s।]+', text):
        tokens_with_pos.append((m.group(), m.start()))

    if word_index < len(tokens_with_pos):
        return tokens_with_pos[word_index][1]
    return -1
