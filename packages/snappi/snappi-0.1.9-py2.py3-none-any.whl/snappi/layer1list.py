from .layer1 import Layer1
from .snappicommon import SnappiList


class Layer1List(SnappiList):
    def __init__(self):
        super(Layer1List, self).__init__()


    def layer1(self, port_names=None, speed='speed_10_gbps', media='None', promiscuous=False, mtu=1500, ieee_media_defaults=True, auto_negotiate=True, name=None):
        # type: () -> Layer1
        """Factory method to create an instance of the snappi.layer1.Layer1 class

        A container for layer1 settings.
        """
        item = Layer1(port_names, speed, media, promiscuous, mtu, ieee_media_defaults, auto_negotiate, name)
        self._add(item)
        return self
