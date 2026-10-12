"""
Symantyx Sovereign Operator: cmdline_operator
Domain: cmdline_operator
Description:
    Executes command-line actions with semantic metadata, membrane binding,
    TabRs indexing, and registry logging. This operator is sovereign:
    no dependencies, no children, no hierarchy — only emergence and entrainment.
"""

import subprocess
import datetime
from pathlib import Path
from typing import Any, Optional


class CmdlineOperator:
    """
    EssenceContainer implementation for:
        id: sym.op.cmdline
        domain: cmdline_operator
    """

    def __init__(self,
                 hydrate_fn,
                 membrane_fn,
                 registry_fn,
                 tabrs_fn):
        """
        engine_hooks:
            hydrate_fn(text, domain)
            membrane_fn(hypertuples, domain)
            registry_fn(hypertuple)
            tabrs_fn(query, mode)
        """
        self.hydrate_fn = hydrate_fn
        self.membrane_fn = membrane_fn
        self.registry_fn = registry_fn
        self.tabrs_fn = tabrs_fn

    # ----------------------------------------------------------------------
    # Core Execution
    # ----------------------------------------------------------------------

    def execute(self,
                cmd_text: str,
                cmd_role: Optional[str] = None,
                cmd_args: Optional[list[str]] = None,
                environment: Optional[dict[str, str]] = None,
                semantic_tags: Optional[list[str]] = None) -> dict[str, Any]:
        """
        Execute a command-line instruction with semantic wrapping.
        """

        if not cmd_text:
            raise ValueError("cmd_text must be provided")

        cmd_args = cmd_args or []
        semantic_tags = semantic_tags or []

        # Build full command
        full_cmd = [cmd_text] + cmd_args

        # Timestamp
        capture_timestamp = datetime.datetime.utcnow().isoformat()

        # ------------------------------------------------------------------
        # 1. Execute raw command
        # ------------------------------------------------------------------
        try:
            proc = subprocess.Popen(
                full_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment
            )
            stdout, stderr = proc.communicate()
        except Exception as exc:
            stdout, stderr = "", f"Execution error: {exc}"

        # ------------------------------------------------------------------
        # 2. Hydrate stdout → hypertuples
        # ------------------------------------------------------------------
        seed_text = stdout.strip() or stderr.strip() or ""
        hypertuples = self.hydrate_fn(seed_text, domain="cmdline_operator")

        # ------------------------------------------------------------------
        # 3. Bind membrane
        # ------------------------------------------------------------------
        bound = self.membrane_fn(hypertuples, domain="cmdline_operator")

        # ------------------------------------------------------------------
        # 4. Register hypertuples
        # ------------------------------------------------------------------
        for h in bound:
            self.registry_fn(h)

        # ------------------------------------------------------------------
        # 5. TabRs indexing
        # ------------------------------------------------------------------
        tabrs_result = self.tabrs_fn(seed_text, mode="AND")

        # ------------------------------------------------------------------
        # 6. Build operator result
        # ------------------------------------------------------------------
        operator_result = {
            "cmd": full_cmd,
            "cmd_role": cmd_role,
            "semantic_tags": semantic_tags,
            "stdout": stdout,
            "stderr": stderr,
            "seed_text": seed_text,
            "hypertuples": bound,
            "tabrs_index": tabrs_result,
            "capture_timestamp": capture_timestamp,
            "session_id": f"cmd-{capture_timestamp}",
            "reproducibility_notes": (
                "cmdline → operator → shim → gateway → registry → TabRs → membrane → operator"
            )
        }

        return operator_result

    # ----------------------------------------------------------------------
    # Utility: run script file
    # ----------------------------------------------------------------------

    def run_script(self, script_path: Path, **kwargs) -> dict[str, Any]:
        """
        Execute a script file (e.g., operator.sh) with semantic wrapping.
        """
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        return self.execute(str(script_path), **kwargs)
