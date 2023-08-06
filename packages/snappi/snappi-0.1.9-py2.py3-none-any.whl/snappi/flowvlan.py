from .flowpattern import FlowPattern
from .snappicommon import SnappiObject


class FlowVlan(SnappiObject):
    _TYPES = {
        'priority': '.flowpattern.FlowPattern',
        'cfi': '.flowpattern.FlowPattern',
        'id': '.flowpattern.FlowPattern',
        'protocol': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowVlan, self).__init__()

    @property
    def priority(self):
        # type: () -> FlowPattern
        """priority getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'priority' not in self._properties or self._properties['priority'] is None:
            self._properties['priority'] = FlowPattern()
        return self._properties['priority']

    @property
    def cfi(self):
        # type: () -> FlowPattern
        """cfi getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'cfi' not in self._properties or self._properties['cfi'] is None:
            self._properties['cfi'] = FlowPattern()
        return self._properties['cfi']

    @property
    def id(self):
        # type: () -> FlowPattern
        """id getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'id' not in self._properties or self._properties['id'] is None:
            self._properties['id'] = FlowPattern()
        return self._properties['id']

    @property
    def protocol(self):
        # type: () -> FlowPattern
        """protocol getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'protocol' not in self._properties or self._properties['protocol'] is None:
            self._properties['protocol'] = FlowPattern()
        return self._properties['protocol']
