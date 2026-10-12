import yaml
from pathlib import Path

def load():
    path = Path(__file__).with_suffix(".yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
