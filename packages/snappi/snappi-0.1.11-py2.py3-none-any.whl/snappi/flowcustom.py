from .flowbitpatternlist import FlowBitPatternList
from .snappicommon import SnappiObject


class FlowCustom(SnappiObject):
    _TYPES = {
        'patterns': '.flowbitpatternlist.FlowBitPatternList',
    }

    def __init__(self, bytes=None):
        super(FlowCustom, self).__init__()
        self.bytes = bytes

    @property
    def bytes(self):
        # type: () -> str
        """bytes getter

        A custom packet header defined as a string of hex bytes. The string MUST contain valid hex characters. Spaces or colons can be part of the bytes but will be discarded This can be used to create a custom protocol from other inputs such as scapy, wireshark, pcap etc.. An example of ethernet/ipv4: '00000000000200000000000108004500001400010000400066e70a0000010a000002'

        Returns: str
        """
        return self._properties['bytes']

    @bytes.setter
    def bytes(self, value):
        """bytes setter

        A custom packet header defined as a string of hex bytes. The string MUST contain valid hex characters. Spaces or colons can be part of the bytes but will be discarded This can be used to create a custom protocol from other inputs such as scapy, wireshark, pcap etc.. An example of ethernet/ipv4: '00000000000200000000000108004500001400010000400066e70a0000010a000002'

        value: str
        """
        self._properties['bytes'] = value

    @property
    def patterns(self):
        # type: () -> FlowBitPatternList
        """patterns getter

        Modify the bytes with bit based patterns

        Returns: list[obj(snappi.FlowBitPattern)]
        """
        if 'patterns' not in self._properties or self._properties['patterns'] is None:
            self._properties['patterns'] = FlowBitPatternList()
        return self._properties['patterns']
