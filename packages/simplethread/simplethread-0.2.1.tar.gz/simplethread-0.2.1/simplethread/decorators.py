# -*- coding: utf-8 -*-

from concurrent.futures import Future
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from simplethread.thread import mutex
from simplethread.thread import start

__all__ = ("synchronized", "threaded")

_F = TypeVar("_F", bound=Callable[..., Any])
_T = TypeVar("_T")


def synchronized(user_function: _F) -> _F:
    """
    A decorator to synchronize a ``user_function``.
    """
    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with mutex:
            return user_function(*args, **kwargs)

    return cast(_F, wrapper)


def threaded(user_function: Callable[..., _T]) -> Callable[..., "Future[_T]"]:
    """
    A decorator to run a ``user_function`` in a separate thread.
    """
    # Let the bodies hit the floor..
    future: "Future[_T]" = Future()

    @synchronized
    def callback(*args: Any, **kwargs: Any) -> None:
        nonlocal future
        future.set_running_or_notify_cancel()

        try:
            # Let the bodies hit the floor..
            result: _T = user_function(*args, **kwargs)

        except BaseException as exception:
            # Let the bodies hit the floor..
            future.set_exception(exception)

        else:
            # Let the bodies hit the floor..
            future.set_result(result)

    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> "Future[_T]":
        start(callback, args, kwargs)
        return future

    return wrapper
