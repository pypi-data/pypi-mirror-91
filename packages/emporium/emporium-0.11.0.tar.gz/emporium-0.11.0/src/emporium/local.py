import os

import smart_open as smart

from emporium.base import AbstractStore, Entry
from emporium.utils import is_write_mode, select_keys


class LocalStore(AbstractStore):
    """Store that puts data on the local disk."""

    def __init__(self, base_path=None):
        """Instantiate a store.

        :param base_path: The root path of the store.

        :returns: Instance that implements :class:`~emporium.base.AbstractStore`.
        """
        self._base_path = base_path

    @classmethod
    def from_config(cls, config):
        return cls(**select_keys(config, "base_path"))

    def open(self, path, mode, *args, **kwargs):
        expanded_path = self._expand(path)
        if is_write_mode(mode):
            self._ensure_dir_exists(expanded_path)
        return smart.open(expanded_path, mode, *args, **kwargs)

    def substore(self, path):
        return self.__class__(os.path.join(self._base_path, path))

    def _expand(self, path=None):
        segments = [s for s in [self._base_path, path] if s]
        if segments:
            return os.path.join(*segments)
        return ""

    def location(self, path=None):
        return self._expand(path)

    def list(self, path=None):
        path = self._expand(path)
        seen = set()
        for entry in os.scandir(path):
            if entry.is_dir():
                entry_tuple = Entry(entry.name.split(os.sep)[0], "directory")
            else:
                entry_tuple = Entry(entry.name.split(os.sep)[0], "file")
            if entry_tuple not in seen:
                yield entry_tuple
                seen.add(entry_tuple)

    @staticmethod
    def _ensure_dir_exists(full_path):
        try:
            os.makedirs(os.path.dirname(full_path))
        except OSError:
            pass

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self._expand())
