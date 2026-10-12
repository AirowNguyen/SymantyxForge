"""
EssenceContainer Runtime
Symantyx · Essence Layer
Handles packet lifecycle, medium physics, membrane binding, and hypertuple emission.
"""

class EssenceContainer:
    def __init__(self, domain: str, medium: str = "photic"):
        self.domain = domain
        self.medium = medium
        self.packets = []
        self.metadata = {
            "domain": domain,
            "medium": medium,
            "count": 0
        }

    def add(self, packet):
        self.packets.append(packet)
        self.metadata["count"] = len(self.packets)

    def collapse(self, packet):
        # medium-specific collapse physics
        if self.medium == "photic":
            packet["collapse"] = "sharp"
        elif self.medium == "acoustic":
            packet["collapse"] = "diffused"
        else:
            packet["collapse"] = "neutral"
        return packet

    def bind(self, packet, membrane):
        # membrane geometry binding
        packet["membrane"] = membrane.geometry
        return packet

    def emit(self, packet):
        # hypertuple emission
        return {
            "domain": self.domain,
            "medium": self.medium,
            "packet": packet
        }

    def to_dict(self):
        return {
            "domain": self.domain,
            "medium": self.medium,
            "packet_count": len(self.packets),
            "packets": self.packets
        }
