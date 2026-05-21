"""
Lekhak - FastAPI Main Application
POST /check - accepts Marathi text, returns spelling + grammar analysis.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sys
import os

# Make sure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.rules.spell_checker import check_spelling, load_wordlist
from src.rules.suggester import get_suggestions as get_edit_suggestions
from src.rules.grammar_checker import check_grammar

# Load wordlist once at startup — not on every request
_wordlist = load_wordlist()
app = FastAPI(
    title="Lekhak API",
    description="AI-powered Marathi proofreading engine",
    version="0.1.0"
)

# Allow all origins for local dev (lock this down in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextInput(BaseModel):
    text: str = Field(
    ...,
    min_length=1,
    max_length=10000,
    json_schema_extra={"example": "मी शाळेत जातो आणि पुस्तक वाचतो।"}
)


class CheckResponse(BaseModel):
    input_text: str
    spelling: dict
    grammar: dict
    total_issues: int


@app.get("/")
def root():
    return {"message": "Lekhak API is running 🟢", "version": "0.1.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/check", response_model=CheckResponse)
def check_text(payload: TextInput):
    """
    Proofread Marathi text.
    Returns spelling errors and grammar issues with suggestions.
    """
    try:
        spelling_result = check_spelling(payload.text)
        grammar_result = check_grammar(payload.text)
        
        total_issues = (
            spelling_result["error_count"] + grammar_result["error_count"]
        )
        
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

class SuggestRequest(BaseModel):
    word: str


class SuggestResponse(BaseModel):
    word: str
    suggestions: list


@app.post("/suggest", response_model=SuggestResponse)
def suggest_corrections(request: SuggestRequest):
    """
    Returns ranked spelling suggestions for a single Marathi word.
    Layer 1: edit distance based. Layer 2 will add ML ranking.
    """
    word = request.word.strip()
    if not word:
        return SuggestResponse(word=word, suggestions=[])

    suggestions = get_edit_suggestions(word, _wordlist)
    return SuggestResponse(word=word, suggestions=suggestions)