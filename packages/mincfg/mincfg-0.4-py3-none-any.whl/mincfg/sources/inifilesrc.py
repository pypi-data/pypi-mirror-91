from pathlib import Path
from typing import Union

from configobj import ConfigObj  # type: ignore

from .abstract import ConfigSource, CfgDict


class INIFileSource(ConfigSource):
    '''
    An INI-file source of configuration information
    '''
    def __init__(self, filename: Union[Path, str]):
        self.filename = str(filename)

    def as_dict(self) -> CfgDict:
        return ConfigObj(self.filename)

