from .devicepattern import DevicePattern
from .snappicommon import SnappiObject


class DeviceVlan(SnappiObject):
    _TYPES = {
        'tpid': '.devicepattern.DevicePattern',
        'priority': '.devicepattern.DevicePattern',
        'id': '.devicepattern.DevicePattern',
    }

    TPID_8100 = '8100'
    TPID_88A8 = '88a8'
    TPID_9100 = '9100'
    TPID_9200 = '9200'
    TPID_9300 = '9300'

    def __init__(self, name=None):
        super(DeviceVlan, self).__init__()
        self.name = name

    @property
    def tpid(self):
        # type: () -> DevicePattern
        """tpid getter

        A container for emulated device property patterns.Vlan tag protocol identifier.

        Returns: obj(snappi.DevicePattern)
        """
        if 'tpid' not in self._properties or self._properties['tpid'] is None:
            self._properties['tpid'] = DevicePattern()
        return self._properties['tpid']

    @property
    def priority(self):
        # type: () -> DevicePattern
        """priority getter

        A container for emulated device property patterns.Vlan priority.

        Returns: obj(snappi.DevicePattern)
        """
        if 'priority' not in self._properties or self._properties['priority'] is None:
            self._properties['priority'] = DevicePattern()
        return self._properties['priority']

    @property
    def id(self):
        # type: () -> DevicePattern
        """id getter

        A container for emulated device property patterns.Vlan id.

        Returns: obj(snappi.DevicePattern)
        """
        if 'id' not in self._properties or self._properties['id'] is None:
            self._properties['id'] = DevicePattern()
        return self._properties['id']

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
