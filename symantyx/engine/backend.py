"""
Symantyx Engine Surface
Priority 1 Debugging — Fully Wired Engine Layer

This module exposes the core engine functions used by:
- backend API server
- UI workbook
- WebView2 canvas
- cmdline operator
- OCR operator
- survey ingest
- pivots/shims
"""

from pathlib import Path
from typing import Any, Dict, List

from .hypertuple import Hypertuple
from .registry import HypertupleRegistry
from .membrane import MembraneBinder
from .tabrs import TabRsEngine

# hydration pipeline (backend module)
from backend.hydration_pipeline import HydrationPipeline


class SymantyxEngine:
    """
    The unified engine surface.
    All operators, UI, canvas, and backend call into this class.
    """

    def __init__(self, db_path: Path):
        # registry
        self.registry = HypertupleRegistry(db_path)

        # membrane
        self.membrane = MembraneBinder(domain="symantyx")

        # TabRs semantic engine
        self.tabrs = TabRsEngine()

        # hydration pipeline
        ety_path = Path(__file__).parent.parent / "data" / "etymology.jsonl"
        self.hydration = HydrationPipeline(ety_path)

    # ------------------------------------------------------------------
    # HYDRATION
    # ------------------------------------------------------------------
    def hydrate(self, text: str, domain: str) -> List[Hypertuple]:
        """
        Run the full hydration pipeline:
        tokenize → etymology → concepts → hypertuples
        """
        return self.hydration.hydrate(text, domain)

    # ------------------------------------------------------------------
    # FULL PIPELINE
    # ------------------------------------------------------------------
    def process_text(self, text: str, domain: str) -> Dict[str, Any]:
        """
        Full engine pipeline:
        hydrate → membrane → registry → TabRs
        """

        # 1. hydrate
        hypertuples = self.hydrate(text, domain)

        # 2. membrane binding
        bound = self.membrane.bind_all(hypertuples)

        # 3. registry storage
        for h in bound:
            payload_json = self._serialize(h)
            self.registry.store(h, payload_json)

        # 4. TabRs semantic forces
        tabrs_result = self.tabrs.apply_forces(text)

        # 5. return full result
        return {
            "hypertuples": [self._to_dict(h) for h in bound],
            "tabrs": tabrs_result,
        }

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------
    def _make_id(self, domain: str) -> str:
        from uuid import uuid4
        return f"{domain}-{uuid4().hex}"

    def _serialize(self, h: Hypertuple) -> str:
        import json
        return json.dumps(self._to_dict(h), ensure_ascii=False)

    def _to_dict(self, h: Hypertuple) -> Dict[str, Any]:
        return {
            "id": h.id,
            "domain": h.domain,
            "fields": h.fields,
            "tags": h.tags,
            "provenance": h.provenance,
        }
