from .snappicommon import SnappiList
from .capture import Capture


class CaptureList(SnappiList):
    def __init__(self):
        super(CaptureList, self).__init__()


    def capture(self, port_names=None, pcap=None, enable=True, overwrite=False, format='pcap', name=None):
        # type: () -> Capture
        """Factory method to create an instance of the snappi.capture.Capture class

        Container for capture settings.
        """
        item = Capture(port_names, pcap, enable, overwrite, format, name)
        self._add(item)
        return self
