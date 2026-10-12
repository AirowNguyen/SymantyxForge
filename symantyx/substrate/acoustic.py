class AcousticEssenceContainer:
    collapse_rate = "diffuse"
    propagation = "pressure_gradient"
    resonance = "low_frequency"

    def collapse(self, packet):
        # acoustic collapse: soften boundaries
        packet["collapse"] = "diffused"
        return packet
