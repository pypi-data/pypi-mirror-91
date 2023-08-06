import json
import os
from typing import Dict, Callable, Sequence, Union, TypeVar, Generic, Tuple

Exists = bool
JsonSerializable = Union[Dict, Sequence, str, bool, int, float]
JsonSerializableGeneric = TypeVar("JsonSerializableGeneric", bound=JsonSerializable)


class DictJsonRepo(Generic[JsonSerializableGeneric]):
    def __init__(self, directory: str = None) -> None:
        self.directory = directory or os.getcwd()

    def read(self, filename: str) -> JsonSerializableGeneric:
        with open(self._build_path(filename), encoding="utf-8") as f:
            return json.load(f)

    def write(self, data: JsonSerializableGeneric, filename: str) -> JsonSerializableGeneric:
        with open(self._build_path(filename), "w", encoding="utf-8") as f:
            json.dump(data, f)

        return data

    def read_or_write_default(
        self, filename: str, default_factory: Callable[[], JsonSerializableGeneric]
    ) -> Tuple[JsonSerializableGeneric, Exists]:
        if os.path.exists(self._build_path(filename)):
            return self.read(filename), True
        else:
            return self.write(default_factory(), filename), False

    def _build_path(self, filename: str) -> str:
        return os.path.join(self.directory, filename)
