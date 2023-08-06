# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import List, Optional, Protocol, runtime_checkable

__all__: List[str] = ["LockType"]


@runtime_checkable
class LockType(Protocol):
    @abstractmethod
    def acquire(self, blocking: bool, timeout: Optional[float]) -> bool:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def release(self) -> None:  # pragma: no cover
        raise NotImplementedError
