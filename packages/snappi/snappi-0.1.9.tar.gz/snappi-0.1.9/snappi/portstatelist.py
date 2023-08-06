from .portstate import PortState
from .snappicommon import SnappiList


class PortStateList(SnappiList):
    def __init__(self):
        super(PortStateList, self).__init__()


    def state(self, name=None, link='None', capture='None'):
        # type: () -> PortState
        """Factory method to create an instance of the snappi.portstate.PortState class

        TBD
        """
        item = PortState(name, link, capture)
        self._add(item)
        return self
