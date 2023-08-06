from .layer1ieee8023x import Layer1Ieee8023x
from .layer1ieee8021qbb import Layer1Ieee8021qbb
from .snappicommon import SnappiObject


class Layer1FlowControl(SnappiObject):
    _TYPES = {
        'ieee_802_1qbb': '.layer1ieee8021qbb.Layer1Ieee8021qbb',
        'ieee_802_3x': '.layer1ieee8023x.Layer1Ieee8023x',
    }

    IEEE_802_1QBB = 'ieee_802_1qbb'
    IEEE_802_3X = 'ieee_802_3x'

    def __init__(self, directed_address=None):
        super(Layer1FlowControl, self).__init__()
        self.directed_address = directed_address

    @property
    def ieee_802_1qbb(self):
        # type: () -> Layer1Ieee8021qbb
        """Factory method to create an instance of the Layer1Ieee8021qbb class

        These settings enhance the existing 802.3x pause priority capabilities to enable flow control based on 802.1p priorities (classes of service). 
        """
        if 'ieee_802_1qbb' not in self._properties or self._properties['ieee_802_1qbb'] is None:
            self._properties['ieee_802_1qbb'] = Layer1Ieee8021qbb()
        self.choice = 'ieee_802_1qbb'
        return self._properties['ieee_802_1qbb']

    @property
    def ieee_802_3x(self):
        # type: () -> Layer1Ieee8023x
        """Factory method to create an instance of the Layer1Ieee8023x class

        A container for ieee 802.3x rx pause settings
        """
        if 'ieee_802_3x' not in self._properties or self._properties['ieee_802_3x'] is None:
            self._properties['ieee_802_3x'] = Layer1Ieee8023x()
        self.choice = 'ieee_802_3x'
        return self._properties['ieee_802_3x']

    @property
    def directed_address(self):
        # type: () -> str
        """directed_address getter

        The 48bit mac address that the layer1 port names will listen on for a directed pause. 

        Returns: str
        """
        return self._properties['directed_address']

    @directed_address.setter
    def directed_address(self, value):
        """directed_address setter

        The 48bit mac address that the layer1 port names will listen on for a directed pause. 

        value: str
        """
        self._properties['directed_address'] = value

    @property
    def choice(self):
        # type: () -> Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice, choice]
        """choice getter

        The type of priority flow control.

        Returns: Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of priority flow control.

        value: Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice, choice]
        """
        self._properties['choice'] = value
