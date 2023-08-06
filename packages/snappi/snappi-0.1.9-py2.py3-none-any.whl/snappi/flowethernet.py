from .flowpattern import FlowPattern
from .snappicommon import SnappiObject


class FlowEthernet(SnappiObject):
    _TYPES = {
        'dst': '.flowpattern.FlowPattern',
        'src': '.flowpattern.FlowPattern',
        'ether_type': '.flowpattern.FlowPattern',
        'pfc_queue': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowEthernet, self).__init__()

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def ether_type(self):
        # type: () -> FlowPattern
        """ether_type getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ether_type' not in self._properties or self._properties['ether_type'] is None:
            self._properties['ether_type'] = FlowPattern()
        return self._properties['ether_type']

    @property
    def pfc_queue(self):
        # type: () -> FlowPattern
        """pfc_queue getter

        A container for packet header field patterns.A container for packet header field patterns.Optional field of 3 bits

        Returns: obj(snappi.FlowPattern)
        """
        if 'pfc_queue' not in self._properties or self._properties['pfc_queue'] is None:
            self._properties['pfc_queue'] = FlowPattern()
        return self._properties['pfc_queue']
