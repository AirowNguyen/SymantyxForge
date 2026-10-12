"""
Symantyx Hydration Pipeline
Priority 1 Debugging — Core Engine Hydration

This module provides the real hydration logic used by SymantyxEngine.
It transforms raw text → tokens → etymology → concepts → hypertuples.
"""

from pathlib import Path
from typing import Any, Dict, List
import json

from engine.hypertuple import Hypertuple


class HydrationPipeline:
    def __init__(self, etymology_path: Path):
        self.etymology = self._load_etymology(etymology_path)

    # ------------------------------------------------------------------
    # Load etymology JSONL
    # ------------------------------------------------------------------
    def _load_etymology(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}

        ety = {}
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    word = entry.get("word")
                    if word:
                        ety[word.lower()] = entry
                except Exception:
                    continue
        return ety

    # ------------------------------------------------------------------
    # Tokenization
    # ------------------------------------------------------------------
    def tokenize(self, text: str) -> List[str]:
        return [
            token.strip(".,!?;:\"'()[]{}").lower()
            for token in text.split()
            if token.strip()
        ]

    # ------------------------------------------------------------------
    # Etymology lookup
    # ------------------------------------------------------------------
    def etymon_map(self, tokens: List[str]) -> Dict[str, Dict[str, Any]]:
        return {t: self.etymology.get(t, {}) for t in tokens}

    # ------------------------------------------------------------------
    # Concept resolution (minimal)
    # ------------------------------------------------------------------
    def resolve_concepts(self, etymons: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        concepts = []
        for word, ety in etymons.items():
            concepts.append({
                "word": word,
                "origin": ety.get("origin"),
                "root": ety.get("root"),
                "definition": ety.get("definition"),
                "tags": ety.get("tags", [])
            })
        return concepts

    # ------------------------------------------------------------------
    # Emit hypertuples
    # ------------------------------------------------------------------
    def emit_hypertuples(self, concepts: List[Dict[str, Any]], domain: str) -> List[Hypertuple]:
        hypertuples = []
        for concept in concepts:
            h = Hypertuple(
                id=f"{domain}-{concept['word']}",
                domain=domain,
                fields=concept,
                tags=["hydrated", "concept"],
                provenance={"source": "hydration_pipeline"}
            )
            hypertuples.append(h)
        return hypertuples

    # ------------------------------------------------------------------
    # Full hydration pipeline
    # ------------------------------------------------------------------
    def hydrate(self, text: str, domain: str) -> List[Hypertuple]:
        tokens = self.tokenize(text)
        etymons = self.etymon_map(tokens)
        concepts = self.resolve_concepts(etymons)
        hypertuples = self.emit_hypertuples(concepts, domain)
        return hypertuples
