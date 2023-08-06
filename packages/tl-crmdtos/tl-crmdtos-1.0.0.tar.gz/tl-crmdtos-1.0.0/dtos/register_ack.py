from .register_info import RegisterInfo
from .crm_pkt_type import CrmPktType


class RegisterAck(object):
    """
    Registration information sent back to a particular worker after trying to register
    with a collector host.
    """
    def __init__(self, packet_id: str, info: 'RegisterInfo', packet_type: 'CrmPktType'):
        self.id = packet_id
        self.info = info
        self.type = packet_type

    def __str__(self):
        return "[{}] {} - {}".format(str(self.type), id, str(self.info))

    def __repr__(self):
        return "{}({} - {})".format(self.__class__.__name__,
                                    id,
                                    str(self.info))
