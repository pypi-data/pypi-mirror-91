__all__ = [
    "TProtocol",
    "TProtocolFactory"
]

from typing import TYPE_CHECKING
from thriftpy2.protocol.base import TProtocolBase as TProtocol

if TYPE_CHECKING:
    from ..transport.base import TTransport

class TProtocolFactory(TProtocol):

    def get_protocol(self, trans: "TTransport") -> TProtocol:
        raise NotImplementedError