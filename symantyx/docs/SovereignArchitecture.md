**SovereignModule:**

&#x20; **name: "Symantyx.Sovereign.Substrate"**

&#x20; **version: "1.0.0"**

&#x20; **authority\_scope:**

&#x20;   **- "Essence definition"**

&#x20;   **- "Substrate law"**

&#x20;   **- "Cross-agent invariants"**



&#x20; **structure\_tree:**

&#x20;   **root: "src/symantyx/sovereign"**

&#x20;   **nodes:**

&#x20;     **- name: "essence"**

&#x20;       **path: "src/symantyx/sovereign/essence"**

&#x20;       **children:**

&#x20;         **- "EssenceContainer.yaml"**

&#x20;         **- "EssencePacket.yaml"**

&#x20;     **- name: "substrate\_core"**

&#x20;       **path: "src/symantyx/sovereign/substrate\_core"**

&#x20;       **children:**

&#x20;         **- "SubstrateCore.py"**

&#x20;         **- "EngineBind.py"**

&#x20;         **- "ContainerShim.py"**

&#x20;     **- name: "transformers\_4d"**

&#x20;       **path: "src/symantyx/sovereign/transformers\_4d"**

&#x20;       **children:**

&#x20;         **- "PhoticTransformer.py"**

&#x20;         **- "PhoneticTransformer.py"**

&#x20;         **- "SemanticTransformer.py"**

&#x20;         **- "SpectralTransformer.py"**

&#x20;     **- name: "dsl"**

&#x20;       **path: "src/symantyx/sovereign/dsl"**

&#x20;       **children:**

&#x20;         **- "EssenceStorage.dsl"**

&#x20;         **- "CollapseOperators.dsl"**

&#x20;     **- name: "docs"**

&#x20;       **path: "docs/sovereign"**

&#x20;       **children:**

&#x20;         **- "SovereignModule.md"**

&#x20;         **- "4DTransformerCreators.md"**

&#x20;         **- "SubstrateCoreSpec.md"**

&#x20;         **- "EssencePacketSpec.md"**



