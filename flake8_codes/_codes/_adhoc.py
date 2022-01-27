# built-in
import re
from contextlib import suppress
from importlib import import_module
from pathlib import Path
from typing import Dict

# app
from ._default import extract_default
from ._registry import registry


@registry.add
def extract_flake8_commas() -> Dict[str, str]:
    # external
    from flake8_commas._base import ERRORS

    return dict(ERRORS.values())


@registry.add
def extract_flake8_debugger() -> Dict[str, str]:
    # external
    from flake8_debugger import DEBUGGER_ERROR_CODE
    return {DEBUGGER_ERROR_CODE: 'trace found'}


@registry.add
def extract_flake8_mutable() -> Dict[str, str]:
    # external
    from mutable_defaults import MutableDefaultChecker

    return {MutableDefaultChecker._code: MutableDefaultChecker._error_tmpl}


@registry.add
def extract_flake8_fixme() -> Dict[str, str]:
    # external
    from flake8_fixme import WORD_CODES

    return {code: 'fixme found ({})'.format(word) for word, code in WORD_CODES.items()}


@registry.add
def extract_pep8_naming() -> Dict[str, str]:
    # external
    import pep8ext_naming

    codes = dict()
    for checker_name in dir(pep8ext_naming):
        if not checker_name.endswith('Check'):
            continue
        checker = getattr(pep8ext_naming, checker_name)
        for code, message in checker.__dict__.items():
            if code[0] == 'N':
                codes[code] = message
    return codes


@registry.add
def extract_flake8_pyi() -> Dict[str, str]:
    # external
    import pyi
    codes = dict()
    for name, value in vars(pyi).items():
        if name.startswith('Y0'):
            codes[name] = value
    return codes


@registry.add
def extract_flake8_pytest_style() -> Dict[str, str]:
    # external
    from flake8_pytest_style import errors
    codes = dict()
    for error in vars(errors).values():
        if error is errors.Error:
            continue
        if not isinstance(error, type):
            continue
        if not issubclass(error, errors.Error):
            continue
        codes[error.code] = error.message  # type: ignore
    return codes


@registry.add
def extract_flake8_annotations_complexity() -> Dict[str, str]:
    # external
    from flake8_annotations_complexity.checker import AnnotationsComplexityChecker

    with suppress(ImportError):
        codes = extract_default('flake8_annotations_complexity.ast_helpers')
        if codes:
            return codes

    code, message = AnnotationsComplexityChecker._error_message_template.split(' ', maxsplit=1)
    return {code: message}


@registry.add
def extract_flake8_future_import() -> Dict[str, str]:
    # external
    from flake8_future_import import ALL_FEATURES
    codes = dict()
    tmpl = 'FI{}'
    for feature in ALL_FEATURES:
        code = tmpl.format(10 + feature.index)
        codes[code] = '__future__ import "{}" missing'.format(feature.name)
        code = tmpl.format(50 + feature.index)
        codes[code] = '__future__ import "{}" present'.format(feature.name)
    codes[tmpl.format(90)] = '__future__ import does not exist'
    return codes


@registry.add
def extract_flake8_string_format() -> Dict[str, str]:
    # external
    from flake8_string_format import StringFormatChecker

    return {'P{}'.format(c): m for c, m in StringFormatChecker.ERRORS.items()}


@registry.add
def extract_flake8_bandit() -> Dict[str, str]:
    # external
    from bandit.core.extension_loader import MANAGER

    codes = dict()
    for blacklist in MANAGER.blacklist.values():
        for check in blacklist:
            code = check['id'].replace('B', 'S')
            codes[code] = check['message']
    for plugin in MANAGER.plugins:
        code = plugin.plugin._test_id.replace('B', 'S')
        codes[code] = plugin.name.replace('_', ' ')
    return codes


@registry.add
def extract_pylint() -> Dict[str, str]:
    # external
    import pylint.checkers
    try:
        # external
        from pylint.lint import MSGS
    except ImportError:
        # external
        from pylint.lint.pylinter import MSGS

    codes = dict()
    for code, (msg, alias, *_) in MSGS.items():
        if msg in ('%s', '%s: %s'):
            msg = alias.replace('-', ' ')
        codes[code] = msg.replace('\n', ' ')

    for path in Path(pylint.checkers.__path__[0]).iterdir():
        module = import_module('pylint.checkers.' + path.stem)
        for class_name in dir(module):
            cls = getattr(module, class_name, None)
            msgs = getattr(cls, 'msgs', None)
            if not msgs:
                continue
            for code, (msg, alias, *_) in msgs.items():
                if msg in ('%s', '%s: %s'):
                    msg = alias.replace('-', ' ')
                codes[code] = msg.replace('\n', ' ')
    return codes


@registry.add
def extract_pyflakes() -> Dict[str, str]:
    # external
    from flake8.plugins.pyflakes import FLAKE8_PYFLAKES_CODES
    from pyflakes import messages

    codes = dict()
    for class_name, code in FLAKE8_PYFLAKES_CODES.items():
        codes[code] = getattr(messages, class_name).message
    return codes


@registry.add
def extract_flake8_rst_docstrings() -> Dict[str, str]:
    # external
    from flake8_rst_docstrings import code_mappings_by_level

    codes = dict()
    for level, codes_mapping in code_mappings_by_level.items():
        for message, number in codes_mapping.items():
            code = 'RST{}{:02d}'.format(level, number)
            codes[code] = message
    return codes


@registry.add
def extract_flake8_django() -> Dict[str, str]:
    # external
    import flake8_django.checkers

    codes = dict()
    for path in Path(flake8_django.checkers.__path__[0]).iterdir():
        module = import_module('flake8_django.checkers.' + path.stem)
        for class_name in dir(module):
            cls = getattr(module, class_name, None)
            if not hasattr(cls, 'code'):
                continue
            if '0' not in cls.__name__:
                continue
            codes[cls.__name__] = cls.description
    return codes


@registry.add
def extract_flake8_scrapy() -> Dict[str, str]:
    # external
    from flake8_scrapy import ScrapyStyleIssueFinder

    codes = dict()
    for finders in ScrapyStyleIssueFinder().finders.values():
        for finder in finders:
            codes[finder.msg_code] = finder.msg_info
    return codes


@registry.add
def extract_flake8_executable() -> Dict[str, str]:
    # external
    import flake8_executable

    path = Path(flake8_executable.__file__)
    content = path.read_text()
    codes = dict()
    for code, msg in re.findall(r"'(EXE00\d)', '(.*)'", content):
        codes[code] = msg
    return codes


@registry.add
def extract_flake8_strict() -> Dict[str, str]:
    # external
    from flake8_strict import ErrorCode

    codes = dict()
    for code, message in ErrorCode._member_map_.items():
        codes[code] = message.value
    return codes


@registry.add
def extract_flake8_docstrings() -> Dict[str, str]:
    # external
    from pydocstyle.violations import ErrorRegistry

    codes = dict()
    for group in ErrorRegistry.groups:
        for error in group.errors:
            codes[error.code] = error.short_desc
    return codes


@registry.add
def extract_dlint() -> Dict[str, str]:
    # external
    from dlint.linters import ALL

    codes = dict()
    for linter in ALL:
        code, msg = linter._error_tmpl.split(' ', maxsplit=1)
        codes[code] = msg
    return codes


@registry.add
def extract_flake8_mock() -> Dict[str, str]:
    # external
    from flake8_mock import ERROR_MESSAGE, MOCK_ERROR_CODE

    message = ERROR_MESSAGE.split(' ', maxsplit=1)[1]
    return {MOCK_ERROR_CODE: message}


@registry.add
def extract_flake8_pytest() -> Dict[str, str]:
    # external
    from flake8_pytest import PYTEST_ERROR_CODE, PYTEST_ERROR_MESSAGE

    return {PYTEST_ERROR_CODE: PYTEST_ERROR_MESSAGE}


@registry.add
def extract_flake8_length() -> Dict[str, str]:
    # external
    from flake8_length._parser import Message

    return {message.name: message.value for message in Message}


@registry.add
def extract_wemake_python_styleguide() -> Dict[str, str]:
    # external
    from wemake_python_styleguide import violations

    codes = dict()
    for path in Path(violations.__path__[0]).iterdir():
        module = import_module('wemake_python_styleguide.violations.' + path.stem)
        for checker_name in dir(module):
            if not checker_name.endswith('Violation'):
                continue
            checker = getattr(module, checker_name)
            if not hasattr(checker, 'code'):
                continue
            code = 'WPS' + str(checker.code).zfill(3)
            codes[code] = checker.error_template
    return codes
