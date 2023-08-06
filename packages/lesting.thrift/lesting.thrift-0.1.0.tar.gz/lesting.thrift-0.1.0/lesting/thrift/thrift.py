__all__ = [
    "TClient",
    "TPoolClient"
]

from typing import Optional, Any
from .transport.base import TTransportFactory
from .protocol.base import TProtocolFactory
from thriftpy2.thrift import TPayload, TClient
from threading import Semaphore
from queue import LifoQueue, Empty

class TPoolClient(TClient):

    _trans: TTransportFactory
    _iprot: TProtocolFactory
    _oprot: TProtocolFactory
    semaphore: Semaphore
    queue: LifoQueue

    def __init__(self, service, trans_factory: TTransportFactory, iprot_factory: TProtocolFactory, oprot_factory: Optional[TProtocolFactory] = None, max_connections: int = 10):
        super().__init__(service, iprot_factory, oprot_factory)
        self._trans = trans_factory
        self.semaphore = Semaphore(max_connections)
        self.queue = LifoQueue(max_connections)

    def _req(self, _api: TPayload, *args: Any, **kwargs: Any) -> TPayload:
        self.semaphore.acquire()
        try:
            client = self.queue.get(False)
        except Empty:
            transport = self._trans.get_transport()
            client = TClient(self._service, self._iprot.get_protocol(transport), self._oprot.get_protocol(transport))
        try:
            return client._req(_api, *args, **kwargs)
        finally:
            self.queue.put(client)
            self.semaphore.release()