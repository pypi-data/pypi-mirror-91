from .snappicommon import SnappiObject


class Layer1AutoNegotiation(SnappiObject):
    def __init__(self, advertise_1000_mbps=None, advertise_100_fd_mbps=None, advertise_100_hd_mbps=None, advertise_10_fd_mbps=None, advertise_10_hd_mbps=None, link_training=None, rs_fec=None):
        super(Layer1AutoNegotiation, self).__init__()
        self.advertise_1000_mbps = advertise_1000_mbps
        self.advertise_100_fd_mbps = advertise_100_fd_mbps
        self.advertise_100_hd_mbps = advertise_100_hd_mbps
        self.advertise_10_fd_mbps = advertise_10_fd_mbps
        self.advertise_10_hd_mbps = advertise_10_hd_mbps
        self.link_training = link_training
        self.rs_fec = rs_fec

    @property
    def advertise_1000_mbps(self):
        # type: () -> boolean
        """advertise_1000_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_1000_mbps']

    @advertise_1000_mbps.setter
    def advertise_1000_mbps(self, value):
        """advertise_1000_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_1000_mbps'] = value

    @property
    def advertise_100_fd_mbps(self):
        # type: () -> boolean
        """advertise_100_fd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_100_fd_mbps']

    @advertise_100_fd_mbps.setter
    def advertise_100_fd_mbps(self, value):
        """advertise_100_fd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_100_fd_mbps'] = value

    @property
    def advertise_100_hd_mbps(self):
        # type: () -> boolean
        """advertise_100_hd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_100_hd_mbps']

    @advertise_100_hd_mbps.setter
    def advertise_100_hd_mbps(self, value):
        """advertise_100_hd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_100_hd_mbps'] = value

    @property
    def advertise_10_fd_mbps(self):
        # type: () -> boolean
        """advertise_10_fd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_10_fd_mbps']

    @advertise_10_fd_mbps.setter
    def advertise_10_fd_mbps(self, value):
        """advertise_10_fd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_10_fd_mbps'] = value

    @property
    def advertise_10_hd_mbps(self):
        # type: () -> boolean
        """advertise_10_hd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_10_hd_mbps']

    @advertise_10_hd_mbps.setter
    def advertise_10_hd_mbps(self, value):
        """advertise_10_hd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_10_hd_mbps'] = value

    @property
    def link_training(self):
        # type: () -> boolean
        """link_training getter

        Enable/disable gigabit ethernet link training.

        Returns: boolean
        """
        return self._properties['link_training']

    @link_training.setter
    def link_training(self, value):
        """link_training setter

        Enable/disable gigabit ethernet link training.

        value: boolean
        """
        self._properties['link_training'] = value

    @property
    def rs_fec(self):
        # type: () -> boolean
        """rs_fec getter

        Enable/disable gigabit ethernet reed solomon forward error correction (RS FEC).

        Returns: boolean
        """
        return self._properties['rs_fec']

    @rs_fec.setter
    def rs_fec(self, value):
        """rs_fec setter

        Enable/disable gigabit ethernet reed solomon forward error correction (RS FEC).

        value: boolean
        """
        self._properties['rs_fec'] = value
