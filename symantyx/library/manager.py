import json
import re
from pathlib import Path


class LibraryManager:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.index_path = self.root / "library_index.json"
        if not self.index_path.exists():
            self._write_index({})

    def _read_index(self) -> dict:
        with self.index_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_index(self, data: dict):
        with self.index_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def list_snippets(self) -> list[str]:
        idx = self._read_index()
        return sorted(idx.keys())

    def save_snippet(self, name: str, content: str, tags: list[str] | None = None):
        idx = self._read_index()
        snippet_path = self.root / f"{name}.txt"
        snippet_path.write_text(content, encoding="utf-8")
        idx[name] = {
            "path": str(snippet_path),
            "tags": tags or []
        }
        self._write_index(idx)

    def load_snippet(self, name: str) -> str:
        idx = self._read_index()
        meta = idx.get(name)
        if not meta:
            return ""
        return Path(meta["path"]).read_text(encoding="utf-8")

    def save_module_from_header(self, header: str, content: str):
        """
        header example: '5. OCR operator module (engine/ocr_operator.py)'
        content: the code block to write into that file
        """
        match = re.search(r"\(([^)]+)\)", header)
        if not match:
            return None

        rel_path = match.group(1).strip()
        rel_path = rel_path.replace("\\", "/").strip("/")
        if not rel_path:
            return None

        target = (Path(__file__).resolve().parent.parent / rel_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        idx = self._read_index()
        name = rel_path
        idx[name] = {
            "path": str(target),
            "tags": ["module", "auto_generated"],
        }
        self._write_index(idx)
        return target
