from typing import Any
from typing import List
from typing import Mapping
from typing import Optional

import pluggy


class Configuration:
    def __init__(
        self,
        options: Mapping[str, Any],
        plugin_manager: pluggy.PluginManager,
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
        target = self.get_option("target")
        assert isinstance(target, str)
        return target

    @property
    def port_range(self) -> List[int]:
        port_range = self.get_option("port_range")
        assert port_range is not None
        return [int(x) for x in port_range]

    @property
    def quick(self) -> bool:
        quick = self.get_option("quick")
        assert isinstance(quick, bool)
        return quick

    @property
    def random(self) -> bool:
        random = self.get_option("random")
        assert isinstance(random, bool)
        return random

    @property
    def thread_count(self) -> int:
        thread_count = self.get_option("thread_count")
        assert isinstance(thread_count, int)
        return thread_count

    def __repr__(self) -> str:
        return f"Configuration=(options={repr(self.options)}"
