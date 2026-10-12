try:
    from ..engine.operators.survey_ingest import ingest  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    from symantyx.engine.operators.survey_ingest import ingest  # type: ignore[reportMissingImports]


def on_new_message(msg):
    ingest(msg)
