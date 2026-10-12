#This lets you do:
#kernel.extensions.register(
 #   "gateways",
  #  "symantyx.app.smessenger",
  #  "gateways.messenger",
  #  "MessengerGateway"
#)
#
class KernelExtensions:
    def __init__(self):
        self.extensions = {
            "schemas": {},
            "containers": {},
            "membranes": {},
            "gateways": {},
            "ports": {},
            "paths": {}
        }

    def register(self, category: str, name: str, module: str, cls: str):
        self.extensions[category][name] = {
            "module": module,
            "class": cls
        }

    def get(self, category: str):
        return self.extensions.get(category, {})
