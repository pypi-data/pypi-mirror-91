"""Top-level package for zonic."""

__author__ = """Simon Kerr"""
__email__ = "jackofspaces@gmail.com"
__version__ = "0.1.0"

import colorama
import pluggy

from .configuration import Configuration
from .hooks import hookspec

# TODO: consider moving this out of init.py; is it bad practice?
colorama.init()
plugin_manager = pluggy.PluginManager("zonic")
plugin_manager.add_hookspecs(hookspec)

zonic_hookspec = hookspec.zonic_hookspec
zonic_hookimpl = hookspec.zonic_hookimpl

__all__ = [
    "Configuration",
    "plugin_manager",
    "hookspec",
    "zonic_hookimpl",
    "zonic_hookspec",
]
