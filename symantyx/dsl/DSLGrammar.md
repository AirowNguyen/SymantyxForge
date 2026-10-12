# Symantyx DSL Grammar
Priority 2 Debugging — Linguistic Substrate

The Symantyx DSL is a sovereign grammar for manipulating EssenceContainers,
EssencePackets, hypertuples, membrane bindings, and TabRs forces.

---

## 1. Grammar Overview

The DSL consists of:
- operators
- rules
- actions
- storage directives
- collapse directives
- emit directives

---

## 2. Syntax

### Operator Definition
operator <name> {
input: <type>
output: <type>

rule <rule_name> {
description: "<text>"
action: <expression>
}
}

### Storage Definition
storage <name> {
target: <type>

rule <rule_name> {
description: "<text>"
action: <expression>
}
}


---

## 3. Expressions

Expressions may reference:
- packet.fields.<field>
- packet.tags
- container.packets
- tabrs.compute(<word>)
- engine.emit(<packet>)
- serialize(<object>)
- deserialize(<json>)

---

## 4. Collapse Semantics

Collapse operators reduce semantic complexity:
- collapse_to_root
- collapse_to_origin
- collapse_to_definition
- collapse_strip_tags

These are used by:
- transformers
- membrane binding
- canvas interactions
- operators

---

## 5. Binding Semantics

Binding operators attach:
- membrane domain
- membrane tags
- TabRs forces

---

## 6. Emission Semantics

Emission operators convert:
- EssencePacket → Hypertuple
- Hypertuple → Canvas Node
- Canvas Node → Registry Entry

---

## 7. Storage Semantics

Storage operators manage:
- EssenceContainers
- packet lists
- serialization
- deserialization

---

## 8. Sovereign Constraints

The DSL must:
- preserve Essence invariants
- respect membrane boundaries
- remain deterministic
- remain serializable
- remain canvas‑renderable
