# external
import pytest

# project
from flake8_codes import extract
from flake8_codes._codes._default import extract_default
from flake8_codes._codes._registry import registry

# app
from ._constants import KNOWN_PLUGINS


@pytest.mark.parametrize('plugin_name', KNOWN_PLUGINS)
def test_smoke_extract(plugin_name):
    codes = extract(plugin_name)
    assert codes

    for code, msg in codes.items():
        assert type(code) is str, 'bad code type'
        assert type(msg) is str, 'bad message type'

        # that's not exactly true but all plugins follow this convention
        assert code[0].isalpha(), 'code must start from letter'
        assert code[0].isupper(), 'code must be uppercase'


@pytest.mark.parametrize('plugin_name', KNOWN_PLUGINS)
def test_no_custom_extractor_needed(plugin_name):
    extractor = registry.get(plugin_name)
    if extractor is None:
        return
    custom_codes = extractor()
    default_codes = extract_default(plugin_name)
    assert default_codes != custom_codes
