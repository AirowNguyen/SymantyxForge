class UniversalSchema:
    def slice(self, text: str, domain: str):
        # placeholder: treat each sentence as an event
        return [{"type": "sentence", "text": t.strip()} for t in text.split(".") if t.strip()]
