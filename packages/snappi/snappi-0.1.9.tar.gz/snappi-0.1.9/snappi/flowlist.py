from .snappicommon import SnappiList
from .flow import Flow


class FlowList(SnappiList):
    def __init__(self):
        super(FlowList, self).__init__()


    def flow(self, name=None):
        # type: () -> Flow
        """Factory method to create an instance of the snappi.flow.Flow class

        A high level data plane traffic flow. Acts as a container for endpoints, packet headers, packet size, transmit rate and transmit duration.
        """
        item = Flow(name)
        self._add(item)
        return self
