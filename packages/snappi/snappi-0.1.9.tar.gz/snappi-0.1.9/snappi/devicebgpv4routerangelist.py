from .devicebgpv4routerange import DeviceBgpv4RouteRange
from .snappicommon import SnappiList


class DeviceBgpv4RouteRangeList(SnappiList):
    def __init__(self):
        super(DeviceBgpv4RouteRangeList, self).__init__()


    def bgpv4routerange(self, route_count_per_device=1, name=None):
        # type: () -> DeviceBgpv4RouteRange
        """Factory method to create an instance of the snappi.devicebgpv4routerange.DeviceBgpv4RouteRange class

        Emulated BGPv4 route range
        """
        item = DeviceBgpv4RouteRange(route_count_per_device, name)
        self._add(item)
        return self
