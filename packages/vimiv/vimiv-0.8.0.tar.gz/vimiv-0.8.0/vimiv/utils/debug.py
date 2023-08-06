# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

# This file is part of vimiv.
# Copyright 2017-2021 Christian Karl (karlch) <karlch at protonmail dot com>
# License: GNU GPL v3, see the "LICENSE" and "AUTHORS" files for details.

"""Various utility functions for debugging and profiling."""

import contextlib
import cProfile
import functools
import pstats
import time
from typing import Any, Iterator

from vimiv.utils.customtypes import FuncT


def timed(function: FuncT) -> FuncT:
    """Decorator to time a function and log evaluation time."""

    @functools.wraps(function)
    def inner(*args: Any, **kwargs: Any) -> Any:
        """Wrap decorated function and add timing."""
        start = time.time()
        return_value = function(*args, **kwargs)
        elapsed_in_ms = (time.time() - start) * 1000
        print(f"{function.__qualname__}: took {elapsed_in_ms:.3f} ms")
        return return_value

    # Mypy seems to disapprove the *args, **kwargs, but we just wrap the function
    return inner  # type: ignore


@contextlib.contextmanager
def profile(amount: int = 15) -> Iterator[None]:
    """Contextmanager to profile code sections.

    Starts a cProfile.Profile upon entry, disables it on exit and prints profiling
    information.

    Usage:
        with profile(amount=10):
            # your code to profile here
            ...
        # This is no longer profiled

    Args:
        amount: Number of lines to restrict the output to.
    """
    cprofile = cProfile.Profile()
    cprofile.enable()
    yield
    cprofile.disable()
    stats = pstats.Stats(cprofile)
    stats.sort_stats("cumulative").print_stats(amount)
    stats.sort_stats("time").print_stats(amount)
