from .flowstatelist import FlowStateList
from .snappicommon import SnappiObject
from .portstatelist import PortStateList


class StateMetrics(SnappiObject):
    _TYPES = {
        'port_state': '.portstatelist.PortStateList',
        'flow_state': '.flowstatelist.FlowStateList',
    }

    def __init__(self):
        super(StateMetrics, self).__init__()

    @property
    def port_state(self):
        # type: () -> PortStateList
        """port_state getter

        TBD

        Returns: list[obj(snappi.PortState)]
        """
        if 'port_state' not in self._properties or self._properties['port_state'] is None:
            self._properties['port_state'] = PortStateList()
        return self._properties['port_state']

    @property
    def flow_state(self):
        # type: () -> FlowStateList
        """flow_state getter

        TBD

        Returns: list[obj(snappi.FlowState)]
        """
        if 'flow_state' not in self._properties or self._properties['flow_state'] is None:
            self._properties['flow_state'] = FlowStateList()
        return self._properties['flow_state']
