from typing import List, Dict


class RegisterInfo(object):
    """
    Detail information of the subscription between a worker with a collector host.
    """

    def __init__(self, status: bool, message: str, max_retries: int):
        self.status = status
        self.message = message,
        self.max_retries = max_retries

    def __repr__(self):
        return "{} - {} - max remaining retries: {}".format(self.status,
                                                            self.message,
                                                            self.max_retries)

    def __str__(self):
        return "{} - {} - max remaining retries: {}".format(self.status,
                                                            self.message,
                                                            self.max_retries)
