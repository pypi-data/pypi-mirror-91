from .snappicommon import SnappiList
from .devicevlan import DeviceVlan


class DeviceVlanList(SnappiList):
    def __init__(self):
        super(DeviceVlanList, self).__init__()


    def vlan(self, name=None):
        # type: () -> DeviceVlan
        """Factory method to create an instance of the snappi.devicevlan.DeviceVlan class

        Emulated vlan protocol
        """
        item = DeviceVlan(name)
        self._add(item)
        return self
