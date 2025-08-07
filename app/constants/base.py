from enum import Enum
from typing import Any, Optional


class BaseConstant(str, Enum):
    @classmethod
    def to_list(cls) -> list[str]:
        return [item.name for item in cls]  # noqa

    @classmethod
    def to_dict(cls) -> dict[str, str]:
        return {item.name: item.value for item in cls}  # noqa

    @classmethod
    def to_enumerated_choices(cls) -> dict[int, 'BaseConstant']:
        return dict(enumerate(cls, 1))

    @classmethod
    def get(cls, value: Any) -> Optional['BaseConstant']:
        try:
            return cls(value)
        except ValueError:
            return None