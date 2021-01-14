# built-in
from typing import Dict

# app
from ._registry import registry


@registry.add
def extract_flake8_spellcheck() -> Dict[str, str]:
    return {
        'SC100': 'Spelling error in comments',
        'SC200': 'Spelling error in name',
    }


@registry.add
def extract_flake8_import_order() -> Dict[str, str]:
    return {
        'I666': 'Import statement mixes groups.',
        'I100': 'Import statements are in the wrong order.',
        'I101': 'Imported names are in the wrong order.',
        'I201': 'Missing newline between import groups.',
        'I202': 'Additional newline in a group of imports.',
    }


@registry.add
def extract_flake8_black() -> Dict[str, str]:
    # external
    from flake8_black import black_prefix

    return {
        black_prefix + '901': 'Invalid input',
        black_prefix + '997': 'Invalid TOML file',
        black_prefix + '999': 'Unexpected exception',
    }


@registry.add
def extract_flake8_alfred() -> Dict[str, str]:
    return {'B1': 'banned symbol'}


@registry.add
def extract_flake8_eradicate() -> Dict[str, str]:
    return {'E800': 'Found commented out code: {0}'}
