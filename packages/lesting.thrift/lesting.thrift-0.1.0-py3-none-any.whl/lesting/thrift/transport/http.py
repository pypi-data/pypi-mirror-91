__all__ = [
    "THttpClient",
    "THttpClientFactory"
]

from typing import Dict, Optional, Tuple
from .base import TTransport, TTransportFactory
from lesting.http import Http
from io import BytesIO

class THttpClient(TTransport):

    uri: str
    source_address: Tuple[str, int]
    headers: Dict[str, str]
    http: Http
    wbuf: BytesIO
    last: int
    response: bytes

    def __init__(self, uri: str, source_address: Optional[Tuple[str, int]] = None) -> None:
        self.uri = uri
        self.source_address = source_address
        self.headers = {
            "Content-Type": "application/x-thrift"
        }
        self.http = None
        self.wbuf = BytesIO()

    def is_open(self) -> bool:
        return self.http is not None

    def open(self) -> None:
        self.http = Http(source_address = self.source_address)

    def close(self) -> None:
        self.http.close()
        self.http = None

    def read(self, sz: int) -> bytes:
        min = self.last
        self.last += sz
        return self.response[min:self.last]

    def write(self, buf) -> None:
        self.wbuf.write(buf)

    def flush(self):
        if not self.is_open(): self.open()
        _, self.response = self.http.request(self.uri, "POST", self.wbuf.getvalue(), self.headers)
        self.wbuf.truncate()
        self.last = 0

class THttpClientFactory(TTransportFactory):

    uri: str
    source_address: Tuple[str, int]
    headers: Dict[str, str]

    def __init__(self, uri: str, source_address: Optional[Tuple[str, int]] = None) -> None:
        self.uri = uri
        self.source_address = source_address
        self.headers = {
            "Content-Type": "application/x-thrift"
        }

    def get_transport(self) -> THttpClient:
        transport = THttpClient(self.uri, self.source_address)
        transport.headers = self.headers
        return transport