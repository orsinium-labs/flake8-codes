# built-in
from unittest.mock import patch

# external
import pytest

# project
from flake8_codes import extract, get_installed

# app
from ._constants import KNOWN_PLUGINS


@patch('sys.argv', ['flake8'])
@pytest.mark.parametrize('plugin_name', KNOWN_PLUGINS)
def test_smoke_prefixes(plugin_name):
    plugins = {plugin.name: plugin for plugin in get_installed()}
    plugin = plugins[plugin_name]

    codes = extract(plugin_name)
    for code in codes:
        print(plugin_name, code, plugin.codes)
        assert code.startswith(plugin.codes)
