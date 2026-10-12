class VisualMembrane:
    geometry = "cube"
    pressure = "low"
    velocity = "high"

    def bind_all(self, hypertuples):
        for h in hypertuples:
            h["membrane"] = "visual_cube"
        return hypertuples
