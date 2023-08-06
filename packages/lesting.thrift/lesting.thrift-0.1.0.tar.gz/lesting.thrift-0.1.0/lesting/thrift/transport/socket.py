__all__ = [
    "TSocket",
    "TSocketFactory"
]

from typing import Optional
from .base import TTransportFactory
from thriftpy2.transport.socket import TSocket
import socket

class TSocketFactory(TTransportFactory):

    host: str
    port: int
    unix_socket: str
    sock: socket.socket
    socket_family: socket.AddressFamily
    socket_timeout: int
    connect_timeout: int

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, unix_socket: Optional[str] = None, sock: Optional[socket.socket] = None, socket_family: socket.AddressFamily = socket.AF_INET, socket_timeout: int = 3000, connect_timeout: Optional[int] = None) -> None:
        self.host = host
        self.port = port
        self.unix_socket = unix_socket
        self.sock = sock
        self.socket_family = socket_family
        self.socket_timeout = socket_timeout
        self.connect_timeout = connect_timeout

    def get_transport(self) -> TSocket:
        return TSocket(self.host, self.port, self.unix_socket, self.sock, self.socket_family, self.socket_timeout, self.connect_timeout)