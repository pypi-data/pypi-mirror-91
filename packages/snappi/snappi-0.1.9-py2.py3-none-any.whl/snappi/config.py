from .configoptions import ConfigOptions
from .devicelist import DeviceList
from .flowlist import FlowList
from .portlist import PortList
from .laglist import LagList
from .capturelist import CaptureList
from .snappicommon import SnappiObject
from .layer1list import Layer1List


class Config(SnappiObject):
    _TYPES = {
        'ports': '.portlist.PortList',
        'lags': '.laglist.LagList',
        'layer1': '.layer1list.Layer1List',
        'captures': '.capturelist.CaptureList',
        'devices': '.devicelist.DeviceList',
        'flows': '.flowlist.FlowList',
        'options': '.configoptions.ConfigOptions',
    }

    def __init__(self):
        super(Config, self).__init__()

    @property
    def ports(self):
        # type: () -> PortList
        """ports getter

        The ports that will be configured on the traffic generator.

        Returns: list[obj(snappi.Port)]
        """
        if 'ports' not in self._properties or self._properties['ports'] is None:
            self._properties['ports'] = PortList()
        return self._properties['ports']

    @property
    def lags(self):
        # type: () -> LagList
        """lags getter

        The lags that will be configured on the traffic generator.

        Returns: list[obj(snappi.Lag)]
        """
        if 'lags' not in self._properties or self._properties['lags'] is None:
            self._properties['lags'] = LagList()
        return self._properties['lags']

    @property
    def layer1(self):
        # type: () -> Layer1List
        """layer1 getter

        The layer1 settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Layer1)]
        """
        if 'layer1' not in self._properties or self._properties['layer1'] is None:
            self._properties['layer1'] = Layer1List()
        return self._properties['layer1']

    @property
    def captures(self):
        # type: () -> CaptureList
        """captures getter

        The capture settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Capture)]
        """
        if 'captures' not in self._properties or self._properties['captures'] is None:
            self._properties['captures'] = CaptureList()
        return self._properties['captures']

    @property
    def devices(self):
        # type: () -> DeviceList
        """devices getter

        The emulated device settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Device)]
        """
        if 'devices' not in self._properties or self._properties['devices'] is None:
            self._properties['devices'] = DeviceList()
        return self._properties['devices']

    @property
    def flows(self):
        # type: () -> FlowList
        """flows getter

        The flows that will be configured on the traffic generator.

        Returns: list[obj(snappi.Flow)]
        """
        if 'flows' not in self._properties or self._properties['flows'] is None:
            self._properties['flows'] = FlowList()
        return self._properties['flows']

    @property
    def options(self):
        # type: () -> ConfigOptions
        """options getter

        Global configuration options.

        Returns: obj(snappi.ConfigOptions)
        """
        if 'options' not in self._properties or self._properties['options'] is None:
            self._properties['options'] = ConfigOptions()
        return self._properties['options']
