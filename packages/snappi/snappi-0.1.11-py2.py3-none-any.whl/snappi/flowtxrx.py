from .snappicommon import SnappiObject
from .flowport import FlowPort
from .flowdevice import FlowDevice


class FlowTxRx(SnappiObject):
    _TYPES = {
        'port': '.flowport.FlowPort',
        'device': '.flowdevice.FlowDevice',
    }

    PORT = 'port'
    DEVICE = 'device'

    def __init__(self):
        super(FlowTxRx, self).__init__()

    @property
    def port(self):
        # type: () -> FlowPort
        """Factory method to create an instance of the FlowPort class

        A container for a transmit port and 0..n intended receive ports. When assigning this container to a flow the flows's packet headers will not be populated with any address resolution information such as source and/or destination addresses. For example Flow.Ethernet dst mac address values will be defaulted to 0. For full control over the Flow.properties.packet header contents use this container. 
        """
        if 'port' not in self._properties or self._properties['port'] is None:
            self._properties['port'] = FlowPort()
        self.choice = 'port'
        return self._properties['port']

    @property
    def device(self):
        # type: () -> FlowDevice
        """Factory method to create an instance of the FlowDevice class

        A container for 1..n transmit devices and 1..n receive devices. Implemementations may use learned information from the devices to pre-populate Flow.properties.packet[Flow.Header fields].. For example an implementation may automatically start devices, get arp table information and pre-populate the Flow.Ethernet dst mac address values.. To discover what the implementation supports use the /results/capabilities API.
        """
        if 'device' not in self._properties or self._properties['device'] is None:
            self._properties['device'] = FlowDevice()
        self.choice = 'device'
        return self._properties['device']

    @property
    def choice(self):
        # type: () -> Union[port, device, choice, choice, choice]
        """choice getter

        The type of transmit and receive container used by the flow.

        Returns: Union[port, device, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of transmit and receive container used by the flow.

        value: Union[port, device, choice, choice, choice]
        """
        self._properties['choice'] = value
