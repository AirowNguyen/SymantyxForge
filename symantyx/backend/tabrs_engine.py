from typing import Iterable

class TabRsEngine:
    def __init__(self, registry):
        self.registry = registry  # expects Registry instance

    def search(self, query: str, mode: str = "AND"):
        # Very simple stub: delegate to registry FTS
        return self.registry.search(query, mode)

    def apply_force(self, sets: list[set], mode: str) -> set:
        if mode == "AND":
            return set.intersection(*sets) if sets else set()
        if mode == "OR":
            out = set()
            for s in sets:
                out |= s
            return out
        if mode == "NOT":
            return sets[0] - sets[1] if len(sets) >= 2 else set()
        if mode == "XOR":
            return sets[0] ^ sets[1] if len(sets) >= 2 else set()
        return set()
