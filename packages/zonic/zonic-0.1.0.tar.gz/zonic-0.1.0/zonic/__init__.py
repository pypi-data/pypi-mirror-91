"""Top-level package for sonic."""

__author__ = """Simon Kerr"""
__email__ = "jackofspaces@gmail.com"
__version__ = "0.1.0"

import colorama
import pluggy

from .configuration import Configuration
from .hooks import hookspec

# TODO: consider moving this out of init.py; is it bad practice?
colorama.init()
plugin_manager = pluggy.PluginManager("sonic")
plugin_manager.add_hookspecs(hookspec)

sonic_hookspec = hookspec.sonic_hookspec
sonic_hookimpl = hookspec.sonic_hookimpl

__all__ = [
    "Configuration",
    "plugin_manager",
    "hookspec",
    "sonic_hookimpl",
    "sonic_hookspec",
]
