import re
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
try:
    from PIL import ImageGrab  # pyright: ignore[reportMissingImports]
except ImportError:
    ImageGrab = None
try:
    import pytesseract  # pyright: ignore[reportMissingImports]
except ImportError:
    pytesseract = None

class ClipboardImporter:
    HEADER_PATTERN = re.compile(r"\(([^)]+)\)")

    def __init__(self, library_manager):
        self.library = library_manager

    def import_from_clipboard(self):
        root = tk.Tk()
        root.withdraw()

        try:
            text = root.clipboard_get()
        except tk.TclError:
            return self._try_ocr_import()

        return self._process_text(text)

    def import_from_clipboard_history(self, history_items: list[str]):
        # You will wire this to Windows 11 clipboard history API later
        for item in history_items:
            if "(" in item and ")" in item:
                return self._process_text(item)
        return None

    def _try_ocr_import(self):
        if pytesseract is None:
            messagebox.showinfo(
                "Clipboard",
                "OCR is unavailable because pytesseract is not installed.",
            )
            return None

        try:
            img = ImageGrab.grabclipboard()
            if img:
                text = pytesseract.image_to_string(img)
                return self._process_text(text)
        except Exception:
            pass
        messagebox.showinfo("Clipboard", "Clipboard is empty or unsupported.")
        return None

    def _process_text(self, text: str):
        lines = text.strip().splitlines()
        if not lines:
            return None

        header = lines[0]
        code = "\n".join(lines[1:]).strip()

        match = self.HEADER_PATTERN.search(header)
        if not match:
            messagebox.showwarning("No Header", "Clipboard text does not contain a valid module header.")
            return None

        rel_path = match.group(1).strip()
        return self.library.save_module_from_header(header, code)


class library_manager:
    """Simple on-disk library manager for saved modules imported from clipboard."""

    def __init__(self, root_path: str | Path | None = None):
        self.root_path = Path(root_path) if root_path is not None else Path.cwd() / "library"
        self.root_path.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, rel_path: str) -> Path:
        normalized = rel_path.strip().replace("\\", "/")
        if normalized.startswith("/"):
            normalized = normalized.lstrip("/")
        if not normalized:
            raise ValueError("Module path cannot be empty.")

        candidate = self.root_path / normalized
        if not candidate.resolve().is_relative_to(self.root_path.resolve()):
            raise ValueError(f"Refusing to save outside the library root: {rel_path!r}")
        return candidate

    def save_module(self, rel_path: str, code: str) -> Path:
        path = self._resolve_path(rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code, encoding="utf-8")
        return path

    def save_module_from_header(self, header: str, code: str):
        match = re.search(r"\(([^)]+)\)", header)
        if not match:
            raise ValueError(f"Clipboard header does not include a module path: {header!r}")
        rel_path = match.group(1).strip()
        return self.save_module(rel_path, code)

    def load_module(self, rel_path: str) -> str:
        path = self._resolve_path(rel_path)
        if not path.exists():
            raise FileNotFoundError(f"Module not found: {rel_path}")
        return path.read_text(encoding="utf-8")

    def module_exists(self, rel_path: str) -> bool:
        try:
            return self._resolve_path(rel_path).exists()
        except ValueError:
            return False

    def list_modules(self) -> list[str]:
        modules: list[str] = []
        for path in sorted(self.root_path.rglob("*")):
            if path.is_file() and path.suffix:
                relative = path.relative_to(self.root_path).as_posix()
                modules.append(relative)
        return modules

    def delete_module(self, rel_path: str) -> bool:
        path = self._resolve_path(rel_path)
        if not path.exists():
            return False
        if path.is_dir():
            raise IsADirectoryError(f"Path is a directory, not a module: {rel_path}")
        path.unlink()
        return True
