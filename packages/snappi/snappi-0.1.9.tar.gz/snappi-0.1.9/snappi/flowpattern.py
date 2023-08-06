from .flowcounter import FlowCounter
from .snappicommon import SnappiObject


class FlowPattern(SnappiObject):
    _TYPES = {
        'increment': '.flowcounter.FlowCounter',
        'decrement': '.flowcounter.FlowCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, metric_group=None):
        super(FlowPattern, self).__init__()
        self.metric_group = metric_group

    @property
    def increment(self):
        # type: () -> FlowCounter
        """Factory method to create an instance of the FlowCounter class

        A counter pattern that can increment or decrement.
        """
        if 'increment' not in self._properties or self._properties['increment'] is None:
            self._properties['increment'] = FlowCounter()
        self.choice = 'increment'
        return self._properties['increment']

    @property
    def decrement(self):
        # type: () -> FlowCounter
        """Factory method to create an instance of the FlowCounter class

        A counter pattern that can increment or decrement.
        """
        if 'decrement' not in self._properties or self._properties['decrement'] is None:
            self._properties['decrement'] = FlowCounter()
        self.choice = 'decrement'
        return self._properties['decrement']

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def value(self):
        # type: () -> Union[string,number]
        """value getter

        TBD

        Returns: Union[string,number]
        """
        return self._properties['value']

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: Union[string,number]
        """
        self._properties['choice'] = 'value'
        self._properties['value'] = value

    @property
    def values(self):
        # type: () -> list[Union[string,number]]
        """values getter

        TBD

        Returns: list[Union[string,number]]
        """
        return self._properties['values']

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[Union[string,number]]
        """
        self._properties['choice'] = 'values'
        self._properties['values'] = value

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._properties['metric_group']

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._properties['metric_group'] = value
