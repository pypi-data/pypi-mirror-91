from typing import Any
from typing import Iterable
from typing import Mapping
from typing import Optional

import pluggy


class Configuration:
    def __init__(
        self, options: Mapping[Any, Any], plugin_manager: pluggy.PluginManager
    ) -> None:
        self.options = options
        self.plugin_manager = plugin_manager

    def get_option(self, option: str) -> Optional[Any]:
        """
        Fetches a command line option from the config.
        Config options need to be dynamic because arbitrary third party plugins can add their own options
        """
        return self.options.get(option)

    @property
    def target(self) -> str:
        return self.get_option("target")

    @property
    def port_range(self) -> Iterable[int]:
        return self.get_option("port_range")

    @property
    def quick(self) -> bool:
        return self.get_option("quick")

    @property
    def random(self) -> bool:
        return self.get_option("random")

    @property
    def thread_count(self) -> int:
        return self.get_option("thread_count")

    def __repr__(self) -> str:
        return f"Configuration=(options={repr(self.options)}"
