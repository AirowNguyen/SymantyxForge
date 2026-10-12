"""
Symantyx Membrane Binder
Priority 1 Debugging — Domain Boundary Layer

The membrane is the boundary between:
- raw hydrated concepts
- structured hypertuples
- semantic forces (TabRs)
- sovereign modules
- substrate and virtual shims

It tags, filters, and binds hypertuples into their correct domain context.
"""

from typing import Dict, Any, List


class MembraneBinder:
    def __init__(self, domain: str = "symantyx"):
        self.domain = domain
        self.rules = {
            "default": ["hydrated", "concept"],
            "cmdline_operator": ["cmd", "operator"],
            "ocr": ["ocr", "ingest"],
            "survey": ["survey", "ingest"],
        }

    # ------------------------------------------------------------------
    # Bind hypertuple to membrane
    # ------------------------------------------------------------------
    def bind(self, hypertuple) -> Dict[str, Any]:
        """
        Attach membrane tags and domain context.
        """
        tags = hypertuple.tags or []
        domain_tags = self.rules.get(hypertuple.domain, self.rules["default"])

        hypertuple.tags = list(set(tags + domain_tags))
        hypertuple.fields["membrane_domain"] = hypertuple.domain
        hypertuple.fields["membrane_tags"] = hypertuple.tags

        return hypertuple

    # ------------------------------------------------------------------
    # Batch bind
    # ------------------------------------------------------------------
    def bind_all(self, hypertuples: List[Any]) -> List[Any]:
        return [self.bind(h) for h in hypertuples]
