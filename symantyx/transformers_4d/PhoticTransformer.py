"""
Symantyx Photic Transformer
Priority 2 Debugging — Visual Layer

Transforms EssencePackets into photic (visual) geometry.
"""

class PhoticTransformer:
    def __init__(self):
        pass

    def compute_geometry(self, packet):
        word = packet.fields.get("word", "")
        length = len(word)

        return {
            "radius": 20 + length * 2,
            "color": "#4CAF50" if length % 2 == 0 else "#FF5722",
            "glow": length > 6
        }

    def transform(self, packet):
        packet.fields["photic_geometry"] = self.compute_geometry(packet)
        return packet
