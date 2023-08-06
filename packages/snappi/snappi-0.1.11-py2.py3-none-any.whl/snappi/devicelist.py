from .snappicommon import SnappiList
from .deviceethernet import DeviceEthernet
from .deviceipv6 import DeviceIpv6
from .devicecontaineripv4 import DeviceContainerIpv4
from .device import Device
from .devicebgpv4 import DeviceBgpv4


class DeviceList(SnappiList):
    def __init__(self):
        super(DeviceList, self).__init__()


    def device(self, container_name=None, device_count=1, name=None):
        # type: () -> Device
        """Factory method to create an instance of the snappi.device.Device class

        A container for emulated protocol devices.
        """
        item = Device(container_name, device_count, name)
        self._add(item)
        return self

    def ethernet(self, name=None):
        # type: () -> DeviceList
        """Factory method to create an instance of the snappi.deviceethernet.DeviceEthernet class

        Emulated ethernet protocol. A top level in the emulated device stack.
        """
        item = Device()
        item.ethernet
        self._add(item)
        return self

    def ipv4(self, name=None):
        # type: () -> DeviceList
        """Factory method to create an instance of the snappi.devicecontaineripv4.DeviceContainerIpv4 class

        Emulated ipv4 protocol
        """
        item = Device()
        item.ipv4
        self._add(item)
        return self

    def ipv6(self, name=None):
        # type: () -> DeviceList
        """Factory method to create an instance of the snappi.deviceipv6.DeviceIpv6 class

        Emulated ipv6 protocol
        """
        item = Device()
        item.ipv6
        self._add(item)
        return self

    def bgpv4(self, as_type='None', name=None):
        # type: () -> DeviceList
        """Factory method to create an instance of the snappi.devicebgpv4.DeviceBgpv4 class

        Emulated BGPv4 router and routes
        """
        item = Device()
        item.bgpv4
        self._add(item)
        return self
