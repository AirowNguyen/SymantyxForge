from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Hypertuple:
    """
    Core hypertuple model.
    A hypertuple is a semantic packet with fields, tags, and provenance.
    """
    id: str
    domain: str
    fields: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)

    def add_field(self, key: str, value: Any) -> None:
        self.fields[key] = value

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def set_provenance(self, key: str, value: Any) -> None:
        self.provenance[key] = value
