# built-in
import re
from typing import Any, Dict


REX_NAME = re.compile(r'[-_.]+')
ALIASES = {
    'aaa': 'flake8-aaa',
    'flake-mutable': 'flake8-mutable',
    'flake8-pandas-vet': 'pandas-vet',
    'import-order': 'flake8-import-order',
    'logging-format': 'flake8-logging-format',
    'naming': 'pep8-naming',
    'pyflakes': 'pyflakes',
    'sql': 'flake8-sql',
    'use-fstring-format': 'flake8-use-fstring',
    'use-fstring-percent': 'flake8-use-fstring',
    'use-fstring-prefix': 'flake8-use-fstring',
}


def get_plugin_name(plugin: Dict[str, Any]) -> str:
    """Get plugin name from plugin info

    Users expect the same plugin name as the name of the package that provides plugin.
    However, that's not true for some plugins.
    Also, some plugins has different module name, that doesn't match to package.

    Lookup order:

    1. Ad-hoc aliases when nothing match
    2. Normalized name that starts with `flake8`
    3. Normalized name that starts with `pep`
    4. `plugin_name`
    """
    if not plugin:
        return 'UNKNOWN'
    if plugin['plugin_name'] in ALIASES:
        return ALIASES[plugin['plugin_name']]

    names = [plugin['plugin_name'], plugin['plugin'].__module__]
    names = [REX_NAME.sub('-', name).lower() for name in names]
    for name in names:
        if name.startswith('flake8'):
            return name
    for name in names:
        if name.startswith('pep8'):
            return name
    return names[0]
