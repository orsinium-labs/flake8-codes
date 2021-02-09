# built-in
import re
from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, Iterator, List, NamedTuple, Tuple

from flake8.main.application import Application
from flake8.plugins.manager import Plugin as Flake8Plugin

# app
from ._plugin import get_plugin_name

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata


REX_CODE = re.compile(r'^[A-Z]{1,5}[0-9]{0,5}$')

ALIASES = {
    'flake-mutable': ('M511', ),
    'flake8-annotations-complexity': ('TAE00', ),
    'flake8-bandit': ('S', ),
    'flake8-django': ('DJ', ),  # they say `DJ0` prefix but codes have `DJ10`
    'flake8-future-import': ('FI', ),
    'flake8-mock': ('M001', ),
    'flake8-pytest': ('T003', ),
    'logging-format': ('G', ),
    'pycodestyle': ('W', 'E'),
    'pylint': ('C', 'E', 'F', 'I', 'R', 'W'),
}
NAMESPACE = 'flake8.extension'


class Plugin(NamedTuple):
    check_type: str
    name: str
    codes: Tuple[str, ...]
    version: str


def get_installed(app: Application) -> Iterator[Plugin]:
    plugins_codes: DefaultDict[Tuple[str, str], List[str]]
    plugins_codes = defaultdict(list)
    versions = dict()
    codes: Iterable[str]

    entry_points = importlib_metadata.entry_points()[NAMESPACE]
    for entry_point in entry_points:
        plugin = Flake8Plugin(entry_point.name, entry_point, local=False)
        check_type = plugin.parameter_names[0]
        key = (check_type, get_plugin_name(plugin.to_dictionary()))
        versions[key[-1]] = plugin.version

        # if codes for plugin specified explicitly in ALIASES, use it
        codes = ALIASES.get(plugin.plugin_name, [])
        if codes:
            plugins_codes[key] = list(codes)
            continue

        # otherwise get codes from plugin entrypoint
        code = plugin.name
        if not REX_CODE.match(code):
            raise ValueError('Invalid code format: {}'.format(code))
        plugins_codes[key].append(code)

    if 'flake8-docstrings' in versions:
        versions['flake8-docstrings'] = versions['flake8-docstrings'].split(',')[0]

    for (check_type, name), codes in plugins_codes.items():
        yield Plugin(
            check_type=check_type,
            name=name,
            codes=tuple(sorted(codes)),
            version=versions[name],
        )
