# flake8-codes

CLI tool to introspect flake8 plugins and their codes.

**Input**: plugin name (`pycodestyle`), error code (`W605`), or code prefix (`W6`).

**Output**: plugin name, error code, error message.

Only plugins installed in the same environment are inspected.

## Installation

```bash
python3 -m pip install -U --user flake8-codes
```

## Example

```bash
$ python3 -m flake8_codes W6
pycodestyle          | W601     | .has_key() is deprecated, use 'in'
pycodestyle          | W602     | deprecated form of raising exception
pycodestyle          | W603     | '<>' is deprecated, use '!='
pycodestyle          | W604     | backticks are deprecated, use 'repr()'
pycodestyle          | W605     | invalid escape sequence '\%s'
pycodestyle          | W606     | 'async' and 'await' are reserved keywords starting with Python 3.7
```
