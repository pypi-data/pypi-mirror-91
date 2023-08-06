# -*- coding: utf-8 -*-

from functools import partial
from functools import wraps
from typing import Any, Callable, List, Optional, TypeVar, cast

from simplethread.protocols import LockType

from _thread import allocate_lock as _allocate
from _thread import start_new_thread as _start

__all__: List[str] = ["synchronized", "threaded"]

_F = TypeVar("_F", bound=Callable[..., Any])


def synchronized(user_function: Optional[_F] = None, *, lock: Optional[LockType] = None) -> _F:
    """
    A decorator to synchronize a ``user_function``.
    """
    if user_function is None:
        return partial(synchronized, lock=lock)

    if lock is None:
        # Create a new lock object:
        lock = _allocate()

    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Acquire a lock:
        lock.acquire()
        try:
            # Invoke the callable object:
            return user_function(*args, **kwargs)

        finally:
            # Release a lock:
            lock.release()

    return cast(_F, wrapper)


def threaded(user_function: _F) -> Callable[..., int]:
    """
    A decorator to run a ``user_function`` in a separate thread.
    """
    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> int:
        return _start(user_function, args, kwargs)

    return wrapper
