# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

# This file is part of vimiv.
# Copyright 2017-2021 Christian Karl (karlch) <karlch at protonmail dot com>
# License: GNU GPL v3, see the "LICENSE" and "AUTHORS" files for details.

"""Main function and startup utilities for vimiv.

Module Attributes:
    _tmpdir: TemporaryDirectory when running with ``--temp-basedir``. The
        object must exist until vimiv exits.
"""

import argparse
import os
import sys
import tempfile
from typing import List

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from vimiv import app, api, parser, imutils, plugins
from vimiv.commands import runners, search
from vimiv.config import configfile, keyfile, styles
from vimiv.gui import mainwindow
from vimiv.utils import xdg, crash_handler, log, trash_manager, customtypes, migration

# Must be imported to create the commands using the decorators
from vimiv.commands import (  # pylint: disable=unused-import
    misccommands,
    delete_command,
    help_command,
)
from vimiv.config import configcommands  # pylint: disable=unused-import


_tmpdir = None
_logger = log.module_logger(__name__)


def main() -> int:
    """Run startup and the Qt main loop."""
    args = setup_pre_app(sys.argv[1:])
    qapp = app.Application()
    crash_handler.CrashHandler(qapp)
    setup_post_app(args)
    _logger.debug("Startup completed, starting Qt main loop")
    returncode = qapp.exec_()
    plugins.cleanup()
    _logger.debug("Exiting with status %d", returncode)
    return returncode


def setup_pre_app(argv: List[str]) -> argparse.Namespace:
    """Early setup that is done before the QApplication is created.

    Includes parsing the command line and setting up logging as well as initializing the
    components that do not require an application.

    Args:
        argv: sys.argv[1:] from the executable or argv passed by test suite.
    """
    args = parser.get_argparser().parse_args(argv)
    if args.version:
        import vimiv.version

        print(vimiv.version.info(), vimiv.version.paths(), sep="\n\n")
        sys.exit(customtypes.Exit.success)
    migration.run()
    init_directories(args)
    log.setup_logging(args.log_level, *args.debug)
    _logger.debug("Start: vimiv %s", " ".join(argv))
    update_settings(args)
    trash_manager.init()
    return args


def setup_post_app(args: argparse.Namespace) -> None:
    """Setup performed after creating the QApplication."""
    api.working_directory.init()
    imutils.init()
    init_ui(args)
    # Must be done after UI so the search signals are processed after the widgets have
    # been updated
    search.search.connect_signals()
    plugins.load()
    init_paths(args)
    if args.command:
        run_startup_commands(*args.command)


def init_directories(args: argparse.Namespace) -> None:
    """Create vimiv cache, config and data directories.

    The directories are either the directories defined in the freedesktop
    standard or located in a temporary base directory.

    Args:
        args: Arguments returned from parser.parse_args().
    """
    if args.temp_basedir:
        global _tmpdir
        _tmpdir = tempfile.TemporaryDirectory(prefix="vimiv-tempdir-")
        args.basedir = _tmpdir.name
    if args.basedir is not None:
        xdg.basedir = args.basedir
    xdg.makedirs(xdg.vimiv_cache_dir(), xdg.vimiv_config_dir(), xdg.vimiv_data_dir())


def init_paths(args: argparse.Namespace) -> None:
    """Open paths given from commandline or fallback to library if set."""
    _logger.debug("Opening paths")
    try:
        api.open_paths(args.paths)
    except api.commands.CommandError:
        _logger.debug("init_paths: No valid paths retrieved")
        if api.settings.startup_library.value:
            api.open_paths([os.getcwd()])
    api.status.update("startup paths initialized")


def init_ui(args: argparse.Namespace) -> None:
    """Initialize the Qt UI."""
    _logger.debug("Initializing UI")
    mw = mainwindow.MainWindow()
    if args.fullscreen:
        mw.fullscreen()
    # Center on screen and apply size
    screen_geometry = QApplication.desktop().screenGeometry()
    geometry = (
        args.geometry
        if args.geometry
        else QSize(screen_geometry.width() // 2, screen_geometry.height() // 2)
    )
    x = screen_geometry.x() + (screen_geometry.width() - geometry.width()) // 2
    y = screen_geometry.y() + (screen_geometry.height() - geometry.height()) // 2
    mw.setGeometry(x, y, geometry.width(), geometry.height())
    mw.show()
    migration.run_welcome_popup(parent=mw)


def update_settings(args: argparse.Namespace) -> None:
    """Update default settings with command line arguments and configfiles.

    Args:
        args: Arguments returned from parser.parse_args().
    """
    configfile.parse(args.config)
    for option, value in args.cmd_settings:
        try:
            setting = api.settings.get(option)
            setting.value = value
        except KeyError:
            log.error("Unknown setting %s", option)
        except ValueError as e:
            log.error(str(e))
    keyfile.parse(args.keyfile)
    styles.parse()


def run_startup_commands(*commands: str) -> None:
    """Run commands given via --command at startup.

    Args:
        commands: All command strings given via individual --command arguments.
    """
    total = len(commands)
    for i, command in enumerate(commands, start=1):
        _logger.debug("Startup commands: running %d/%d '%s'", i, total, command)
        if "quit" in command:  # This does not work without a running app
            log.warning("Quitting forcefully as the app does not exist")
            app.Application.preexit(customtypes.Exit.success)
            sys.exit(customtypes.Exit.success)
        else:
            runners.run(command, mode=api.modes.current())
