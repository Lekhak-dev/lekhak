from pathlib import Path

content = r'''from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import unicodedata
import re

from src.rules.spell_checker import check_spelling, load_wordlist
from src.rules.grammar_checker import check_grammar
from src.rules.suggester import get_suggestions

app = FastAPI(
    title="Lekhak API",
    description="Marathi proofreading engine",
    version="0.3.0"
)

_wordlist = load_wordlist()


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

    enriched_errors = []
    for err in spell_result["errors"]:
        word = err["word"]
        word_index = err["index"]
        char_offset = _find_char_offset(text, word, word_index)
        suggestions = get_suggestions(word, list(_wordlist))
        enriched_errors.append(SpellingErrorDetail(
            word=word,
            index=word_index,
            char_offset=char_offset,
            suggestions=suggestions[:5]
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
        except Exception:
            suggestions = get_suggestions(word, list(_wordlist))
            return SuggestResponse(word=word, suggestions=suggestions, ranking_mode="edit_distance_fallback")

    suggestions = get_suggestions(word, list(_wordlist))
    return SuggestResponse(word=word, suggestions=suggestions, ranking_mode="edit_distance")


def _find_char_offset(text: str, word: str, word_index: int) -> int:
    tokens_with_pos = [(m.group(), m.start()) for m in re.finditer(r'[^\s।]+', text)]
    if word_index < len(tokens_with_pos):
        return tokens_with_pos[word_index][1]
    return -1
'''

Path("src/api/main.py").write_text(content, encoding="utf-8")
print("src/api/main.py written — v0.3.0")