class MajorPremiseContainer:
    def frame(self, container):
        # placeholder: tag container with evidentiary notes
        container.evidentiary_notes = {
            "repeatability": "unknown",
            "limitations": "not yet assessed",
            "admissibility_support": "pending"
        }
        return container

    def to_dict(self):
        return getattr(self, "evidentiary_notes", {})
