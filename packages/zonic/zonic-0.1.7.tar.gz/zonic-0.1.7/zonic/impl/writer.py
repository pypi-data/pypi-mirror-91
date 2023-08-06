from ..abc.base_classes import Writable
from ..utility.string_utils import StringTemplate


class Writer(Writable):
    def write(self, template: StringTemplate, flush: bool = True) -> None:
        print(str(template), flush=True)
