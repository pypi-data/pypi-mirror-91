from .snappicommon import SnappiObject
from .portoptions import PortOptions


class ConfigOptions(SnappiObject):
    _TYPES = {
        'port_options': '.portoptions.PortOptions',
    }

    def __init__(self):
        super(ConfigOptions, self).__init__()

    @property
    def port_options(self):
        # type: () -> PortOptions
        """port_options getter

        Common port options that apply to all configured Port objects. 

        Returns: obj(snappi.PortOptions)
        """
        if 'port_options' not in self._properties or self._properties['port_options'] is None:
            self._properties['port_options'] = PortOptions()
        return self._properties['port_options']
