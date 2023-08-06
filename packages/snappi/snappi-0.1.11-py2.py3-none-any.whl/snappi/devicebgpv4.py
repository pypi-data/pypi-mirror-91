from .devicepattern import DevicePattern
from .snappicommon import SnappiObject
from .devicebgpv4routerangelist import DeviceBgpv4RouteRangeList
from .deviceipv4 import DeviceIpv4
from .devicebgpv6routerangelist import DeviceBgpv6RouteRangeList


class DeviceBgpv4(SnappiObject):
    _TYPES = {
        'router_id': '.devicepattern.DevicePattern',
        'as_number': '.devicepattern.DevicePattern',
        'hold_time_interval': '.devicepattern.DevicePattern',
        'keep_alive_interval': '.devicepattern.DevicePattern',
        'dut_ipv4_address': '.devicepattern.DevicePattern',
        'dut_as_number': '.devicepattern.DevicePattern',
        'ipv4': '.deviceipv4.DeviceIpv4',
        'bgpv4_route_range': '.devicebgpv4routerangelist.DeviceBgpv4RouteRangeList',
        'bgpv6_route_range': '.devicebgpv6routerangelist.DeviceBgpv6RouteRangeList',
    }

    IBGP = 'ibgp'
    EBGP = 'ebgp'

    def __init__(self, as_type=None, name=None):
        super(DeviceBgpv4, self).__init__()
        self.as_type = as_type
        self.name = name

    @property
    def router_id(self):
        # type: () -> DevicePattern
        """router_id getter

        A container for emulated device property patterns.A container for emulated device property patterns.specifies BGP router identifier. It must be the string representation of an IPv4 address 

        Returns: obj(snappi.DevicePattern)
        """
        if 'router_id' not in self._properties or self._properties['router_id'] is None:
            self._properties['router_id'] = DevicePattern()
        return self._properties['router_id']

    @property
    def as_number(self):
        # type: () -> DevicePattern
        """as_number getter

        A container for emulated device property patterns.A container for emulated device property patterns.Autonomous system (AS) number of 4 byte

        Returns: obj(snappi.DevicePattern)
        """
        if 'as_number' not in self._properties or self._properties['as_number'] is None:
            self._properties['as_number'] = DevicePattern()
        return self._properties['as_number']

    @property
    def as_type(self):
        # type: () -> Union[ibgp, ebgp]
        """as_type getter

        The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system.

        Returns: Union[ibgp, ebgp]
        """
        return self._properties['as_type']

    @as_type.setter
    def as_type(self, value):
        """as_type setter

        The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system.

        value: Union[ibgp, ebgp]
        """
        self._properties['as_type'] = value

    @property
    def hold_time_interval(self):
        # type: () -> DevicePattern
        """hold_time_interval getter

        A container for emulated device property patterns.A container for emulated device property patterns.Number of seconds the sender proposes for the value of the Hold Timer

        Returns: obj(snappi.DevicePattern)
        """
        if 'hold_time_interval' not in self._properties or self._properties['hold_time_interval'] is None:
            self._properties['hold_time_interval'] = DevicePattern()
        return self._properties['hold_time_interval']

    @property
    def keep_alive_interval(self):
        # type: () -> DevicePattern
        """keep_alive_interval getter

        A container for emulated device property patterns.A container for emulated device property patterns.Number of seconds between transmissions of Keep Alive messages by router

        Returns: obj(snappi.DevicePattern)
        """
        if 'keep_alive_interval' not in self._properties or self._properties['keep_alive_interval'] is None:
            self._properties['keep_alive_interval'] = DevicePattern()
        return self._properties['keep_alive_interval']

    @property
    def dut_ipv4_address(self):
        # type: () -> DevicePattern
        """dut_ipv4_address getter

        A container for emulated device property patterns.A container for emulated device property patterns.IPv4 address of the BGP peer for the session

        Returns: obj(snappi.DevicePattern)
        """
        if 'dut_ipv4_address' not in self._properties or self._properties['dut_ipv4_address'] is None:
            self._properties['dut_ipv4_address'] = DevicePattern()
        return self._properties['dut_ipv4_address']

    @property
    def dut_as_number(self):
        # type: () -> DevicePattern
        """dut_as_number getter

        A container for emulated device property patterns.A container for emulated device property patterns.Autonomous system (AS) number of the BGP peer router (DUT)

        Returns: obj(snappi.DevicePattern)
        """
        if 'dut_as_number' not in self._properties or self._properties['dut_as_number'] is None:
            self._properties['dut_as_number'] = DevicePattern()
        return self._properties['dut_as_number']

    @property
    def ipv4(self):
        # type: () -> DeviceIpv4
        """ipv4 getter

        Emulated ipv4 protocolEmulated ipv4 protocolThe ipv4 stack that the bgp4 protocol is implemented over.

        Returns: obj(snappi.DeviceIpv4)
        """
        if 'ipv4' not in self._properties or self._properties['ipv4'] is None:
            self._properties['ipv4'] = DeviceIpv4()
        return self._properties['ipv4']

    @property
    def bgpv4_route_range(self):
        # type: () -> DeviceBgpv4RouteRangeList
        """bgpv4_route_range getter

        Emulated BGPv4 route range

        Returns: list[obj(snappi.DeviceBgpv4RouteRange)]
        """
        if 'bgpv4_route_range' not in self._properties or self._properties['bgpv4_route_range'] is None:
            self._properties['bgpv4_route_range'] = DeviceBgpv4RouteRangeList()
        return self._properties['bgpv4_route_range']

    @property
    def bgpv6_route_range(self):
        # type: () -> DeviceBgpv6RouteRangeList
        """bgpv6_route_range getter

        Emulated bgpv6 route range

        Returns: list[obj(snappi.DeviceBgpv6RouteRange)]
        """
        if 'bgpv6_route_range' not in self._properties or self._properties['bgpv6_route_range'] is None:
            self._properties['bgpv6_route_range'] = DeviceBgpv6RouteRangeList()
        return self._properties['bgpv6_route_range']

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
