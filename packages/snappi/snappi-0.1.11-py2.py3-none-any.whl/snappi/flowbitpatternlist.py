from .snappicommon import SnappiList
from .flowbitpattern import FlowBitPattern
from .flowbitcounter import FlowBitCounter
from .flowbitlist import FlowBitList


class FlowBitPatternList(SnappiList):
    def __init__(self):
        super(FlowBitPatternList, self).__init__()


    def bitpattern(self):
        # type: () -> FlowBitPattern
        """Factory method to create an instance of the snappi.flowbitpattern.FlowBitPattern class

        Container for a bit pattern
        """
        item = FlowBitPattern()
        self._add(item)
        return self

    def bitlist(self, offset=1, length=1, count=1, values=None):
        # type: () -> FlowBitPatternList
        """Factory method to create an instance of the snappi.flowbitlist.FlowBitList class

        A pattern which is a list of values.
        """
        item = FlowBitPattern()
        item.bitlist
        self._add(item)
        return self

    def bitcounter(self, offset=0, length=32, count=1, start=0, step=0):
        # type: () -> FlowBitPatternList
        """Factory method to create an instance of the snappi.flowbitcounter.FlowBitCounter class

        An incrementing pattern
        """
        item = FlowBitPattern()
        item.bitcounter
        self._add(item)
        return self
