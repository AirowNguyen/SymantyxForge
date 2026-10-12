# Symantyx Collapse Operators
# Priority 2 Debugging — DSL Operator Layer

operator collapse {
    input: EssencePacket
    output: EssencePacket

    rule collapse_to_root {
        description: "Reduce packet to its etymological root"
        action: packet.fields.word = packet.fields.root
    }

    rule collapse_to_origin {
        description: "Reduce packet to its origin language"
        action: packet.fields.word = packet.fields.origin
    }

    rule collapse_to_definition {
        description: "Reduce packet to its definition"
        action: packet.fields.word = packet.fields.definition
    }

    rule collapse_strip_tags {
        description: "Remove all semantic tags"
        action: packet.fields.tags = []
    }
}

operator bind {
    input: EssencePacket
    output: EssencePacket

    rule bind_membrane {
        description: "Bind packet to membrane domain"
        action: packet.fields.membrane_domain = packet.domain
    }

    rule bind_tabrs {
        description: "Attach TabRs force vectors"
        action: packet.fields.tabrs_forces = tabrs.compute(packet.fields.word)
    }
}

operator emit {
    input: EssencePacket
    output: Hypertuple

    rule emit_hypertuple {
        description: "Convert packet into hypertuple"
        action: hypertuple = engine.emit(packet)
    }
}
