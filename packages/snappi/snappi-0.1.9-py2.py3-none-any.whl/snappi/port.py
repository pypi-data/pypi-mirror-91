from .snappicommon import SnappiObject


class Port(SnappiObject):
    def __init__(self, location=None, name=None):
        super(Port, self).__init__()
        self.location = location
        self.name = name

    @property
    def location(self):
        # type: () -> str
        """location getter

        The location of a test port. It is the endpoint where packets will emit from.. Test port locations can be the following:. - physical appliance with multiple ports. - physical chassis with multiple cards and ports. - local interface. - virtual machine, docker container, kubernetes cluster. . The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property.. Get the configured location state by using the /results/port API.

        Returns: str
        """
        return self._properties['location']

    @location.setter
    def location(self, value):
        """location setter

        The location of a test port. It is the endpoint where packets will emit from.. Test port locations can be the following:. - physical appliance with multiple ports. - physical chassis with multiple cards and ports. - local interface. - virtual machine, docker container, kubernetes cluster. . The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property.. Get the configured location state by using the /results/port API.

        value: str
        """
        self._properties['location'] = value

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value
