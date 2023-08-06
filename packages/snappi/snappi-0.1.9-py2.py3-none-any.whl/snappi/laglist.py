from .lag import Lag
from .snappicommon import SnappiList


class LagList(SnappiList):
    def __init__(self):
        super(LagList, self).__init__()


    def lag(self, port_names=None, name=None):
        # type: () -> Lag
        """Factory method to create an instance of the snappi.lag.Lag class

        A container for LAG settings.
        """
        item = Lag(port_names, name)
        self._add(item)
        return self
