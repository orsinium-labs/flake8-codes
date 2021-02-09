# built-in
import sys
from argparse import ArgumentParser
from typing import Iterator, List, NamedTuple, NoReturn, TextIO

# app
from ._codes import extract
from ._plugins import Plugin, get_installed


TEMPLATE = '{c.plugin.name:20} | {c.code:8} | {c.message}'


class Code(NamedTuple):
    code: str
    message: str
    plugin: Plugin


def normalize(name: str) -> str:
    return name.replace('-', '_').lower()


def get_codes(lookup_name: str) -> Iterator[Code]:
    plugins = sorted(get_installed(), key=lambda p: p.name)
    if not plugins:
        return

    checked = set()
    for plugin in plugins:
        if plugin.name in checked:
            continue
        checked.add(plugin.name)

        is_prefix = lookup_name.startswith(tuple(plugin.codes))
        is_name = normalize(lookup_name) == normalize(plugin.name)
        if lookup_name and not is_name and not is_prefix:
            continue

        try:
            codes = extract(plugin.name)
        except ImportError:
            continue
        for code in sorted(codes):
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
        print(TEMPLATE.format(c=code), file=stream)
    return count


def main(argv: List[str], stream: TextIO) -> int:
    parser = ArgumentParser()
    parser.add_argument('lookup_name', nargs='?', help='plugin name, code, or prefix')
    args = parser.parse_args(argv)
    lookup_name = args.lookup_name or ''

    count = print_codes(lookup_name, stream=stream)
    return int(count == 0)


def entrypoint() -> NoReturn:
    code = main(argv=sys.argv[1:], stream=sys.stdout)
    sys.exit(code)
