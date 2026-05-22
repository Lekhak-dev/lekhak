from pathlib import Path

content = '''"""
Lekhak - FastAPI Main Application
POST /check  - spelling + grammar analysis
POST /suggest - ranked suggestions (edit distance or MuRIL)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.rules.spell_checker import check_spelling, load_wordlist
from src.rules.suggester import get_suggestions as get_edit_suggestions
from src.rules.grammar_checker import check_grammar

_wordlist = load_wordlist()

app = FastAPI(
    title="Lekhak API",
    description="AI-powered Marathi proofreading engine",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)


class CheckResponse(BaseModel):
    input_text: str
    spelling: dict
    grammar: dict
    total_issues: int


class SuggestRequest(BaseModel):
    word: str
    sentence: Optional[str] = None   # required for ml_ranking
    ml_ranking: bool = False          # default: edit distance


class SuggestResponse(BaseModel):
    word: str
    suggestions: list
    ranking_mode: str                 # "edit_distance" or "muril"


@app.get("/")
def root():
    return {"message": "Lekhak API is running", "version": "0.2.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/check", response_model=CheckResponse)
def check_text(payload: TextInput):
    try:
        spelling_result = check_spelling(payload.text)
        grammar_result = check_grammar(payload.text)
        total_issues = spelling_result["error_count"] + grammar_result["error_count"]
        return CheckResponse(
            input_text=payload.text,
            spelling=spelling_result,
            grammar=grammar_result,
            total_issues=total_issues
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/suggest", response_model=SuggestResponse)
def suggest_corrections(request: SuggestRequest):
    """
    Returns ranked spelling suggestions.
    ml_ranking=false (default): edit distance ranking
    ml_ranking=true:            MuRIL contextual ranking (requires sentence)
    """
    word = request.word.strip()
    if not word:
        return SuggestResponse(word=word, suggestions=[], ranking_mode="edit_distance")

    # Layer 1 — always run edit distance first to get candidates
    candidates = get_edit_suggestions(word, _wordlist)

    if not candidates:
        return SuggestResponse(word=word, suggestions=[], ranking_mode="edit_distance")

    # Layer 2 — re-rank with MuRIL if requested and sentence provided
    if request.ml_ranking:
        if not request.sentence:
            raise HTTPException(
                status_code=400,
                detail="ml_ranking=true requires a sentence field."
            )
        try:
            from src.rules.muril_ranker import rank_candidates_by_context
            candidates = rank_candidates_by_context(word, request.sentence, candidates)
            return SuggestResponse(word=word, suggestions=candidates, ranking_mode="muril")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"MuRIL ranking error: {str(e)}")

    return SuggestResponse(word=word, suggestions=candidates, ranking_mode="edit_distance")
'''

Path("src/api/main.py").write_text(content, encoding="utf-8")
print("main.py updated.")