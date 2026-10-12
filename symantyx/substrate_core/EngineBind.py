class EngineBind:
    def __init__(self, substrate):
        self.substrate = substrate

    def attach(self, module):
        # sovereign module chooses to attach
        return True

    def detach(self, module):
        return True
