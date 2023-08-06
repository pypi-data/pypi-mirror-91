from .devicebgpv6routerange import DeviceBgpv6RouteRange
from .snappicommon import SnappiList


class DeviceBgpv6RouteRangeList(SnappiList):
    def __init__(self):
        super(DeviceBgpv6RouteRangeList, self).__init__()


    def bgpv6routerange(self, route_count_per_device=1, name=None):
        # type: () -> DeviceBgpv6RouteRange
        """Factory method to create an instance of the snappi.devicebgpv6routerange.DeviceBgpv6RouteRange class

        Emulated bgpv6 route range
        """
        item = DeviceBgpv6RouteRange(route_count_per_device, name)
        self._add(item)
        return self
