from .flowethernetpause import FlowEthernetPause
from .flowcustom import FlowCustom
from .flowgtpv2 import FlowGtpv2
from .snappicommon import SnappiObject
from .flowtcp import FlowTcp
from .flowudp import FlowUdp
from .flowgre import FlowGre
from .flowipv6 import FlowIpv6
from .flowethernet import FlowEthernet
from .flowgtpv1 import FlowGtpv1
from .flowvxlan import FlowVxlan
from .flowvlan import FlowVlan
from .flowpfcpause import FlowPfcPause
from .flowipv4 import FlowIpv4


class FlowHeader(SnappiObject):
    _TYPES = {
        'custom': '.flowcustom.FlowCustom',
        'ethernet': '.flowethernet.FlowEthernet',
        'vlan': '.flowvlan.FlowVlan',
        'vxlan': '.flowvxlan.FlowVxlan',
        'ipv4': '.flowipv4.FlowIpv4',
        'ipv6': '.flowipv6.FlowIpv6',
        'pfcpause': '.flowpfcpause.FlowPfcPause',
        'ethernetpause': '.flowethernetpause.FlowEthernetPause',
        'tcp': '.flowtcp.FlowTcp',
        'udp': '.flowudp.FlowUdp',
        'gre': '.flowgre.FlowGre',
        'gtpv1': '.flowgtpv1.FlowGtpv1',
        'gtpv2': '.flowgtpv2.FlowGtpv2',
    }

    CUSTOM = 'custom'
    ETHERNET = 'ethernet'
    VLAN = 'vlan'
    VXLAN = 'vxlan'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    PFCPAUSE = 'pfcpause'
    ETHERNETPAUSE = 'ethernetpause'
    TCP = 'tcp'
    UDP = 'udp'
    GRE = 'gre'
    GTPV1 = 'gtpv1'
    GTPV2 = 'gtpv2'

    def __init__(self):
        super(FlowHeader, self).__init__()

    @property
    def custom(self):
        # type: () -> FlowCustom
        """Factory method to create an instance of the FlowCustom class

        Custom packet header
        """
        if 'custom' not in self._properties or self._properties['custom'] is None:
            self._properties['custom'] = FlowCustom()
        self.choice = 'custom'
        return self._properties['custom']

    @property
    def ethernet(self):
        # type: () -> FlowEthernet
        """Factory method to create an instance of the FlowEthernet class

        Ethernet packet header
        """
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = FlowEthernet()
        self.choice = 'ethernet'
        return self._properties['ethernet']

    @property
    def vlan(self):
        # type: () -> FlowVlan
        """Factory method to create an instance of the FlowVlan class

        Vlan packet header
        """
        if 'vlan' not in self._properties or self._properties['vlan'] is None:
            self._properties['vlan'] = FlowVlan()
        self.choice = 'vlan'
        return self._properties['vlan']

    @property
    def vxlan(self):
        # type: () -> FlowVxlan
        """Factory method to create an instance of the FlowVxlan class

        Vxlan packet header
        """
        if 'vxlan' not in self._properties or self._properties['vxlan'] is None:
            self._properties['vxlan'] = FlowVxlan()
        self.choice = 'vxlan'
        return self._properties['vxlan']

    @property
    def ipv4(self):
        # type: () -> FlowIpv4
        """Factory method to create an instance of the FlowIpv4 class

        Ipv4 packet header
        """
        if 'ipv4' not in self._properties or self._properties['ipv4'] is None:
            self._properties['ipv4'] = FlowIpv4()
        self.choice = 'ipv4'
        return self._properties['ipv4']

    @property
    def ipv6(self):
        # type: () -> FlowIpv6
        """Factory method to create an instance of the FlowIpv6 class

        Ipv6 packet header
        """
        if 'ipv6' not in self._properties or self._properties['ipv6'] is None:
            self._properties['ipv6'] = FlowIpv6()
        self.choice = 'ipv6'
        return self._properties['ipv6']

    @property
    def pfcpause(self):
        # type: () -> FlowPfcPause
        """Factory method to create an instance of the FlowPfcPause class

        IEEE 802.1Qbb PFC Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0101 16bits - class_enable_vector: 16bits - pause_class_0: 0x0000 16bits - pause_class_1: 0x0000 16bits - pause_class_2: 0x0000 16bits - pause_class_3: 0x0000 16bits - pause_class_4: 0x0000 16bits - pause_class_5: 0x0000 16bits - pause_class_6: 0x0000 16bits - pause_class_7: 0x0000 16bits
        """
        if 'pfcpause' not in self._properties or self._properties['pfcpause'] is None:
            self._properties['pfcpause'] = FlowPfcPause()
        self.choice = 'pfcpause'
        return self._properties['pfcpause']

    @property
    def ethernetpause(self):
        # type: () -> FlowEthernetPause
        """Factory method to create an instance of the FlowEthernetPause class

        IEEE 802.3x Ethernet Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0001 16bits - time: 0x0000 16bits
        """
        if 'ethernetpause' not in self._properties or self._properties['ethernetpause'] is None:
            self._properties['ethernetpause'] = FlowEthernetPause()
        self.choice = 'ethernetpause'
        return self._properties['ethernetpause']

    @property
    def tcp(self):
        # type: () -> FlowTcp
        """Factory method to create an instance of the FlowTcp class

        Tcp packet header
        """
        if 'tcp' not in self._properties or self._properties['tcp'] is None:
            self._properties['tcp'] = FlowTcp()
        self.choice = 'tcp'
        return self._properties['tcp']

    @property
    def udp(self):
        # type: () -> FlowUdp
        """Factory method to create an instance of the FlowUdp class

        Udp packet header
        """
        if 'udp' not in self._properties or self._properties['udp'] is None:
            self._properties['udp'] = FlowUdp()
        self.choice = 'udp'
        return self._properties['udp']

    @property
    def gre(self):
        # type: () -> FlowGre
        """Factory method to create an instance of the FlowGre class

        Gre packet header
        """
        if 'gre' not in self._properties or self._properties['gre'] is None:
            self._properties['gre'] = FlowGre()
        self.choice = 'gre'
        return self._properties['gre']

    @property
    def gtpv1(self):
        # type: () -> FlowGtpv1
        """Factory method to create an instance of the FlowGtpv1 class

        GTPv1 packet header
        """
        if 'gtpv1' not in self._properties or self._properties['gtpv1'] is None:
            self._properties['gtpv1'] = FlowGtpv1()
        self.choice = 'gtpv1'
        return self._properties['gtpv1']

    @property
    def gtpv2(self):
        # type: () -> FlowGtpv2
        """Factory method to create an instance of the FlowGtpv2 class

        GTPv2 packet header
        """
        if 'gtpv2' not in self._properties or self._properties['gtpv2'] is None:
            self._properties['gtpv2'] = FlowGtpv2()
        self.choice = 'gtpv2'
        return self._properties['gtpv2']

    @property
    def choice(self):
        # type: () -> Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, choice, choice, choice]
        """
        self._properties['choice'] = value
