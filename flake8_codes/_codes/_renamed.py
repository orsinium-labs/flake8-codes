# built-in
from typing import Dict

# app
from ._default import extract_default
from ._registry import registry


@registry.add
def extract_flake8_absolute_import() -> Dict[str, str]:
    return extract_default(name='flake8_absolute_import.core')


@registry.add
def extract_flake8_aaa() -> Dict[str, str]:
    return extract_default(name='flake8_aaa.line_markers')


@registry.add
def extract_flake8_cognitive_complexity() -> Dict[str, str]:
    return extract_default(name='flake8_cognitive_complexity.checker')


@registry.add
def extract_flake8_variables_names() -> Dict[str, str]:
    return extract_default(name='flake8_variables_names.checker')


@registry.add
def extract_logging_format() -> Dict[str, str]:
    return extract_default(name='logging_format.violations')


@registry.add
def extract_flake8_sql() -> Dict[str, str]:
    return extract_default(name='flake8_sql.linter')


@registry.add
def extract_flake8_requirements() -> Dict[str, str]:
    return extract_default(name='flake8_requirements.checker')


@registry.add
def extract_flake8_expression_complexity() -> Dict[str, str]:
    return extract_default(name='flake8_expression_complexity.checker')


@registry.add
def extract_flake8_use_fstring() -> Dict[str, str]:
    codes = dict()
    codes.update(extract_default(name='flake8_use_fstring.format'))
    codes.update(extract_default(name='flake8_use_fstring.percent'))
    # https://github.com/MichaelKim0407/flake8-use-fstring/pull/2
    try:
        codes.update(extract_default(name='flake8_use_fstring.prefix'))
    except ImportError:
        pass
    return codes


@registry.add
def extract_flake8_functions() -> Dict[str, str]:
    codes = dict()
    codes.update(extract_default('flake8_functions.checker'))
    try:
        codes.update(extract_default('flake8_functions.function_arguments_amount'))
        codes.update(extract_default('flake8_functions.function_lenght'))
        codes.update(extract_default('flake8_functions.function_purity'))
    except ImportError:
        pass
    return codes
