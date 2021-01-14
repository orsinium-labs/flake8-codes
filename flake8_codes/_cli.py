import sys
from typing import Iterator, List, NamedTuple, NoReturn, TextIO

from flake8.main.application import Application

from ._codes import extract
from ._plugins import get_installed, Plugin


TEMPLATE = '{c.plugin.name:20} | {c.code:8} | {c.message}'


class Code(NamedTuple):
    code: str
    message: str
    plugin: Plugin


def normalize(name: str) -> str:
    return name.replace('-', '_').lower()


def get_codes(lookup_name: str) -> Iterator[Code]:
    app = Application()
    plugins = sorted(get_installed(app=app), key=lambda p: p.name)
    if not plugins:
        return

    checked = set()
    for plugin in plugins:
        if plugin.name in checked:
            continue
        checked.add(plugin.name)

        is_prefix = lookup_name.startswith(tuple(plugin.codes))
        is_name = normalize(lookup_name) == normalize(plugin.name)
        if not is_name and not is_prefix:
            continue

        try:
            codes = extract(plugin.name)
        except ImportError:
            continue
        for code in codes:
            if is_prefix and not code.startswith(lookup_name):
                continue
            yield Code(
                code=code,
                message=codes[code],
                plugin=plugin,
            )


def print_codes(lookup_name: str, stream: TextIO) -> int:
    count = 0
    for code in get_codes(lookup_name):
        count += 1
        print(TEMPLATE.format(c=code))
    return count


def main(argv: List[str], stream: TextIO) -> int:
    count = print_codes(argv[0], stream=stream)
    return int(count == 0)


def entrypoint() -> NoReturn:
    code = main(argv=sys.argv[1:], stream=sys.stdout)
    sys.exit(code)