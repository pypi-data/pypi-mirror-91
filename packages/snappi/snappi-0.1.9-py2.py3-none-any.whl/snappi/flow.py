from .flowtxrx import FlowTxRx
from .flowrate import FlowRate
from .flowheaderlist import FlowHeaderList
from .snappicommon import SnappiObject
from .flowsize import FlowSize
from .flowduration import FlowDuration


class Flow(SnappiObject):
    _TYPES = {
        'tx_rx': '.flowtxrx.FlowTxRx',
        'packet': '.flowheaderlist.FlowHeaderList',
        'size': '.flowsize.FlowSize',
        'rate': '.flowrate.FlowRate',
        'duration': '.flowduration.FlowDuration',
    }

    def __init__(self, name=None):
        super(Flow, self).__init__()
        self.name = name

    @property
    def tx_rx(self):
        # type: () -> FlowTxRx
        """tx_rx getter

        A container for different types of transmit and receive endpoint containers.The transmit and receive endpoints.

        Returns: obj(snappi.FlowTxRx)
        """
        if 'tx_rx' not in self._properties or self._properties['tx_rx'] is None:
            self._properties['tx_rx'] = FlowTxRx()
        return self._properties['tx_rx']

    @property
    def packet(self):
        # type: () -> FlowHeaderList
        """packet getter

        The header is a list of traffic protocol headers. The order of traffic protocol headers assigned to the list is the order they will appear on the wire.

        Returns: list[obj(snappi.FlowHeader)]
        """
        if 'packet' not in self._properties or self._properties['packet'] is None:
            self._properties['packet'] = FlowHeaderList()
        return self._properties['packet']

    @property
    def size(self):
        # type: () -> FlowSize
        """size getter

        The frame size which overrides the total length of the packetThe size of the packets.

        Returns: obj(snappi.FlowSize)
        """
        if 'size' not in self._properties or self._properties['size'] is None:
            self._properties['size'] = FlowSize()
        return self._properties['size']

    @property
    def rate(self):
        # type: () -> FlowRate
        """rate getter

        The rate of packet transmissionThe transmit rate of the packets.

        Returns: obj(snappi.FlowRate)
        """
        if 'rate' not in self._properties or self._properties['rate'] is None:
            self._properties['rate'] = FlowRate()
        return self._properties['rate']

    @property
    def duration(self):
        # type: () -> FlowDuration
        """duration getter

        A container for different transmit durations. The transmit duration of the packets.

        Returns: obj(snappi.FlowDuration)
        """
        if 'duration' not in self._properties or self._properties['duration'] is None:
            self._properties['duration'] = FlowDuration()
        return self._properties['duration']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value
