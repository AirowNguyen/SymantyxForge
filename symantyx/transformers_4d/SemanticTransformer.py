"""
Symantyx Semantic Transformer
Priority 2 Debugging — Meaning Layer

Transforms EssencePackets into semantic vectors.
"""

class SemanticTransformer:
    def __init__(self):
        pass

    def compute_semantic_vector(self, packet):
        tags = packet.fields.get("tags", [])
        root = packet.fields.get("root", "")
        origin = packet.fields.get("origin", "")

        return {
            "tag_count": len(tags),
            "root_length": len(root),
            "origin_length": len(origin)
        }

    def transform(self, packet):
        packet.fields["semantic_vector"] = self.compute_semantic_vector(packet)
        return packet
