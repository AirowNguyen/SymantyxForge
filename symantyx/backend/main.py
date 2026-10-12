from pathlib import Path
try:
    from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
except ImportError as exc:
    raise ImportError(
        "FastAPI is not installed in the active Python environment. "
        "Install it with `python -m pip install fastapi`."
    ) from exc
from engine.integration_kernel import IntegrationKernel

app = FastAPI()

kernel = IntegrationKernel(
    db_path=Path("db.sqlite"),
    registry_path=Path("registry/symantyx_registry.json")
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Symantyx backend running"}

@app.post("/hydrate")
def hydrate_text(payload: dict):
    text = payload["text"]
    domain = payload.get("domain", "default")
    return kernel.integrate(text, domain)
