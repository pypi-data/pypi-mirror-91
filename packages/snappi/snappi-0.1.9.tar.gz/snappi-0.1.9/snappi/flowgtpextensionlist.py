from .flowgtpextension import FlowGtpExtension
from .snappicommon import SnappiList


class FlowGtpExtensionList(SnappiList):
    def __init__(self):
        super(FlowGtpExtensionList, self).__init__()


    def gtpextension(self):
        # type: () -> FlowGtpExtension
        """Factory method to create an instance of the snappi.flowgtpextension.FlowGtpExtension class

        TBD
        """
        item = FlowGtpExtension()
        self._add(item)
        return self
