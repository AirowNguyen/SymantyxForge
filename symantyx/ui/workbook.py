from __future__ import annotations

import importlib
import json
import tkinter as tk
import re
from pathlib import Path
from tkinter import ttk
from typing import Any, TypeAlias

try:
    symantyx_path_builder = importlib.import_module("engine").symantyx_path_builder
except ImportError:
    symantyx_path_builder = importlib.import_module("symantyx_app.engine").symantyx_path_builder

try:
    LibraryManager = importlib.import_module("library.manager").LibraryManager
except ImportError:
    LibraryManager = importlib.import_module("symantyx_app.library.manager").LibraryManager

# Static analysis reports a runtime-imported symbol as a type expression.
# Alias the imported runtime class to a proper type alias to keep the annotation valid.
LibraryManagerType: TypeAlias = Any

class SymantyxWorkbook(tk.Tk):
    def __init__(self, library: LibraryManagerType):
        super().__init__()
        self.title("Symantyx Library Engine · v3.0")
        self.geometry("1100x700")

        self.library = library

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self._init_path_builder_tab()
        self._init_code_library_tab()
        # stubs for future tabs:
        # self._init_tree_builder_tab()
        # self._init_engine_console_tab()
        # self._init_canvas_tab()
        # self._init_ocr_tab()

    def _init_path_builder_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Path Builder")

        # Raw input
        raw_label = ttk.Label(frame, text="Raw Tree Input")
        raw_label.pack(anchor="w", padx=8, pady=(8, 0))

        self.raw_text = tk.Text(frame, height=20, bg="#1e1e1e", fg="#dcdcdc")
        self.raw_text.pack(fill="both", expand=True, padx=8, pady=4)

        # Base path
        base_frame = ttk.Frame(frame)
        base_frame.pack(fill="x", padx=8, pady=4)
        ttk.Label(base_frame, text="Base Path:").pack(side="left")
        self.base_entry = ttk.Entry(base_frame, width=60)
        self.base_entry.insert(0, r"C:\Users\airow")
        self.base_entry.pack(side="left", padx=4)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=8, pady=4)

        ttk.Button(btn_frame, text="Preview", command=self._preview_paths).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Build Paths", command=self._build_paths).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Save Current Snippet as Module",
           command=self._save_current_snippet_as_module).pack(side="left", padx=4)

        # Output log
        log_label = ttk.Label(frame, text="Output Log")
        log_label.pack(anchor="w", padx=8, pady=(8, 0))
        self.log_text = tk.Text(frame, height=10, bg="#111", fg="#dcdcdc")
        self.log_text.pack(fill="x", padx=8, pady=4)

    def _preview_paths(self):
        raw = self.raw_text.get("1.0", "end").strip()
        base = self.base_entry.get().strip()
        if not raw:
            return
        paths = symantyx_path_builder.preview_paths(raw, base)
        self.log_text.delete("1.0", "end")
        for p in paths:
            self.log_text.insert("end", f"[PREVIEW] {p}\n")

    def _build_paths(self):
        raw = self.raw_text.get("1.0", "end").strip()
        base = self.base_entry.get().strip()
        if not raw:
            return
        result = symantyx_path_builder.build_paths(raw, base)
        self.log_text.delete("1.0", "end")
        for line in result.log:
            self.log_text.insert("end", line + "\n")

    def _init_code_library_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Code Library")

        ttk.Label(frame, text="Stored Snippets").pack(anchor="w", padx=8, pady=(8, 0))

        self.snippet_list = tk.Listbox(frame, height=15)
        self.snippet_list.pack(fill="both", expand=True, padx=8, pady=4)
        self.snippet_list.bind("<<ListboxSelect>>", self._on_snippet_select)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=8, pady=4)
        ttk.Button(btn_frame, text="Import from Clipboard",
               command=self._import_from_clipboard).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Import from Clipboard History",
               command=self._import_from_clipboard_history).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Add Current Raw as Snippet",
                   command=self._add_current_raw_as_snippet).pack(side="left", padx=4)

        self.snippet_view = tk.Text(frame, height=10, bg="#111", fg="#dcdcdc")
        self.snippet_view.pack(fill="x", padx=8, pady=4)

        self._refresh_snippet_list()

    def _save_current_snippet_as_module(self):
        sel = self.snippet_list.curselection()
        if not sel:
            return
        header = self.snippet_list.get(sel[0])
        content = self.snippet_view.get("1.0", "end").strip()
        if not content:
            return
        self.library.save_module_from_header(header, content)

    
    def _refresh_snippet_list(self):
        self.snippet_list.delete(0, "end")
        for name in self.library.list_snippets():
            self.snippet_list.insert("end", name)

    def _add_current_raw_as_snippet(self):
        raw = self.raw_text.get("1.0", "end").strip()
        if not raw:
            return
        name = f"snippet_{len(self.library.list_snippets())+1}"
        self.library.save_snippet(name, raw, tags=["raw_tree", "generated"])
        self._refresh_snippet_list()

    def _on_snippet_select(self, event):
        sel = self.snippet_list.curselection()
        if not sel:
            return
        name = self.snippet_list.get(sel[0])
        snippet = self.library.load_snippet(name)
        self.snippet_view.delete("1.0", "end")
        self.snippet_view.insert("end", snippet)

    def _import_from_clipboard(self):
        """Import the current clipboard text as a uniquely named snippet."""
        try:
            content = self.clipboard_get().strip()
        except tk.TclError:
            return False
        if not content:
            return False

        existing = set(self.library.list_snippets())
        index = 1
        name = f"clipboard_{index}"
        while name in existing:
            index += 1
            name = f"clipboard_{index}"
        self.library.save_snippet(name, content, tags=["clipboard", "imported"])
        self._refresh_snippet_list()
        return True

    def _import_from_clipboard_history(self):
        """Import the current clipboard as a portable history fallback."""
        return self._import_from_clipboard()

    def _module_index_path(self) -> Path:
        return Path(__file__).resolve().parent.parent / "module_index.json"

    def _read_index(self):
        index_path = self._module_index_path()
        if not index_path.exists():
            return {}
        try:
            with index_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}

    def _write_index(self, index):
        path = self._module_index_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(index, handle, indent=2, ensure_ascii=False)

    def save_module_from_header(self, header: str, content: str):
        if not header or not content:
            return None

        match = re.search(r"\(([^)]+)\)", header)
        if not match:
            return None

        rel_path = match.group(1).strip()
        if not rel_path:
            return None

        target = Path(__file__).resolve().parent.parent / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.strip(), encoding="utf-8")

        idx = self._read_index()
        idx[rel_path] = {
            "path": str(target),
            "tags": ["module", "auto_generated"],
            "header": header,
        }
        self._write_index(idx)
        return target

def create_app(library: LibraryManagerType) -> SymantyxWorkbook:
    return SymantyxWorkbook(library)
