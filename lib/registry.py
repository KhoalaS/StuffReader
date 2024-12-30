from lib.extension import Extension
from lib.console import Console


class Registry:
    _map: dict[str, Extension] = {}

    def __init__(self):
        pass

    def getExtensions(self):
        return self._map.items()

    def getExtension(self, ext_handle: str):
        for (k, ext) in self._map.items():
            if ext.handle == ext_handle:
                return ext
        return None

    def register(self, ext: Extension):
        if self._map.get(ext.handle) is None:
            self._map.update({ext.handle: ext})
            Console.Log("Added extension with handle '@{}'".format(ext.handle))
        else:
            Console.Error("Extension '@{}' already exists".format(ext.handle))
