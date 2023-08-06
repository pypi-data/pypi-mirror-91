from .flowstate import FlowState
from .snappicommon import SnappiList


class FlowStateList(SnappiList):
    def __init__(self):
        super(FlowStateList, self).__init__()


    def state(self, name=None, transmit='None'):
        # type: () -> FlowState
        """Factory method to create an instance of the snappi.flowstate.FlowState class

        TBD
        """
        item = FlowState(name, transmit)
        self._add(item)
        return self
