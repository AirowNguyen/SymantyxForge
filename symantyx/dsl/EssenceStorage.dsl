# Symantyx Essence Storage DSL
# Priority 2 Debugging — DSL Storage Layer

storage essence {
    target: EssenceContainer

    rule store_packet {
        description: "Store packet in container"
        action: container.packets.append(packet)
    }

    rule remove_packet {
        description: "Remove packet by ID"
        action: container.packets.remove_if(p => p.ID == packet.ID)
    }

    rule update_packet {
        description: "Update packet fields"
        action: container.packets.map(p => p.ID == packet.ID ? packet : p)
    }

    rule serialize_container {
        description: "Serialize container to JSON"
        action: json = serialize(container)
    }

    rule deserialize_container {
        description: "Load container from JSON"
        action: container = deserialize(json)
    }
}
