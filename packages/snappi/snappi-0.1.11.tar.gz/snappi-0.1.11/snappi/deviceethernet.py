from .devicevlanlist import DeviceVlanList
from .devicepattern import DevicePattern
from .snappicommon import SnappiObject


class DeviceEthernet(SnappiObject):
    _TYPES = {
        'mac': '.devicepattern.DevicePattern',
        'mtu': '.devicepattern.DevicePattern',
        'vlans': '.devicevlanlist.DeviceVlanList',
    }

    def __init__(self, name=None):
        super(DeviceEthernet, self).__init__()
        self.name = name

    @property
    def mac(self):
        # type: () -> DevicePattern
        """mac getter

        A container for emulated device property patterns.Media access control address (MAC) is a 48bit identifier for use as a network address. The value can be an int or a hex string with or without spaces or colons separating each byte. The min value is 0 or '00:00:00:00:00:00'. The max value is 281474976710655 or 'FF:FF:FF:FF:FF:FF'.

        Returns: obj(snappi.DevicePattern)
        """
        if 'mac' not in self._properties or self._properties['mac'] is None:
            self._properties['mac'] = DevicePattern()
        return self._properties['mac']

    @property
    def mtu(self):
        # type: () -> DevicePattern
        """mtu getter

        A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        if 'mtu' not in self._properties or self._properties['mtu'] is None:
            self._properties['mtu'] = DevicePattern()
        return self._properties['mtu']

    @property
    def vlans(self):
        # type: () -> DeviceVlanList
        """vlans getter

        List of vlans

        Returns: list[obj(snappi.DeviceVlan)]
        """
        if 'vlans' not in self._properties or self._properties['vlans'] is None:
            self._properties['vlans'] = DeviceVlanList()
        return self._properties['vlans']

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
