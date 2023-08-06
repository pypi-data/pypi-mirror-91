__all__ = [
    "Http"
]

from typing import Optional, Union, Tuple, Any
import httplib2
import http.client

class HTTPConnection(http.client.HTTPConnection):

    source_address: Optional[Tuple[str, int]]

    def __init__(self, *args: Any, proxy_info: Optional[httplib2.ProxyInfo] = None, **kwargs: Any):
        super().__init__(*args, **kwargs)

class HTTPSConnection(http.client.HTTPSConnection):

    source_address: Optional[Tuple[str, int]]

    def __init__(self, *args, proxy_info: Optional[httplib2.ProxyInfo] = None, **kwargs):
        super().__init__(*args, **kwargs)

httplib2.SCHEME_TO_CONNECTION["http"] = HTTPConnection
httplib2.SCHEME_TO_CONNECTION["https"] = HTTPSConnection

class Connections(dict):

    source_address: Optional[Tuple[str, int]]

    def __init__(self, source_address: Optional[Tuple[str, int]]):
        self.source_address = source_address

    def __setitem__(self, key: Any, connection: Union[Union[HTTPConnection, HTTPSConnection], Any]):
        if isinstance(connection, (HTTPConnection, HTTPSConnection)):
            connection.source_address = self.source_address
        super().__setitem__(key, connection)

class Http(httplib2.Http):

    source_address: str
    connections: Connections

    def __init__(self, *args: Any, source_address: Optional[Tuple[str, int]] = None, **kwargs: Any) -> None:
        self.source_address = source_address
        super().__init__(*args, **kwargs)
        self.connections = Connections(self.source_address)