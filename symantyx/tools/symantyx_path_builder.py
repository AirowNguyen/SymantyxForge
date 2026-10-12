#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          Symantyx Path Builder  ·  v1.0.0                   ║
║  Converts indented Raw-text tree notation into real          ║
║  directories and files on disk.                              ║
║                                                              ║
║  Supports:                                                   ║
║    · Symantyx / Palette Raw-text format                      ║
║    · Inline ← # · ▸ // annotations (stripped automatically) ║
║    · Trailing-/ directory markers                            ║
║    · Extension-based file detection                          ║
║    · Mixed indentation (spaces / tabs)                       ║
║    · Dry-run preview mode                                    ║
║    · Export log to .txt                                      ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    python symantyx_path_builder.py
    python symantyx_path_builder.py --cli tree.txt C:/output

Requirements: Python 3.8+  (tkinter ships with standard Python)
On Linux:     sudo apt install python3-tk
"""

import os
import re
import sys
import argparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from datetime import datetime


# ══════════════════════════════════════════════════════════════
#  ENGINE — tree parsing + filesystem creation
# ══════════════════════════════════════════════════════════════

_INLINE_STRIP = re.compile(r'\s*(←|#|·|▸|▹|//|;)\s.*$')
_TREE_CHARS   = re.compile(r'^[│├└─┬┐┤┘╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬|+`\- ]+')


def _detect_indent_unit(lines: list) -> int:
    sizes = set()
    for line in lines:
        expanded = line.expandtabs(4)
        stripped = expanded.lstrip(' ')
        if stripped.strip():
            leading = len(expanded) - len(stripped)
            if leading > 0:
                sizes.add(leading)
    return min(sizes) if sizes else 4


def _clean_label(raw: str) -> str:
    cleaned = _INLINE_STRIP.sub('', raw)
    return cleaned.rstrip(':').strip()


def _is_comment(s: str) -> bool:
    if not s:
        return True
    if s[0] in ('#', '←', '·', '▸', '▹', '►', '▶'):
        return True
    if s.startswith('//') or s.startswith('/*'):
        return True
    if re.match(r'^\d+[\.\)]\s', s) and '/' not in s and '.' not in s.split()[0]:
        return True
    return False


def _is_dir_node(name: str) -> bool:
    if not name:
        return False
    if name.endswith('/') or name.endswith('\\'):
        return True
    base = os.path.basename(name.rstrip('/\\'))
    return '.' not in base


def parse_tree(raw_text: str) -> list:
    """
    Parse indented Raw-text into a list of (depth, name, is_dir) tuples.

    Handles:
      · Spaces and tabs (tabs expanded to 4 spaces)
      · Inline ← # · ▸ ▹ // ; annotations
      · Unicode box-drawing tree characters
      · Pure comment lines
    """
    lines = raw_text.splitlines()
    indent_unit = _detect_indent_unit(lines)
    nodes = []

    for line in lines:
        expanded = line.expandtabs(4)
        stripped_left = expanded.lstrip(' ')
        label = stripped_left.strip()

        if _is_comment(label):
            continue

        leading_spaces = len(expanded) - len(stripped_left)
        depth = leading_spaces // indent_unit if indent_unit else 0

        name = _clean_label(label)
        name = _TREE_CHARS.sub('', name).strip()
        if not name or _is_comment(name):
            continue

        is_dir = _is_dir_node(name)
        name = name.rstrip('/\\')

        nodes.append((depth, name, is_dir))

    return nodes


def nodes_to_paths(nodes: list, base_path) -> list:
    """Convert (depth, name, is_dir) list into full filesystem Paths."""
    results = []
    stack = []

    for depth, name, is_dir in nodes:
        stack = stack[:depth]
        stack.append(name)
        full_path = Path(base_path).joinpath(*stack)
        results.append((full_path, is_dir))

    return results


def build_paths(raw_text: str, base_path, create_files: bool = True,
                dry_run: bool = False) -> tuple:
    """
    Main build function. Returns (log_lines, created, skipped, errors).

    Args:
        raw_text:     Indented tree text.
        base_path:    Root directory for creation.
        create_files: When False, only directories are created.
        dry_run:      When True, nothing is written to disk.
    """
    nodes = parse_tree(raw_text)
    if not nodes:
        return ["[WARN] No valid nodes found in the input text."], 0, 0, 0

    paths = nodes_to_paths(nodes, base_path)
    log = []
    created = skipped = errors = 0
    ts = datetime.now().strftime('%H:%M:%S')

    log.append(f"[{ts}]  Base  →  {base_path}")
    log.append(f"[{ts}]  Nodes →  {len(nodes)}   Dry-run: {dry_run}")
    log.append("─" * 62)

    for full_path, is_dir in paths:
        rel = full_path.relative_to(base_path)
        tag = "[DIR ] " if is_dir else "[FILE]"

        if dry_run:
            log.append(f"  {tag}  {rel}")
            created += 1
            continue

        try:
            if is_dir:
                if full_path.exists():
                    log.append(f"  {tag}  EXISTS    {rel}"); skipped += 1
                else:
                    full_path.mkdir(parents=True, exist_ok=True)
                    log.append(f"  {tag}  CREATED   {rel}"); created += 1
            else:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                if create_files:
                    if full_path.exists():
                        log.append(f"  {tag}  EXISTS    {rel}"); skipped += 1
                    else:
                        full_path.touch()
                        log.append(f"  {tag}  CREATED   {rel}"); created += 1
                else:
                    log.append(f"  {tag}  SKIPPED   {rel}  (files disabled)"); skipped += 1
        except Exception as exc:
            log.append(f"  [ERR!]  FAILED    {rel}  →  {exc}"); errors += 1

    log.append("─" * 62)
    if dry_run:
        log.append(f"  Preview complete — {created} item(s) listed.")
    else:
        log.append(
            f"  Done — created: {created}   skipped: {skipped}   errors: {errors}"
        )

    return log, created, skipped, errors


# ══════════════════════════════════════════════════════════════
#  COLOUR PALETTE
# ══════════════════════════════════════════════════════════════

_C = {
    "bg":      "#1e1e2e",
    "panel":   "#2a2a3e",
    "panel2":  "#222234",
    "accent":  "#7c6af7",
    "accent2": "#5a48d4",
    "fg":      "#cdd6f4",
    "dim":     "#6c7086",
    "green":   "#a6e3a1",
    "yellow":  "#f9e2af",
    "red":     "#f38ba8",
    "blue":    "#89b4fa",
    "surface": "#12121e",
}

_MONO    = ("Consolas", 10) if sys.platform == "win32" else ("Menlo", 10)
_MONO_LG = ("Consolas", 11) if sys.platform == "win32" else ("Menlo", 11)
_UI      = ("Segoe UI", 10) if sys.platform == "win32" else ("SF Pro Text", 10)
_UI_B    = ("Segoe UI Semibold", 10, "bold") if sys.platform == "win32" else ("SF Pro Text", 10, "bold")
_UI_LG   = ("Segoe UI Semibold", 13, "bold") if sys.platform == "win32" else ("SF Pro Display", 13, "bold")
_UI_SM   = ("Segoe UI", 9) if sys.platform == "win32" else ("SF Pro Text", 9)


# ══════════════════════════════════════════════════════════════
#  SAMPLE TREE
# ══════════════════════════════════════════════════════════════

SAMPLE_TREE = """\
tools/
    capture_url.ps1
    convert_to_md.py          ← markdown converter
    run_capture_and_convert.bat

docs/
    README.md
    api/
        endpoints.md
        auth.md

src/
    core/
        engine.py
        parser.py
        builder.py
    gui/
        app.py
        widgets.py
    utils/
        logger.py
        helpers.py
    __init__.py

tests/
    test_engine.py
    test_parser.py

config/
    settings.toml
    manifest.json
"""


# ══════════════════════════════════════════════════════════════
#  GUI
# ══════════════════════════════════════════════════════════════

class SymantyxApp(tk.Tk):
    """Main application window for the Symantyx Path Builder."""

    def __init__(self):
        super().__init__()
        self.title("Symantyx Path Builder  ·  v1.0.0")
        self.configure(bg=_C["bg"])
        self.resizable(True, True)
        self.minsize(920, 640)
        self.geometry("1140x740")

        self._build_styles()
        self._build_ui()
        self._apply_tag_colours()

    # ── Styles ────────────────────────────────────────────────

    def _build_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".",              background=_C["bg"],    foreground=_C["fg"],  font=_UI)
        s.configure("TFrame",         background=_C["bg"])
        s.configure("Panel.TFrame",   background=_C["panel"])
        s.configure("Panel2.TFrame",  background=_C["panel2"])
        s.configure("TLabel",         background=_C["bg"],    foreground=_C["fg"])
        s.configure("Dim.TLabel",     background=_C["bg"],    foreground=_C["dim"],    font=_UI_SM)
        s.configure("Panel.TLabel",   background=_C["panel"], foreground=_C["fg"])
        s.configure("PanelDim.TLabel",background=_C["panel"], foreground=_C["dim"],    font=_UI_SM)
        s.configure("PanelHead.TLabel",background=_C["panel"],foreground=_C["accent"], font=_UI_B)
        s.configure("TCheckbutton",   background=_C["bg"],    foreground=_C["fg"],
                    indicatorcolor=_C["accent"], selectcolor=_C["accent"])
        s.map("TCheckbutton", background=[("active", _C["bg"])])
        s.configure("Panel.TCheckbutton", background=_C["panel"], foreground=_C["fg"],
                    indicatorcolor=_C["accent"], selectcolor=_C["accent"])
        s.map("Panel.TCheckbutton", background=[("active", _C["panel"])])
        s.configure("Accent.TButton", background=_C["accent"], foreground="#ffffff",
                    relief="flat", padding=(14, 7), font=_UI_B)
        s.map("Accent.TButton",
              background=[("active", _C["accent2"]), ("pressed", _C["accent2"])])
        s.configure("Muted.TButton",  background=_C["panel"], foreground=_C["fg"],
                    relief="flat", padding=(10, 6))
        s.map("Muted.TButton",
              background=[("active", "#3a3a50"), ("pressed", "#3a3a50")])

    # ── Layout ────────────────────────────────────────────────

    def _build_ui(self):
        self._build_topbar()
        self._build_body()
        self._build_statusbar()

    def _build_topbar(self):
        bar = tk.Frame(self, bg=_C["panel"], height=48)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Label(bar, text="  ⬡  Symantyx Path Builder",
                 bg=_C["panel"], fg=_C["fg"], font=_UI_LG).pack(side="left", padx=12)
        tk.Label(bar, text="Raw-text tree  →  real filesystem paths",
                 bg=_C["panel"], fg=_C["dim"], font=_UI_SM).pack(side="left")
        tk.Label(bar,
                 text="Ctrl+Return = Build    Ctrl+P = Preview    Ctrl+L = Sample  ",
                 bg=_C["panel"], fg=_C["dim"], font=_UI_SM).pack(side="right")

    def _build_body(self):
        paned = tk.PanedWindow(self, orient="horizontal",
                               bg=_C["bg"], sashwidth=6, sashpad=2,
                               relief="flat", bd=0)
        paned.pack(fill="both", expand=True, padx=10, pady=8)
        self._build_left(paned)
        self._build_right(paned)

    def _build_left(self, paned):
        left = ttk.Frame(paned)
        paned.add(left, minsize=380)

        tk.Label(left, text="Raw Tree Input",
                 bg=_C["bg"], fg=_C["accent"], font=_UI_B).pack(anchor="w")
        tk.Label(left,
                 text="Paste your indented tree.  "
                      "Dirs = no extension or trailing /    "
                      "Files = have .ext    "
                      "Annotations (← # ·) stripped automatically.",
                 bg=_C["bg"], fg=_C["dim"], font=_UI_SM,
                 wraplength=440, justify="left").pack(anchor="w", pady=(2, 6))

        self.input_text = scrolledtext.ScrolledText(
            left, wrap="none",
            bg=_C["panel"], fg=_C["fg"],
            insertbackground=_C["fg"],
            font=_MONO_LG, relief="flat", bd=0,
            padx=10, pady=10,
            selectbackground=_C["accent"],
        )
        self.input_text.pack(fill="both", expand=True)

        self.input_text.bind("<Control-Return>", lambda e: self._build())
        self.input_text.bind("<Control-p>",      lambda e: self._preview())
        self.bind("<Control-l>",                 lambda e: self._load_sample())

        row = ttk.Frame(left)
        row.pack(fill="x", pady=(6, 0))
        ttk.Button(row, text="Load Sample",  style="Muted.TButton",
                   command=self._load_sample).pack(side="left")
        ttk.Button(row, text="Clear Input",  style="Muted.TButton",
                   command=lambda: self.input_text.delete("1.0", "end")
                   ).pack(side="left", padx=6)
        ttk.Button(row, text="Open File…",   style="Muted.TButton",
                   command=self._open_file).pack(side="left")

    def _build_right(self, paned):
        right = ttk.Frame(paned)
        paned.add(right, minsize=380)

        # Base path
        bp = ttk.Frame(right, style="Panel.TFrame")
        bp.pack(fill="x", pady=(0, 8))
        ttk.Label(bp, text="Base Path", style="PanelHead.TLabel").pack(
            anchor="w", padx=10, pady=(8, 2))
        ttk.Label(bp,
                  text="All directories and files will be created relative to this folder.",
                  style="PanelDim.TLabel").pack(anchor="w", padx=10)
        prow = ttk.Frame(bp, style="Panel.TFrame")
        prow.pack(fill="x", padx=10, pady=(4, 10))
        self.base_path_var = tk.StringVar(value=str(Path.home()))
        entry = tk.Entry(prow,
                         textvariable=self.base_path_var,
                         bg=_C["panel2"], fg=_C["fg"],
                         insertbackground=_C["fg"],
                         relief="flat", bd=0, font=_MONO,
                         highlightthickness=1,
                         highlightbackground=_C["dim"],
                         highlightcolor=_C["accent"])
        entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        ttk.Button(prow, text="Browse…", style="Muted.TButton",
                   command=self._browse_base).pack(side="left")

        # Options
        op = ttk.Frame(right, style="Panel.TFrame")
        op.pack(fill="x", pady=(0, 8))
        ttk.Label(op, text="Options", style="PanelHead.TLabel").pack(
            anchor="w", padx=10, pady=(8, 4))
        self.create_files_var = tk.BooleanVar(value=True)
        self.dry_run_var      = tk.BooleanVar(value=False)
        self.open_after_var   = tk.BooleanVar(value=False)
        for var, text in [
            (self.create_files_var, "Create files  (not just directories)"),
            (self.dry_run_var,      "Dry run  —  preview only, nothing written to disk"),
            (self.open_after_var,   "Open base folder in Explorer / Finder when done"),
        ]:
            tk.Checkbutton(op, text=text, variable=var,
                           bg=_C["panel"], fg=_C["fg"],
                           selectcolor=_C["accent"],
                           activebackground=_C["panel"],
                           activeforeground=_C["fg"],
                           relief="flat", bd=0, font=_UI_SM
                           ).pack(anchor="w", padx=16, pady=2)
        tk.Frame(op, bg=_C["panel"], height=6).pack()

        # Action buttons
        arow = ttk.Frame(right)
        arow.pack(fill="x", pady=(0, 8))
        ttk.Button(arow, text="⬡  Preview",
                   style="Muted.TButton",  command=self._preview).pack(side="left")
        ttk.Button(arow, text="▶  Build Paths",
                   style="Accent.TButton", command=self._build).pack(side="left", padx=(8, 0))
        ttk.Button(arow, text="Export Log",
                   style="Muted.TButton",  command=self._export_log).pack(side="right")
        ttk.Button(arow, text="Clear Log",
                   style="Muted.TButton",  command=self._clear_log).pack(side="right", padx=(0, 6))

        # Output log
        tk.Label(right, text="Output Log",
                 bg=_C["bg"], fg=_C["accent"], font=_UI_B).pack(anchor="w", pady=(0, 4))
        self.output_text = scrolledtext.ScrolledText(
            right, wrap="none",
            bg=_C["surface"], fg=_C["fg"],
            insertbackground=_C["fg"],
            font=_MONO, relief="flat", bd=0,
            padx=10, pady=10,
            state="disabled",
        )
        self.output_text.pack(fill="both", expand=True)

    def _apply_tag_colours(self):
        t = self.output_text
        t.tag_config("dir",     foreground=_C["blue"])
        t.tag_config("file",    foreground=_C["green"])
        t.tag_config("skip",    foreground=_C["yellow"])
        t.tag_config("err",     foreground=_C["red"])
        t.tag_config("header",  foreground=_C["dim"])
        t.tag_config("summary", foreground=_C["fg"])
        t.tag_config("preview", foreground=_C["yellow"])

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=_C["panel"], height=26)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self.status_var = tk.StringVar(
            value="Ready  ·  Ctrl+Return = Build   Ctrl+P = Preview")
        tk.Label(bar, textvariable=self.status_var,
                 bg=_C["panel"], fg=_C["dim"], font=_UI_SM,
                 anchor="w").pack(side="left", padx=12, pady=4)

    # ── Actions ───────────────────────────────────────────────

    def _browse_base(self):
        folder = filedialog.askdirectory(
            title="Select Base Path", initialdir=self.base_path_var.get())
        if folder:
            self.base_path_var.set(folder)

    def _load_sample(self):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", SAMPLE_TREE)
        self.status_var.set("Sample loaded — edit then press ▶ Build Paths.")

    def _open_file(self):
        path = filedialog.askopenfilename(
            title="Open tree text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            try:
                content = Path(path).read_text(encoding="utf-8", errors="replace")
                self.input_text.delete("1.0", "end")
                self.input_text.insert("1.0", content)
                self.status_var.set(f"Loaded: {path}")
            except Exception as exc:
                messagebox.showerror("Open File Error", str(exc))

    def _get_raw(self) -> str:
        return self.input_text.get("1.0", "end").strip()

    def _preview(self):
        self._run(force_dry=True)

    def _build(self):
        base = self.base_path_var.get().strip()
        dry  = self.dry_run_var.get()
        if not dry:
            raw = self._get_raw()
            if not raw:
                messagebox.showwarning("No Input",
                    "Paste a path tree into the left panel first.")
                return
            if not messagebox.askyesno(
                "Confirm Build",
                f"This will create directories and files inside:\n\n"
                f"  {base}\n\nProceed?"
            ):
                return
        self._run()

    def _run(self, force_dry: bool = False):
        raw = self._get_raw()
        if not raw:
            messagebox.showwarning("No Input",
                "Paste a path tree into the left panel first.")
            return
        base = self.base_path_var.get().strip()
        if not base:
            messagebox.showwarning("No Base Path",
                "Set a base path before building.")
            return

        dry          = self.dry_run_var.get() or force_dry
        create_files = self.create_files_var.get()
        self.status_var.set("Working…")
        self.update_idletasks()

        try:
            log_lines, created, skipped, errors = build_paths(
                raw, base, create_files=create_files, dry_run=dry)
        except Exception as exc:
            messagebox.showerror("Engine Error", str(exc))
            self.status_var.set("Error — see message.")
            return

        self._write_log(log_lines, preview=dry or force_dry)

        if dry or force_dry:
            self.status_var.set(f"Preview — {created} item(s) listed.")
        else:
            icon = "✓" if errors == 0 else "⚠"
            self.status_var.set(
                f"{icon}  Done — created: {created}   "
                f"skipped: {skipped}   errors: {errors}")
            if self.open_after_var.get() and errors == 0:
                _open_in_explorer(base)

    def _write_log(self, lines, preview=False):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        if preview:
            self.output_text.insert("end",
                "  ── PREVIEW MODE — nothing written to disk ──\n\n", "preview")
        for line in lines:
            lo = line.lower()
            if   "[dir "  in lo:                      tag = "dir"
            elif "[file]" in lo:                      tag = "file"
            elif "exists" in lo or "skip" in lo:      tag = "skip"
            elif "[err"   in lo or "failed" in lo:    tag = "err"
            elif "done"   in lo or "complete" in lo:  tag = "summary"
            elif line.startswith("─"):                tag = "header"
            else:                                     tag = "header"
            self.output_text.insert("end", line + "\n", tag)
        self.output_text.configure(state="disabled")
        self.output_text.see("end")

    def _clear_log(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        self.status_var.set("Log cleared.")

    def _export_log(self):
        content = self.output_text.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Nothing to Export", "The log is empty.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"symantyx_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        if path:
            try:
                Path(path).write_text(content, encoding="utf-8")
                self.status_var.set(f"Log saved → {path}")
            except Exception as exc:
                messagebox.showerror("Export Error", str(exc))


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════

def _open_in_explorer(path: str):
    try:
        if   sys.platform == "win32":  os.startfile(path)
        elif sys.platform == "darwin": os.system(f'open "{path}"')
        else:                          os.system(f'xdg-open "{path}"')
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════
#  CLI MODE
# ══════════════════════════════════════════════════════════════

def _cli_main():
    parser = argparse.ArgumentParser(
        description="Symantyx Path Builder — CLI mode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python symantyx_path_builder.py --cli tree.txt C:/Projects/MyModule
  python symantyx_path_builder.py --cli tree.txt . --no-files --dry-run
        """)
    parser.add_argument("tree_file",  help="Path to the .txt file containing the indented tree")
    parser.add_argument("base_path",  help="Base directory where paths will be created")
    parser.add_argument("--no-files", action="store_true",
                        help="Create directories only, no empty files")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Preview only — nothing written to disk")

    args = parser.parse_args(sys.argv[2:])
    raw  = Path(args.tree_file).read_text(encoding="utf-8", errors="replace")
    log, created, skipped, errors = build_paths(
        raw, args.base_path,
        create_files=not args.no_files,
        dry_run=args.dry_run,
    )
    for line in log:
        print(line)
    sys.exit(0 if errors == 0 else 1)


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        _cli_main()
    else:
        app = SymantyxApp()
        app.mainloop()
