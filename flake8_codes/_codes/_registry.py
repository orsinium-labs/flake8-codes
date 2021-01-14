

# built-in
from typing import Callable, Dict, Optional


ExtractorType = Callable[[], Dict[str, str]]


class Registry:
    _extractors: Dict[str, ExtractorType]
    _prefix = 'extract_'

    def __init__(self) -> None:
        self._extractors = {}

    def add(self, func: ExtractorType) -> ExtractorType:
        name = func.__name__
        assert name.startswith(self._prefix)
        name = name[len(self._prefix):]
        self._extractors[name] = func
        return func

    def get(self, name: str) -> Optional[ExtractorType]:
        return self._extractors.get(name)


registry = Registry()
