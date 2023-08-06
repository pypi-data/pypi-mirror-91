from .flowbitlist import FlowBitList
from .flowbitcounter import FlowBitCounter
from .snappicommon import SnappiObject


class FlowBitPattern(SnappiObject):
    _TYPES = {
        'bitlist': '.flowbitlist.FlowBitList',
        'bitcounter': '.flowbitcounter.FlowBitCounter',
    }

    BITLIST = 'bitlist'
    BITCOUNTER = 'bitcounter'

    def __init__(self):
        super(FlowBitPattern, self).__init__()

    @property
    def bitlist(self):
        # type: () -> FlowBitList
        """Factory method to create an instance of the FlowBitList class

        A pattern which is a list of values.
        """
        if 'bitlist' not in self._properties or self._properties['bitlist'] is None:
            self._properties['bitlist'] = FlowBitList()
        self.choice = 'bitlist'
        return self._properties['bitlist']

    @property
    def bitcounter(self):
        # type: () -> FlowBitCounter
        """Factory method to create an instance of the FlowBitCounter class

        An incrementing pattern
        """
        if 'bitcounter' not in self._properties or self._properties['bitcounter'] is None:
            self._properties['bitcounter'] = FlowBitCounter()
        self.choice = 'bitcounter'
        return self._properties['bitcounter']

    @property
    def choice(self):
        # type: () -> Union[bitlist, bitcounter, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[bitlist, bitcounter, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[bitlist, bitcounter, choice, choice, choice]
        """
        self._properties['choice'] = value
