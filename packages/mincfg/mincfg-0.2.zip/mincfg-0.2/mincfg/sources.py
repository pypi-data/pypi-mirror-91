import os
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, Union, Any, Set

logger = logging.getLogger(__name__)

__all__ = [ 
    'CfgDict',
    'ConfigSource',
    'DictSource',
    'OSEnvironSource',
    'YamlFileSource',
    'SubsetSource',
]

#CfgDict = Dict[str, Union[str, 'CfgDict']]  # the correct, recursive type... unsupported by mypy
CfgDict = Dict[str, Any]


class ConfigSource(ABC):

    @abstractmethod
    def as_dict(self) -> CfgDict:
        '''
        return a dict containing configuration information from this source.

        NOTE: Errors _MUST_ _NOT_ be raised; in case of error, return as much configuration information as possible.
        An empty dict is acceptable (and expected, in cases where, for instance, the supplied configuration file
        doesn't exist)
        '''
        raise NotImplementedError


class DictSource(ConfigSource):
    '''
    Uses the supplied dict as a config source.  Useful for defaults.
    '''
    def __init__(self, cfg_dict: CfgDict):
        self.cfg = cfg_dict

    def as_dict(self) -> CfgDict:
        return self.cfg


class OSEnvironSource(ConfigSource):
    '''
    Uses os.environ as a config source, by parsing PREFIXd keys into hierarchical dictionaries, splitting on _
    '''
    def __init__(self, prefix: str):
        self.prefix: str = prefix.strip('_').upper() + '_'

    def as_dict(self) -> CfgDict:
        result: CfgDict = dict()
        for env_key in os.environ:
            if not env_key.startswith(self.prefix):
                continue
            key_path = env_key.split('_')[1:]
            if not key_path:
                continue
            *ns_list, key = key_path
            logger.debug("OSEnvironSource: %s -> %r,%s ", env_key, ns_list, key)
            namespace = result
            for subns in ns_list:
                namespace = namespace.setdefault(subns, dict())
            namespace[key] = os.environ[env_key]
        return result


class YamlFileSource(ConfigSource):
    '''
    A YAML file source of configuration information
    '''
    def __init__(self, filename: Union[Path, str]):
        self.path = Path(filename)

    def as_dict(self) -> CfgDict:
        # import yaml here so using the module won't fail if yaml isn't installed
        import yaml  # pylint: disable=import-outside-toplevel
        if not self.path.exists():
            return dict()
        if not self.path.is_file():
            return dict()
        with self.path.open() as f:
            return yaml.safe_load(f)


class SubsetSource(ConfigSource):
    '''
    Returns a sub-namespace of another source.  Useful with MergedConfiguration if you want partial overrides for
    precedence reasons. eg. source A's namespace  'A' should take priority over source B's namspace 'A', but source B's
    namespace 'B' should take priority over source A's namespace 'B'.
    '''
    def __init__(self, source: ConfigSource, keys: Set[str]):
        self.source = source
        self.keys = set(keys)

    def as_dict(self) -> CfgDict:
        full = self.source.as_dict()
        return { k: v for k, v in full.items() if k in self.keys }

