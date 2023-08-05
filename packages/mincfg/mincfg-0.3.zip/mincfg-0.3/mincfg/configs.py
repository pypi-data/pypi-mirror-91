'''
Configurations are the way that multiple sources are glommed together.

MergedConfiguration merges multiple sources linearly, with later sources taking precedence over earlier ones.

'''

import logging
from types import SimpleNamespace
from typing import Dict, List, Optional

from .sources import ConfigSource, CfgDict

logger = logging.getLogger(__name__)


def _recursive_dict_update(main: Dict, update: Dict):
    '''
    like dict.update(), modifies the 'main' by applying 'update'
    UNLIKE dict.update(), normalizes all keys to lowercase
    '''
    for k, v in update.items():
        lk = k.lower()
        if isinstance(v, dict):
            main[lk] = main.get(lk, dict())
            logger.debug("dict %r %s recursing into dict %r to write %r", id(main), lk, id(main[lk]), v)
            _recursive_dict_update(main[lk], v)
        else:
            logger.debug("dict %r : %s -> %r", id(main), lk, v)
            main[lk] = v


class MergedConfiguration:
    '''
    Merges configuration sources, with later overriding earlier
    '''
    def __init__(self, sources: Optional[List[ConfigSource]] = None):
        self.sources: List[ConfigSource] = [] if sources is None else sources
        self._cfg: CfgDict = dict()
        self._loaded: bool = False

    def __repr__(self):
        return 'MergedConfiguration([' + ', '.join(repr(s) for s in self.sources) + ')'

    def add_source(self, source: ConfigSource):
        self.sources.append(source)

    def load(self):
        '''
        cause the config to be loaded; note that this need not be called directly, as it is lazily loaded.
        Subsequent calls _will_ re-load from the config sources.
        '''
        cfg: CfgDict = dict()
        for source in self.sources:
            updates = source.as_dict()
            _recursive_dict_update(cfg, updates)
        self._cfg = cfg
        self._loaded = True

    def as_dict(self) -> CfgDict:
        '''
        return the entire configuration as a single dictionary
        '''
        if not self._loaded:
            self.load()
        return self._cfg

    def get(self, key: str, namespace: Optional[List[str]]=None, default=None, parser=str, raise_error=True, doc=None):
        '''
        get a single config key
        a namespace is the 'path' in the config to the namespace to look the key up in
        default is the value to use if the key is not found
        parser is how to cast the result
        raise_error is whether to raise an error if the key is not found (note: supplying a default negates
            raise_error, as a (presumably) valid value is always available)
        doc is extra information to supply with the error message
        '''
        k = key.lower()
        ns = namespace or []
        in_ns = self.as_dict()
        for subns in ns:
            in_ns = in_ns[subns]
        if raise_error and default is None and k not in in_ns:
            msg = f"Missing config key {'.'.join(ns + [k])}"
            if doc:
                msg += f": {doc}"
            raise KeyError(msg)
        return parser(in_ns.get(k, default))

    def as_ns(self, namespace: List[str]) -> SimpleNamespace:
        '''
        return the config, or a namespace within it, as a SimpleNamespace
        '''
        in_ns = self.as_dict()
        for subns in namespace:
            in_ns = in_ns[subns]
        if not isinstance(in_ns, dict):
            raise ValueError("Need a sub-namespace (dict) to make a namespace")
        return SimpleNamespace(**in_ns)

