from .snappicommon import SnappiObject


class LinkState(SnappiObject):
    UP = 'up'
    DOWN = 'down'

    def __init__(self, port_names=None, state=None):
        super(LinkState, self).__init__()
        self.port_names = port_names
        self.state = state

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The names of port objects to. An empty or null list will control all port objects.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The names of port objects to. An empty or null list will control all port objects.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def state(self):
        # type: () -> Union[up, down]
        """state getter

        The link state.

        Returns: Union[up, down]
        """
        return self._properties['state']

    @state.setter
    def state(self, value):
        """state setter

        The link state.

        value: Union[up, down]
        """
        self._properties['state'] = value
