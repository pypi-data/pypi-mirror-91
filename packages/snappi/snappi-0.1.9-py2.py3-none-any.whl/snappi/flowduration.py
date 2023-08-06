from .flowcontinuous import FlowContinuous
from .flowburst import FlowBurst
from .flowfixedseconds import FlowFixedSeconds
from .snappicommon import SnappiObject
from .flowfixedpackets import FlowFixedPackets


class FlowDuration(SnappiObject):
    _TYPES = {
        'fixed_packets': '.flowfixedpackets.FlowFixedPackets',
        'fixed_seconds': '.flowfixedseconds.FlowFixedSeconds',
        'burst': '.flowburst.FlowBurst',
        'continuous': '.flowcontinuous.FlowContinuous',
    }

    FIXED_PACKETS = 'fixed_packets'
    FIXED_SECONDS = 'fixed_seconds'
    BURST = 'burst'
    CONTINUOUS = 'continuous'

    def __init__(self):
        super(FlowDuration, self).__init__()

    @property
    def fixed_packets(self):
        # type: () -> FlowFixedPackets
        """Factory method to create an instance of the FlowFixedPackets class

        Transmit a fixed number of packets after which the flow will stop.
        """
        if 'fixed_packets' not in self._properties or self._properties['fixed_packets'] is None:
            self._properties['fixed_packets'] = FlowFixedPackets()
        self.choice = 'fixed_packets'
        return self._properties['fixed_packets']

    @property
    def fixed_seconds(self):
        # type: () -> FlowFixedSeconds
        """Factory method to create an instance of the FlowFixedSeconds class

        Transmit for a fixed number of seconds after which the flow will stop.
        """
        if 'fixed_seconds' not in self._properties or self._properties['fixed_seconds'] is None:
            self._properties['fixed_seconds'] = FlowFixedSeconds()
        self.choice = 'fixed_seconds'
        return self._properties['fixed_seconds']

    @property
    def burst(self):
        # type: () -> FlowBurst
        """Factory method to create an instance of the FlowBurst class

        A continuous burst of packets that will not automatically stop.
        """
        if 'burst' not in self._properties or self._properties['burst'] is None:
            self._properties['burst'] = FlowBurst()
        self.choice = 'burst'
        return self._properties['burst']

    @property
    def continuous(self):
        # type: () -> FlowContinuous
        """Factory method to create an instance of the FlowContinuous class

        Transmit will be continuous and will not stop automatically. 
        """
        if 'continuous' not in self._properties or self._properties['continuous'] is None:
            self._properties['continuous'] = FlowContinuous()
        self.choice = 'continuous'
        return self._properties['continuous']

    @property
    def choice(self):
        # type: () -> Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        self._properties['choice'] = value
