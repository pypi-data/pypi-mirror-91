from .capturecustomfilter import CaptureCustomFilter
from .snappicommon import SnappiList
from .capturemacaddressfilter import CaptureMacAddressFilter
from .capturebasicfilter import CaptureBasicFilter


class CaptureBasicFilterList(SnappiList):
    def __init__(self):
        super(CaptureBasicFilterList, self).__init__()


    def basicfilter(self, and_operator=True, not_operator=False):
        # type: () -> CaptureBasicFilter
        """Factory method to create an instance of the snappi.capturebasicfilter.CaptureBasicFilter class

        A container for different types of basic capture filters.
        """
        item = CaptureBasicFilter(and_operator, not_operator)
        self._add(item)
        return self

    def mac_address(self, mac='None', filter=None, mask=None):
        # type: () -> CaptureBasicFilterList
        """Factory method to create an instance of the snappi.capturemacaddressfilter.CaptureMacAddressFilter class

        A container for a mac address capture filter.
        """
        item = CaptureBasicFilter()
        item.mac_address
        self._add(item)
        return self

    def custom(self, filter=None, mask=None, offset=None):
        # type: () -> CaptureBasicFilterList
        """Factory method to create an instance of the snappi.capturecustomfilter.CaptureCustomFilter class

        A container for a custom capture filter.
        """
        item = CaptureBasicFilter()
        item.custom
        self._add(item)
        return self
