# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

# This file is part of vimiv.
# Copyright 2017-2021 Christian Karl (karlch) <karlch at protonmail dot com>
# License: GNU GPL v3, see the "LICENSE" and "AUTHORS" files for details.

"""`Utilities related to logging`.

There are two different types of loggers: the application-wide logger and module
specific loggers.

The application-wide logger is used for general messages meant for the user. All log
messages with level larger than debug are also sent to the statusbar. To send a message
to this logger, the utility functions :func:`debug`, :func:`info`, :func:`warning`,
:func:`error` and :func:`critical` can be used. They are just very thin wrapper
functions around the python logging functions.

For debugging it is recommended to use a module specific logger. This allows fine-tuning
the amount of debug statements that should be displayed using the ``--debug`` flag. To
create a module logger::

    from vimiv.utils import log

    _logger = log.module_logger(__name__)

and use this logger as usual::

    _logger.debug("Performing some setup")
    ...
    _logger.debug("Doing the work")
    ...
    _logger.debug("Performing some clean-up")

Three log handlers are currently used:

* One to print to the console
* One to save the output in a log file located in
  ``$XDG_DATA_HOME/vimiv/vimiv.log``
* One to print log messages to the statusbar (only for application-wide logger)

In case you want to ensure that a log message is only logged a single time, pass
``once=True`` to your log statement::

    _logger.debug("Something happened, and may now happen very often", once=True)
"""

import logging
from typing import Dict, List, Optional, Any, Set

from PyQt5.QtCore import pyqtSignal, QObject

import vimiv

from vimiv.utils import xdg


_module_loggers: Dict[str, "LazyLogger"] = {}
formatter = logging.Formatter(
    "[{asctime}] {levelname:8} {name:20} {message}", datefmt="%H:%M:%S", style="{"
)
_debug_loggers: List[str] = []


def debug(msg: str, *args: Any, **kwargs: Any) -> None:
    log(logging.DEBUG, msg, *args, **kwargs)


def info(msg: str, *args: Any, **kwargs: Any) -> None:
    log(logging.INFO, msg, *args, **kwargs)


def warning(msg: str, *args: Any, **kwargs: Any) -> None:
    log(logging.WARNING, msg, *args, **kwargs)


def error(msg: str, *args: Any, **kwargs: Any) -> None:
    log(logging.ERROR, msg, *args, **kwargs)


def critical(msg: str, *args: Any, **kwargs: Any) -> None:
    log(logging.CRITICAL, msg, *args, **kwargs)


fatal = critical


def setup_logging(level: int, *debug_modules: str) -> None:
    """Configure and set up logging.

    There are two types of loggers: the application-wide logger accessible through the
    convenience functions and the module-level loggers. Both loggers write to stderr and
    $XDG_DATA_HOME/vimiv/vimiv.log. The application-wide logger sends messages with a
    level higher than debug to the statusbar in addition.

    No logging should be performed in this function as the logging header comes directly
    after it.

    Args:
        level: Integer log level set for the console handler.
        debug_modules: Module names for which debug messages are forced to be shown.
    """
    # Enable logging at debug level in general
    logging.getLogger().setLevel(logging.DEBUG)
    # Configure handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # mode=w creates a new file for every new vimiv process
    file_handler = logging.FileHandler(xdg.vimiv_data_dir("vimiv.log"), mode="w")
    file_handler.setFormatter(formatter)
    # Configure app logger
    _app_logger.level = level
    _app_logger.handlers = [file_handler, console_handler, statusbar_loghandler]
    LazyLogger.handlers = [console_handler, file_handler]
    # Setup debug logging for specific module loggers
    _debug_loggers.extend(debug_modules)
    for name, logger in _module_loggers.items():
        logger.level = logging.DEBUG if name in debug_modules else level


def module_logger(name: str) -> "LazyLogger":
    """Create a module-level logger.

    Module-level loggers log to the vimiv log-file as well as the console. The file
    handler is only attached in setup_logging to ensure logging to the correct file,
    even when starting with --temp-basedir.

    Args:
        name: Name of the module for which the logger is created.
    Returns:
        The created logger object.
    """
    name = name.replace("vimiv.", "")
    level = logging.DEBUG if name in _debug_loggers else _app_logger.level
    logger = LazyLogger(name, level=level)
    _module_loggers[name] = logger
    return logger


class LazyLogger:
    """Logger class with lazy initialization of the logger object.

    The class supports logging using a underlying logging.Logger object and provides the
    regular, log, debug, ... functions. The object itself however is only created on an
    is-needed basis.
    """

    handlers: List[logging.Handler] = []

    def __init__(self, name: str, level: int = logging.WARNING):
        self.level = level
        self._logger: Optional[logging.Logger] = None
        self._name = name
        self._stored_messages: Set[str] = set()

    def log(
        self, level: int, msg: str, *args: Any, once: bool = False, **kwargs: Any
    ) -> None:
        """Log a message creating the logger instance if needed."""
        if level < self.level:
            return
        if self._logger is None:
            self._logger = logging.getLogger(f"<{self._name}>")
            self._logger.propagate = False
            self._logger.handlers = self.handlers
        if once:
            if msg in self._stored_messages:
                return
            self._stored_messages.add(msg)
        self._logger.log(level, msg, *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.CRITICAL, msg, *args, **kwargs)

    fatal = critical


class StatusbarLogHandler(QObject, logging.NullHandler):
    """Loghandler to display log messages in the statusbar.

    Only emits a signal on handle which the statusbar connects to.

    Signals:
        message: Emitted with severity and message on log message.
    """

    message = pyqtSignal(str, str)

    def handle(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.INFO:  # Debug in the statusbar makes no sense
            self.message.emit(record.levelname.lower(), record.message)


_app_logger = LazyLogger(f"{vimiv.__name__}")
log = _app_logger.log
statusbar_loghandler = StatusbarLogHandler()
