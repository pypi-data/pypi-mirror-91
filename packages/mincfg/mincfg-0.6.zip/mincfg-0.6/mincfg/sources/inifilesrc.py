import os.path
from pathlib import Path
from typing import Union

from configobj import ConfigObj  # type: ignore

from .abstract import ConfigSource, CfgDict


class INIFileSource(ConfigSource):
    """
    An INI-file source of configuration information
    """
    def __init__(self, filename: Union[Path, str]):
        self.filename = str(filename) if filename is not None else None

    def as_dict(self) -> CfgDict:
        if self.filename is None:
            return dict()
        if not os.path.exists(self.filename):
            return dict()
        if not os.path.isfile(self.filename):
            return dict()
        return ConfigObj(self.filename)
