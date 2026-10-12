class PhoticEssenceContainer:
    collapse_rate = "instant"
    propagation = "line_of_sight"
    resonance = "high_frequency"

    def collapse(self, packet):
        # photic collapse: sharp boundary formation
        packet["collapse"] = "sharp"
        return packet
