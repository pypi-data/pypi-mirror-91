from .port import Port
from .snappicommon import SnappiList


class PortList(SnappiList):
    def __init__(self):
        super(PortList, self).__init__()


    def port(self, location=None, name=None):
        # type: () -> Port
        """Factory method to create an instance of the snappi.port.Port class

        An abstract test port.
        """
        item = Port(location, name)
        self._add(item)
        return self
