from .devicepattern import DevicePattern
from .snappicommon import SnappiObject


class DeviceBgpv6RouteRange(SnappiObject):
    _TYPES = {
        'address': '.devicepattern.DevicePattern',
        'prefix': '.devicepattern.DevicePattern',
        'as_path': '.devicepattern.DevicePattern',
        'next_hop_address': '.devicepattern.DevicePattern',
        'community': '.devicepattern.DevicePattern',
    }

    def __init__(self, route_count_per_device=None, name=None):
        super(DeviceBgpv6RouteRange, self).__init__()
        self.route_count_per_device = route_count_per_device
        self.name = name

    @property
    def route_count_per_device(self):
        # type: () -> int
        """route_count_per_device getter

        The number of routes per device.

        Returns: int
        """
        return self._properties['route_count_per_device']

    @route_count_per_device.setter
    def route_count_per_device(self, value):
        """route_count_per_device setter

        The number of routes per device.

        value: int
        """
        self._properties['route_count_per_device'] = value

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.The network address of the first network

        Returns: obj(snappi.DevicePattern)
        """
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.Ipv6 prefix length with minimum value is 0 to maximum value is 128

        Returns: obj(snappi.DevicePattern)
        """
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def as_path(self):
        # type: () -> DevicePattern
        """as_path getter

        A container for emulated device property patterns.Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DevicePattern)
        """
        if 'as_path' not in self._properties or self._properties['as_path'] is None:
            self._properties['as_path'] = DevicePattern()
        return self._properties['as_path']

    @property
    def next_hop_address(self):
        # type: () -> DevicePattern
        """next_hop_address getter

        A container for emulated device property patterns.IP Address of next router to forward a packet to its final destination

        Returns: obj(snappi.DevicePattern)
        """
        if 'next_hop_address' not in self._properties or self._properties['next_hop_address'] is None:
            self._properties['next_hop_address'] = DevicePattern()
        return self._properties['next_hop_address']

    @property
    def community(self):
        # type: () -> DevicePattern
        """community getter

        A container for emulated device property patterns.BGP communities provide additional capability for tagging routes and for modifying BGP routing policy on upstream and downstream routers BGP community is a 32-bit number which broken into 16-bit As and 16-bit custom value Please specify those two values in this string format 65000:100

        Returns: obj(snappi.DevicePattern)
        """
        if 'community' not in self._properties or self._properties['community'] is None:
            self._properties['community'] = DevicePattern()
        return self._properties['community']

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
