# evaluator.py
"""
Deterministic lexical-first evaluator (fixed) with HF sentence-similarity fallback.
Scoring uses overlap = intersection_size / len(reference_tokens) (strict).
Returns integer score 0..5 and similarity percent (interpretable).
"""

import requests
import re

HF_API_TOKEN = "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"
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_ENDPOINT = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# Lexical thresholds based on fraction of REFERENCE tokens present in student answer.
# These are chosen to give intuitive scores for partial coverage.
LEXICAL_THRESHOLDS = [
    (0.90, 5),   # >=90% of reference tokens => 5
    (0.66, 4),   # >=66% => 4
    (0.50, 3),   # >=50% => 3
    (0.33, 2),   # >=33% => 2
    (0.15, 1),   # >=15% => 1
    (0.0,  0),
]

# HF similarity thresholds used only when lexical overlap == 0
HF_THRESHOLDS = [
    (0.80, 5),
    (0.65, 4),
    (0.50, 3),
    (0.35, 2),
    (0.20, 1),
    (0.0,  0),
]


def preprocess_text(text):
    """Lowercase, remove punctuation, split into tokens."""
    if not text:
        return []
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [t for t in text.split() if t]


class AnswerEvaluator:
    def __init__(self):
        self._sentsim_cache = {}

    def _post(self, payload, timeout=20):
        try:
            r = requests.post(MODEL_ENDPOINT, headers=HEADERS, json=payload, timeout=timeout)
            return r
        except Exception:
            return None

    def _hf_sentence_similarity(self, student_answer, reference_answer):
        """Call HF sentence-similarity pipeline and extract numeric score in [0,1]."""
        key = (student_answer, reference_answer)
        if key in self._sentsim_cache:
            return self._sentsim_cache[key]

        payload = {
            "inputs": {
                "source_sentence": student_answer,
                "sentences": [reference_answer]
            }
        }
        resp = self._post(payload)
        if not resp or resp.status_code != 200:
            return None
        try:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                first = data[0]
                if isinstance(first, (int, float)):
                    sim = float(first)
                elif isinstance(first, dict) and "score" in first:
                    sim = float(first["score"])
                else:
                    sim = None
            else:
                sim = None
        except Exception:
            sim = None

        if sim is not None:
            sim = max(0.0, min(1.0, float(sim)))
            self._sentsim_cache[key] = sim
        return sim

    def token_overlap_ratio_ref(self, reference, student):
        """
        Compute overlap = |tokens_ref ∩ tokens_student| / len(tokens_ref)
        (stricter: measures fraction of reference covered by student)
        """
        ref_tokens = [t for t in preprocess_text(reference)]
        stud_tokens = set(preprocess_text(student))
        if not ref_tokens:
            return 0.0
        if not stud_tokens:
            return 0.0
        inter = set(ref_tokens).intersection(stud_tokens)
        return len(inter) / len(ref_tokens)

    def _lexical_score(self, overlap_ratio):
        for thresh, score in LEXICAL_THRESHOLDS:
            if overlap_ratio >= thresh:
                return score
        return 0

    def _hf_score(self, sim):
        for thresh, score in HF_THRESHOLDS:
            if sim >= thresh:
                return score
        return 0

    def _feedback(self, score):
        return {
            5: "Excellent — highly relevant and complete.",
            4: "Very good — mostly relevant.",
            3: "Good — some relevant points present.",
            2: "Fair — partial relevance.",
            1: "Poor — minimally relevant.",
            0: "No relation detected."
        }.get(score, "")

    def evaluate(self, student_answer, reference_answer):
        """
        Returns: (score_int 0..5, feedback_text, similarity_percent)
        Policy:
          1) exact match -> 5
          2) lexical-first: compute overlap = intersection / len(ref_tokens) and map with LEXICAL_THRESHOLDS
          3) if overlap == 0 -> use HF sentence-similarity pipeline and map with HF_THRESHOLDS
          4) if HF call fails -> return 0
        """
        if not student_answer or not reference_answer:
            return 0, "Please provide both reference and student answers.", 0.0

        # exact match (simple & deterministic)
        if student_answer.strip().lower() == reference_answer.strip().lower():
            return 5, self._feedback(5), 100.0

        # lexical overlap (strict: fraction of reference covered)
        overlap = self.token_overlap_ratio_ref(reference_answer, student_answer)

        if overlap > 0.0:
            score = self._lexical_score(overlap)
            sim_pct = round(overlap * 100.0, 2)
            return score, self._feedback(score), sim_pct

        # no lexical overlap -> call HF sentsim
        sim = self._hf_sentence_similarity(student_answer, reference_answer)
        if sim is None:
            # HF failed or returned unexpected format -> treat as no relation
            return 0, self._feedback(0), 0.0

        score = self._hf_score(sim)
        return score, self._feedback(score), round(sim * 100.0, 2)

