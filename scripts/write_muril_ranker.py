from pathlib import Path

content = '''"""
Lekhak — MuRIL Contextual Ranker (Layer 2)
Ranks spelling candidates by contextual similarity using google/muril-base-cased.

Architecture:
- Input: misspelled word + sentence context + candidates from Layer 1
- For each candidate: substitute into sentence, get MuRIL embedding
- Score = cosine similarity between candidate sentence and original sentence
- Higher score = better contextual fit
- Falls back to edit distance ranking if sentence not provided
"""

import unicodedata
from typing import List, Dict, Optional
import torch
from transformers import AutoTokenizer, AutoModel

MODEL_NAME = "google/muril-base-cased"

# Module-level singletons — loaded once, reused across requests
_tokenizer = None
_model = None


def _load_model():
    """Lazy load MuRIL — only on first ML ranking request."""
    global _tokenizer, _model
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModel.from_pretrained(MODEL_NAME)
        _model.eval()


def _normalize(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _get_embedding(text: str) -> torch.Tensor:
    """
    Get mean-pooled sentence embedding from MuRIL.
    Mean pooling over all token embeddings (excluding padding).
    """
    inputs = _tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        padding=True
    )
    with torch.no_grad():
        outputs = _model(**inputs)

    # Mean pool over token dimension (dim=1), respecting attention mask
    token_embeddings = outputs.last_hidden_state  # (1, seq_len, hidden)
    attention_mask = inputs["attention_mask"]      # (1, seq_len)
    mask_expanded = attention_mask.unsqueeze(-1).float()
    sum_embeddings = (token_embeddings * mask_expanded).sum(dim=1)
    sum_mask = mask_expanded.sum(dim=1).clamp(min=1e-9)
    return sum_embeddings / sum_mask  # (1, hidden)


def _cosine_similarity(a: torch.Tensor, b: torch.Tensor) -> float:
    """Cosine similarity between two embedding vectors."""
    a = a / a.norm(dim=-1, keepdim=True)
    b = b / b.norm(dim=-1, keepdim=True)
    return float((a * b).sum())


def rank_candidates_by_context(
    word: str,
    sentence: str,
    candidates: List[Dict]
) -> List[Dict]:
    """
    Re-rank edit-distance candidates by MuRIL contextual similarity.

    Args:
        word:       The misspelled word as it appears in sentence
        sentence:   Full sentence containing the misspelled word
        candidates: List of dicts from get_suggestions() — each has 'word', 'distance'

    Returns:
        Candidates sorted by ml_score descending.
        Each candidate gets a new 'ml_score' field added.
    """
    _load_model()

    word = _normalize(word)
    sentence = _normalize(sentence)

    # Embedding of the original (misspelled) sentence — our reference point
    # We compare each corrected version against this
    original_embedding = _get_embedding(sentence)

    scored = []
    for candidate in candidates:
        candidate_word = _normalize(candidate["word"])

        # Substitute candidate into sentence
        corrected_sentence = sentence.replace(word, candidate_word, 1)
        candidate_embedding = _get_embedding(corrected_sentence)

        score = _cosine_similarity(original_embedding, candidate_embedding)

        scored.append({
            **candidate,
            "ml_score": round(score, 6)
        })

    # Sort by ml_score descending — highest contextual similarity first
    scored.sort(key=lambda x: x["ml_score"], reverse=True)
    return scored
'''

Path("src/rules/muril_ranker.py").write_text(content, encoding="utf-8")
print("muril_ranker.py written to src/rules/")