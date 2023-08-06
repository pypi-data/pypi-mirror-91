from .flowvlan import FlowVlan
from .flowheader import FlowHeader
from .flowpfcpause import FlowPfcPause
from .flowgtpv1 import FlowGtpv1
from .flowcustom import FlowCustom
from .snappicommon import SnappiList
from .flowtcp import FlowTcp
from .flowipv6 import FlowIpv6
from .flowethernet import FlowEthernet
from .flowudp import FlowUdp
from .flowgre import FlowGre
from .flowethernetpause import FlowEthernetPause
from .flowgtpv2 import FlowGtpv2
from .flowvxlan import FlowVxlan
from .flowipv4 import FlowIpv4


class FlowHeaderList(SnappiList):
    def __init__(self):
        super(FlowHeaderList, self).__init__()


    def header(self):
        # type: () -> FlowHeader
        """Factory method to create an instance of the snappi.flowheader.FlowHeader class

        Container for all traffic packet headers
        """
        item = FlowHeader()
        self._add(item)
        return self

    def custom(self, bytes=None):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowcustom.FlowCustom class

        Custom packet header
        """
        item = FlowHeader()
        item.custom
        self._add(item)
        return self

    def ethernet(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowethernet.FlowEthernet class

        Ethernet packet header
        """
        item = FlowHeader()
        item.ethernet
        self._add(item)
        return self

    def vlan(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowvlan.FlowVlan class

        Vlan packet header
        """
        item = FlowHeader()
        item.vlan
        self._add(item)
        return self

    def vxlan(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowvxlan.FlowVxlan class

        Vxlan packet header
        """
        item = FlowHeader()
        item.vxlan
        self._add(item)
        return self

    def ipv4(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowipv4.FlowIpv4 class

        Ipv4 packet header
        """
        item = FlowHeader()
        item.ipv4
        self._add(item)
        return self

    def ipv6(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowipv6.FlowIpv6 class

        Ipv6 packet header
        """
        item = FlowHeader()
        item.ipv6
        self._add(item)
        return self

    def pfcpause(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowpfcpause.FlowPfcPause class

        IEEE 802.1Qbb PFC Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0101 16bits - class_enable_vector: 16bits - pause_class_0: 0x0000 16bits - pause_class_1: 0x0000 16bits - pause_class_2: 0x0000 16bits - pause_class_3: 0x0000 16bits - pause_class_4: 0x0000 16bits - pause_class_5: 0x0000 16bits - pause_class_6: 0x0000 16bits - pause_class_7: 0x0000 16bits
        """
        item = FlowHeader()
        item.pfcpause
        self._add(item)
        return self

    def ethernetpause(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowethernetpause.FlowEthernetPause class

        IEEE 802.3x Ethernet Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0001 16bits - time: 0x0000 16bits
        """
        item = FlowHeader()
        item.ethernetpause
        self._add(item)
        return self

    def tcp(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowtcp.FlowTcp class

        Tcp packet header
        """
        item = FlowHeader()
        item.tcp
        self._add(item)
        return self

    def udp(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowudp.FlowUdp class

        Udp packet header
        """
        item = FlowHeader()
        item.udp
        self._add(item)
        return self

    def gre(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowgre.FlowGre class

        Gre packet header
        """
        item = FlowHeader()
        item.gre
        self._add(item)
        return self

    def gtpv1(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowgtpv1.FlowGtpv1 class

        GTPv1 packet header
        """
        item = FlowHeader()
        item.gtpv1
        self._add(item)
        return self

    def gtpv2(self):
        # type: () -> FlowHeaderList
        """Factory method to create an instance of the snappi.flowgtpv2.FlowGtpv2 class

        GTPv2 packet header
        """
        item = FlowHeader()
        item.gtpv2
        self._add(item)
        return self
