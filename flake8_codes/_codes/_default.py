# built-in
import ast
import re
from importlib import import_module
from pathlib import Path
from typing import Dict, List


REX_CODE = re.compile(r'^[A-Z]{1,5}[0-9]{1,5}$')


class CollectStrings(ast.NodeVisitor):
    _strings: List[str]

    def visit_Str(self, node):
        self._strings.append(node.s)


def get_messages(code: str, content: str) -> Dict[str, str]:
    root = ast.parse(content)
    CollectStrings._strings = []
    collector = CollectStrings()
    collector.visit(root)

    messages = dict()
    for message in collector._strings:
        message_code, _, message_text = message.partition(' ')
        if not message_text:
            continue
        message_code = message_code.rstrip(':')
        if not REX_CODE.match(message_code):
            continue
        if code and not message_code.startswith(code):
            continue
        messages[message_code] = message_text
    return messages


def extract_default(name: str) -> Dict[str, str]:
    module = import_module(name)
    content = Path(module.__file__).read_text()
    return get_messages(code='', content=content)
