from .snappicommon import SnappiObject
from .bgpv4metriclist import Bgpv4MetricList


class Bgpv4Metrics(SnappiObject):
    _TYPES = {
        'ports': '.bgpv4metriclist.Bgpv4MetricList',
    }

    def __init__(self):
        super(Bgpv4Metrics, self).__init__()

    @property
    def ports(self):
        # type: () -> Bgpv4MetricList
        """ports getter

        TBD

        Returns: list[obj(snappi.Bgpv4Metric)]
        """
        if 'ports' not in self._properties or self._properties['ports'] is None:
            self._properties['ports'] = Bgpv4MetricList()
        return self._properties['ports']
