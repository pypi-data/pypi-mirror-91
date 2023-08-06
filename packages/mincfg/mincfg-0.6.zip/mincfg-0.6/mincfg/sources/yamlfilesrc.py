from pathlib import Path
from typing import Union

from .abstract import ConfigSource, CfgDict

import yaml


class YamlFileSource(ConfigSource):
    """
    A YAML file source of configuration information
    """

    def __init__(self, filename: Union[Path, str]):
        self.path = Path(filename) if filename else None

    def as_dict(self) -> CfgDict:
        if self.path is None:
            return dict()
        if not self.path.exists():
            return dict()
        if not self.path.is_file():
            return dict()
        with self.path.open() as f:
            return yaml.safe_load(f)
