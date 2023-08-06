from .snappicommon import SnappiObject
from .capturecustomfilter import CaptureCustomFilter
from .capturemacaddressfilter import CaptureMacAddressFilter


class CaptureBasicFilter(SnappiObject):
    _TYPES = {
        'mac_address': '.capturemacaddressfilter.CaptureMacAddressFilter',
        'custom': '.capturecustomfilter.CaptureCustomFilter',
    }

    MAC_ADDRESS = 'mac_address'
    CUSTOM = 'custom'

    def __init__(self, and_operator=None, not_operator=None):
        super(CaptureBasicFilter, self).__init__()
        self.and_operator = and_operator
        self.not_operator = not_operator

    @property
    def mac_address(self):
        # type: () -> CaptureMacAddressFilter
        """Factory method to create an instance of the CaptureMacAddressFilter class

        A container for a mac address capture filter.
        """
        if 'mac_address' not in self._properties or self._properties['mac_address'] is None:
            self._properties['mac_address'] = CaptureMacAddressFilter()
        self.choice = 'mac_address'
        return self._properties['mac_address']

    @property
    def custom(self):
        # type: () -> CaptureCustomFilter
        """Factory method to create an instance of the CaptureCustomFilter class

        A container for a custom capture filter.
        """
        if 'custom' not in self._properties or self._properties['custom'] is None:
            self._properties['custom'] = CaptureCustomFilter()
        self.choice = 'custom'
        return self._properties['custom']

    @property
    def choice(self):
        # type: () -> Union[mac_address, custom, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[mac_address, custom, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[mac_address, custom, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def and_operator(self):
        # type: () -> boolean
        """and_operator getter

        TBD

        Returns: boolean
        """
        return self._properties['and_operator']

    @and_operator.setter
    def and_operator(self, value):
        """and_operator setter

        TBD

        value: boolean
        """
        self._properties['and_operator'] = value

    @property
    def not_operator(self):
        # type: () -> boolean
        """not_operator getter

        TBD

        Returns: boolean
        """
        return self._properties['not_operator']

    @not_operator.setter
    def not_operator(self, value):
        """not_operator setter

        TBD

        value: boolean
        """
        self._properties['not_operator'] = value
