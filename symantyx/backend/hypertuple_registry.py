"""
Symantyx Backend Registry Wrapper
Priority 1 Debugging — Virtual Shim Layer

This module wraps the engine-side HypertupleRegistry so the backend API
can expose registry operations cleanly and safely.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from engine.registry import HypertupleRegistry


class BackendRegistry:
    """
    Virtual shim wrapper around the engine registry.
    Provides safe, backend-facing methods for retrieval and search.
    """

    def __init__(self, db_path: Path):
        self.engine_registry = HypertupleRegistry(db_path)

    # ------------------------------------------------------------------
    # Store hypertuple (delegates to engine registry)
    # ------------------------------------------------------------------
    def store(self, hypertuple, payload_json: str) -> None:
        self.engine_registry.store(hypertuple, payload_json)

    # ------------------------------------------------------------------
    # Retrieve by ID
    # ------------------------------------------------------------------
    def get(self, tuple_id: str) -> Optional[Dict[str, Any]]:
        return self.engine_registry.retrieve(tuple_id)

    # ------------------------------------------------------------------
    # Retrieve by domain
    # ------------------------------------------------------------------
    def get_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        return self.engine_registry.search_by_domain(domain)

    # ------------------------------------------------------------------
    # List all hypertuples (optional)
    # ------------------------------------------------------------------
    def list_all(self) -> List[Dict[str, Any]]:
        """
        Optional helper: list all hypertuples in the registry.
        """
        conn = self.engine_registry._connect()
        cur = conn.cursor()
        cur.execute("SELECT id, domain, payload FROM hypertuples")
        rows = cur.fetchall()
        conn.close()

        return [
            {"id": r[0], "domain": r[1], "payload": r[2]}
            for r in rows
        ]
