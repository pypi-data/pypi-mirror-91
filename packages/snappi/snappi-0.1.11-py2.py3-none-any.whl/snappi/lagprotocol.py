from .snappicommon import SnappiObject
from .laglacp import LagLacp
from .lagstatic import LagStatic


class LagProtocol(SnappiObject):
    _TYPES = {
        'lacp': '.laglacp.LagLacp',
        'static': '.lagstatic.LagStatic',
    }

    LACP = 'lacp'
    STATIC = 'static'

    def __init__(self):
        super(LagProtocol, self).__init__()

    @property
    def lacp(self):
        # type: () -> LagLacp
        """Factory method to create an instance of the LagLacp class

        TBD
        """
        if 'lacp' not in self._properties or self._properties['lacp'] is None:
            self._properties['lacp'] = LagLacp()
        self.choice = 'lacp'
        return self._properties['lacp']

    @property
    def static(self):
        # type: () -> LagStatic
        """Factory method to create an instance of the LagStatic class

        TBD
        """
        if 'static' not in self._properties or self._properties['static'] is None:
            self._properties['static'] = LagStatic()
        self.choice = 'static'
        return self._properties['static']

    @property
    def choice(self):
        # type: () -> Union[lacp, static, choice, choice, choice]
        """choice getter

        The type of lag protocol.

        Returns: Union[lacp, static, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of lag protocol.

        value: Union[lacp, static, choice, choice, choice]
        """
        self._properties['choice'] = value
