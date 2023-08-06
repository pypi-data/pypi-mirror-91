__all__ = [
    "TTransport",
    "TTransportFactory"
]

from thriftpy2.transport.base import TTransportBase as TTransport

class TTransportFactory:

    def get_transport(self) -> TTransport:
        raise NotImplementedError