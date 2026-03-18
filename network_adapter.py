import sys


class NetworkAdapter:
    def get_socket_pool(self):
        pass

    def get_ssl_context(self):
        pass


class CircuitPythonNetworkAdapter(NetworkAdapter):
    def __init__(self):
        import socketpool
        import wifi

        self._pool = socketpool.SocketPool(wifi.radio)

    def get_socket_pool(self):
        return self._pool

    def get_ssl_context(self):
        return None


class CPythonNetworkAdapter(NetworkAdapter):
    def __init__(self):
        import adafruit_connection_manager
        from adafruit_connection_manager import CPythonNetwork

        radio = CPythonNetwork()
        self._pool = adafruit_connection_manager.get_radio_socketpool(radio)
        self._ssl_context = adafruit_connection_manager.get_radio_ssl_context(radio)

    def get_socket_pool(self):
        return self._pool

    def get_ssl_context(self):
        return self._ssl_context


class NetworkAdapterFactory:
    @staticmethod
    def create():
        if sys.implementation.name == "circuitpython":
            print("Using CircuitPython network adapter")
            return CircuitPythonNetworkAdapter()
        print("Using CPython network adapter")
        return CPythonNetworkAdapter()
