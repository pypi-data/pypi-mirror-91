from .snappicommon import SnappiObject


class PortMetricsRequest(SnappiObject):
    TRANSMIT = 'transmit'
    LOCATION = 'location'
    LINK = 'link'
    CAPTURE = 'capture'
    FRAMES_TX = 'frames_tx'
    FRAMES_RX = 'frames_rx'
    BYTES_TX = 'bytes_tx'
    BYTES_RX = 'bytes_rx'
    FRAMES_TX_RATE = 'frames_tx_rate'
    FRAMES_RX_RATE = 'frames_rx_rate'
    BYTES_TX_RATE = 'bytes_tx_rate'
    BYTES_RX_RATE = 'bytes_rx_rate'

    def __init__(self, port_names=None, column_names=None):
        super(PortMetricsRequest, self).__init__()
        self.port_names = port_names
        self.column_names = column_names

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The names of objects to return results for. An empty list will return all port row results.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The names of objects to return results for. An empty list will return all port row results.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def column_names(self):
        # type: () -> list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned. The name of the port cannot be excluded.

        Returns: list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """
        return self._properties['column_names']

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned. The name of the port cannot be excluded.

        value: list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """
        self._properties['column_names'] = value
