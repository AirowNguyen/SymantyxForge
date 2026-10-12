class ContainerShim:
    def __init__(self):
        self.routes = {}

    def register(self, module_name, handler):
        self.routes[module_name] = handler

    def dispatch(self, module_name, essence_packet):
        handler = self.routes.get(module_name)
        if handler:
            return handler(essence_packet)
