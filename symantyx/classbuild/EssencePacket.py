class EssencePacket:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.origin_module = kwargs.get("origin_module")
        self.domain = kwargs.get("domain")
        self.description = kwargs.get("description")
        self.payload = kwargs.get("payload", {})
        self.invariants = kwargs.get("invariants", {})
        self.lineage = kwargs.get("lineage", {})
