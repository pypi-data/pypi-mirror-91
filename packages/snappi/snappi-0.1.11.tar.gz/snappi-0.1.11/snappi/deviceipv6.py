from .devicepattern import DevicePattern
from .snappicommon import SnappiObject
from .deviceethernet import DeviceEthernet


class DeviceIpv6(SnappiObject):
    _TYPES = {
        'address': '.devicepattern.DevicePattern',
        'gateway': '.devicepattern.DevicePattern',
        'prefix': '.devicepattern.DevicePattern',
        'ethernet': '.deviceethernet.DeviceEthernet',
    }

    def __init__(self, name=None):
        super(DeviceIpv6, self).__init__()
        self.name = name

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def gateway(self):
        # type: () -> DevicePattern
        """gateway getter

        A container for emulated device property patterns.A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        if 'gateway' not in self._properties or self._properties['gateway'] is None:
            self._properties['gateway'] = DevicePattern()
        return self._properties['gateway']

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def ethernet(self):
        # type: () -> DeviceEthernet
        """ethernet getter

        Emulated ethernet protocol. A top level in the emulated device stack.Emulated ethernet protocol. A top level in the emulated device stack.

        Returns: obj(snappi.DeviceEthernet)
        """
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = DeviceEthernet()
        return self._properties['ethernet']

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
