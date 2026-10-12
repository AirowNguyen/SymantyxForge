class ConversationalMembrane:
    geometry = "cone"
    pressure = "medium"
    velocity = "variable"

    def bind_all(self, hypertuples):
        for h in hypertuples:
            h["membrane"] = "conversational_cone"
        return hypertuples
