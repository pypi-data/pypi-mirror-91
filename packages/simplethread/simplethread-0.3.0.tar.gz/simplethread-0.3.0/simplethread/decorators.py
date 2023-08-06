# -*- coding: utf-8 -*-

from functools import wraps
from typing import Any, Callable, List, TypeVar, cast

from greenlet import greenlet as _greenlet

from _thread import LockType as _LockType
from _thread import allocate_lock as _allocate
from _thread import start_new_thread as _start

__all__: List[str] = ["asynchronous", "synchronized", "threaded"]

_F = TypeVar("_F", bound=Callable[..., Any])


def asynchronous(user_function: _F) -> _F:
    """
    A decorator to run a ``user_function`` asynchronously.
    """
    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return _greenlet(user_function).switch(*args, **kwargs)

    return cast(_F, wrapper)


def synchronized(user_function: _F) -> _F:
    """
    A decorator to synchronize a ``user_function``.
    """
    mutex: _LockType = _allocate()

    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with mutex:
            return user_function(*args, **kwargs)

    return cast(_F, wrapper)


def threaded(user_function: _F) -> Callable[..., int]:
    """
    A decorator to run a ``user_function`` in a separate thread.
    """
    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return _start(user_function, args, kwargs)

    return wrapper
