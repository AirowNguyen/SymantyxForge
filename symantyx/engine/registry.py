import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from .hypertuple import Hypertuple


class HypertupleRegistry:
    """
    Simple SQLite-backed registry for hypertuples.
    This is intentionally minimal: id, domain, payload (JSON string).
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_schema(self) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS hypertuples (
                id TEXT PRIMARY KEY,
                domain TEXT,
                payload TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def store(self, hypertuple: Hypertuple, payload_json: str) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO hypertuples (id, domain, payload)
            VALUES (?, ?, ?)
            """,
            (hypertuple.id, hypertuple.domain, payload_json),
        )
        conn.commit()
        conn.close()

    def retrieve(self, tuple_id: str) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, domain, payload FROM hypertuples WHERE id = ?",
            (tuple_id,),
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {"id": row[0], "domain": row[1], "payload": row[2]}

    def search_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, domain, payload FROM hypertuples WHERE domain = ?",
            (domain,),
        )
        rows = cur.fetchall()
        conn.close()
        return [
            {"id": r[0], "domain": r[1], "payload": r[2]}
            for r in rows
        ]
