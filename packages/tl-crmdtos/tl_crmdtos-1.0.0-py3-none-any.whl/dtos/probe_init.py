from .host_info import HostInfo
from .crm_pkt_type import CrmPktType


class ProbeInit(object):
    """
    Collector information broadcast to all worker hosts in SonarThread
    """

    def __init__(self, packet_id: str, info: 'HostInfo', packet_type: 'CrmPktType'):
        self.id = packet_id
        self.info = info
        self.type = packet_type

    def __str__(self):
        return "[{}] {} - {}".format(str(self.type), self.id, str(self.info))

    def __repr__(self):
        return "{}({} - {})".format(self.__class__.__name__,
                                    self.id,
                                    str(self.info))
