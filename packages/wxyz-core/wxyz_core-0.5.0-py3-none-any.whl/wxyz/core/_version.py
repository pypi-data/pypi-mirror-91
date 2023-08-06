""" some constants
"""
# pylint: disable=invalid-name
import json
from pathlib import Path

HERE = Path(__file__).parent
__jspackage__ = json.loads((HERE / "js/package.json").read_text(encoding="utf-8"))
__version__ = __jspackage__["version"]
module_name = __jspackage__["name"]
module_version = f"""^{__jspackage__["version"]}"""
