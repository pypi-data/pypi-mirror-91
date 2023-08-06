from .devicecounter import DeviceCounter
from .snappicommon import SnappiObject


class DevicePattern(SnappiObject):
    _TYPES = {
        'increment': '.devicecounter.DeviceCounter',
        'decrement': '.devicecounter.DeviceCounter',
    }

    VALUE = 'value'
    VALUE_LIST = 'value_list'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self):
        super(DevicePattern, self).__init__()

    @property
    def increment(self):
        # type: () -> DeviceCounter
        """Factory method to create an instance of the DeviceCounter class

        An incrementing pattern.
        """
        if 'increment' not in self._properties or self._properties['increment'] is None:
            self._properties['increment'] = DeviceCounter()
        self.choice = 'increment'
        return self._properties['increment']

    @property
    def decrement(self):
        # type: () -> DeviceCounter
        """Factory method to create an instance of the DeviceCounter class

        An incrementing pattern.
        """
        if 'decrement' not in self._properties or self._properties['decrement'] is None:
            self._properties['decrement'] = DeviceCounter()
        self.choice = 'decrement'
        return self._properties['decrement']

    @property
    def choice(self):
        # type: () -> Union[value, value_list, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, value_list, increment, decrement, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, value_list, increment, decrement, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._properties['value']

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._properties['choice'] = 'value'
        self._properties['value'] = value

    @property
    def value_list(self):
        # type: () -> list[str]
        """value_list getter

        TBD

        Returns: list[str]
        """
        return self._properties['value_list']

    @value_list.setter
    def value_list(self, value):
        """value_list setter

        TBD

        value: list[str]
        """
        self._properties['choice'] = 'value_list'
        self._properties['value_list'] = value
