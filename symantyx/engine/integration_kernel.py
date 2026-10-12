"""
Symantyx Integration Kernel
Priority 3 — Dynamic Gateways & Registry-Driven Telos

This kernel:

- reads the registry like environment paths / virtual envs
- discovers new gateways, ports, paths, schemas, containers, membranes
- glues multiple Symantyx apps (e.g., symantyx.app.smessenger, symantyx.canvas)
- animates instruments (schemas, containers, membranes) according to telos
"""
import importlib
import json
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency in some environments
    yaml = None

from backend.essence_container import EssenceContainer
from engine.backend import SymantyxEngine


def _safe_yaml_load(stream):
    if yaml is not None:
        return yaml.safe_load(stream)

    text = stream.read() if hasattr(stream, "read") else str(stream)
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        raise ImportError(
            "PyYAML is required to load Symantyx YAML configuration files. "
            "Install the 'PyYAML' package or provide JSON-compatible config files."
        ) from None


ruleset_path = Path("docs/HydrationRulesetV3.yaml")

with open(ruleset_path, "r", encoding="utf-8") as f:
    HydrationRulesetV3 = _safe_yaml_load(f)

class IntegrationKernel:
    def __init__(self, db_path: Path, registry_path: Path):
        try:
            self.engine = SymantyxEngine(db_path, ruleset=HydrationRulesetV3)
        except TypeError:
            # Some engine versions accept the ruleset as a positional argument instead
            # of a keyword-only parameter.
            self.engine = SymantyxEngine(db_path, HydrationRulesetV3)
        self.registry_path = registry_path

        # dynamic instruments
        self.schemas = {}
        self.containers = {}
        self.membranes = {}
        self.gateways = {}
        self.ports = {}
        self.paths = {}

        self._load_registry()

    # ------------------------------------------------------------
    # Registry Loader — like env paths / virtual env packages
    # ------------------------------------------------------------
    def _load_registry(self):
        """
        Reads a JSON/YAML registry that declares:
        - schemas
        - containers
        - membranes
        - gateways
        - ports
        - paths

        Each entry points to a module/class that can be imported dynamically.
        """
        with open(self.registry_path, "r", encoding="utf-8") as f:
            reg = yaml.safe_load(f)

        # schemas
        for name, spec in reg.get("schemas", {}).items():
            self.schemas[name] = self._dynamic_import(spec)

        # containers (medium-specific, telos-specific)
        for name, spec in reg.get("containers", {}).items():
            self.containers[name] = self._dynamic_import(spec)

        # membranes
        for name, spec in reg.get("membranes", {}).items():
            self.membranes[name] = self._dynamic_import(spec)

        # gateways (entry points for apps / domains)
        for name, spec in reg.get("gateways", {}).items():
            self.gateways[name] = self._dynamic_import(spec)

        # ports (interfaces, channels)
        for name, spec in reg.get("ports", {}).items():
            self.ports[name] = self._dynamic_import(spec)

        # paths (invocation sequences, pipelines)
        for name, spec in reg.get("paths", {}).items():
            self.paths[name] = spec  # often just declarative sequences

                # auto-discovery: merge registry with extension modules
        for category in self.extensions.extensions:
            reg[category].update(self.extensions.get(category))


    def _dynamic_import(self, spec: dict):
        """
        spec = {
          "module": "substrate.photic",
          "class": "PhoticEssenceContainer"
        }
        """
        module = importlib.import_module(spec["module"])
        return getattr(module, spec["class"])

    # ------------------------------------------------------------
    # Universal Integration Entry — per gateway
    # ------------------------------------------------------------
    def integrate(self, text: str, domain: str, gateway: str = "default"):
        """
        text → schemas → container → membranes → transformers → registry

        The gateway defines:
        - which schemas to use
        - which container medium to use
        - which membranes to bind
        - which paths (pipelines) to execute

        This makes the kernel reusable across:
        - symantyx.canvas
        - symantyx.app.smessenger
        - symantyx.cloud.orchestrator
        - symantyx.local.operator
        """
        gw = self.gateways.get(gateway)
        if gw is None:
            raise ValueError(f"Unknown gateway: {gateway}")

        # 1. Resolve gateway config (which schemas, which container, which membranes, which path)
        config = gw.resolve(domain)

        schema_names = config.get("schemas", [])
        container_name = config.get("container")
        membrane_names = config.get("membranes", [])
        path_name = config.get("path")

        # 2. Instantiate instruments
        schema_objs = [self.schemas[name]() for name in schema_names]
        container = EssenceContainer(domain=domain, medium=container_name.replace("_container",""))

        membrane_objs = [self.membranes[name]() for name in membrane_names]
        path_spec = self.paths.get(path_name, {})

        # 3. Apply schemas (substrate slicing, major premise framing, etc.)
        events = []
        for s in schema_objs:
            events.extend(s.slice(text, domain))

        # 4. Hydrate via engine
        hydrated = self.engine.hydrate(text, domain)

        # 5. Bind hydrated hypertuples + events into container
        for h in hydrated:
            packet = container.from_hypertuple(h)
            container.add_packet(packet)

        for ev in events:
            container.bind_event(ev)

        # 6. Execute path (pipeline) — collapse, bind, transform, emit
        # path_spec might look like:
        # {
        #   "steps": ["collapse", "bind", "transform_phonetic", "transform_photic", "emit"]
        # }
        for step in path_spec.get("steps", []):
            if step == "collapse":
                for p in container.packets:
                    container.collapse(p)
            elif step == "bind":
                for p in container.packets:
                    container.bind(p)
            elif step == "transform_phonetic":
                from transformers_4d.PhoneticTransformer import PhoneticTransformer
                t = PhoneticTransformer()
                for p in container.packets:
                    t.transform(p)
            elif step == "transform_photic":
                from transformers_4d.PhoticTransformer import PhoticTransformer
                t = PhoticTransformer()
                for p in container.packets:
                    t.transform(p)
            elif step == "transform_semantic":
                from transformers_4d.SemanticTransformer import SemanticTransformer
                t = SemanticTransformer()
                for p in container.packets:
                    t.transform(p)
            elif step == "transform_spectral":
                from transformers_4d.SpectralTransformer import SpectralTransformer
                t = SpectralTransformer()
                for p in container.packets:
                    t.transform(p)
            elif step == "emit":
                emitted = []
                for p in container.packets:
                 emitted.append(container.emit(p))
                final_hypertuples = emitted


        # 7. Membrane binding (across selected membranes)
        final_hypertuples = [container.emit(p) for p in container.packets]
        for m in membrane_objs:
            final_hypertuples = m.bind_all(final_hypertuples)

        # 8. Registry storage
        for h in final_hypertuples:
            payload_json = self.engine._serialize(h)
            self.engine.registry.store(h, payload_json)

        # 9. Return integrated result
        return {
            "gateway": gateway,
            "domain": domain,
            "essence_container": container.to_dict(),
            "hypertuples": [self.engine._to_dict(h) for h in final_hypertuples],
            "tabrs": self.engine.tabrs.apply_forces(text),
            "path": path_spec
        }
