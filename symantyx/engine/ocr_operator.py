import pathlib
from typing import Any

# Stub: you can wire this to Tesseract, Azure OCR, etc.


class OcrOperator:
    def __init__(self, engine_hooks: dict[str, Any]):
        self.engine_hooks = engine_hooks  # hydrate, membrane, registry, substrate

    def run(self, image_path: pathlib.Path, config: dict) -> dict:
        # 1. validate
        if not image_path.exists():
            raise FileNotFoundError("image must exist")

        # 2. run OCR backend (stub)
        seed_text = f"[OCR STUB] text from {image_path.name}"

        # 3. hydrate
        hydrate_fn = self.engine_hooks["hydrate"]
        hypertuples = hydrate_fn(seed_text, domain="optic-control-read")

        # 4. bind membrane
        membrane_fn = self.engine_hooks["membrane"]
        bound = membrane_fn(hypertuples, domain="optic-control-read")

        # 5. register
        registry_fn = self.engine_hooks["registry"]
        for h in bound:
            registry_fn(h)

        return {
            "normalized_text": seed_text,
            "hypertuples": bound,
        }
