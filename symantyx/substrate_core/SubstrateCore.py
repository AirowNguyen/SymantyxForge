class SubstrateCore:
    def __init__(self):
        self.registry = {}

    def store(self, essence_packet):
        self.registry[essence_packet.id] = essence_packet

    def retrieve(self, packet_id):
        return self.registry.get(packet_id)

    def bind(self, module_name):
        pass  # sovereign modules choose to bind voluntarily
