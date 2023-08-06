class PortInfo(object):
    """
    Define structure of the information of a pair daemon:port that
    will be exchanged via ProbeInit/ProbeAck packets between worker and collector hosts
    """
    def __init__(self, daemon_name: str, port: int):
        self.daemon = daemon_name
        self.port = port

    def __str__(self):
        return "{}:{}".format(self.daemon,
                              self.port)

    def __repr__(self):
        return "{}:{}".format(self.daemon,
                              self.port)
