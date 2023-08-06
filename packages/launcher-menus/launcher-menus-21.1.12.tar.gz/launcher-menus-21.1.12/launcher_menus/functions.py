#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-
#
# Copyright 2021 Pradyumna Paranjape
# This file is part of launcher-menus.
#
# launcher-menus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# launcher-menus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with launcher-menus.  If not, see <https://www.gnu.org/licenses/>.
#

'''
menu function
'''

import re
import typing
import yaml
import subprocess
import pathlib
from . import MENUS
from .errors import FlagNameNotFoundError, CommandError, UsageError


def process_comm(cmd: list, pipe_inputs: str = '',
                 timeout: float = None, **kwargs) -> str:
    '''
    Args:
        cmd: list = list form of commands to be passed to Popen as args
        pipe_inputs: str = inputs to be passed as stdin
        timeout: floa: timeout of communication in seconds
        **kwargs: passed to Popen

    Raises:
        UsageError: Command usage error
        CommandError: can't open process/ stderr from process

    Return
        stdout: str: returned by process
    '''
    try:
        proc = subprocess.Popen(
            cmd,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            **kwargs
            )
    except OSError as err:
        raise CommandError(cmd, err)

    stdout, stderr = proc.communicate(input=pipe_inputs)
    if stderr:
        if re.match('usage', stderr, re.I):
            raise UsageError(cmd, stderr)
        raise CommandError(cmd, stderr)
    return stdout.rstrip('\n')


def menu(
        opts: typing.List[str] = [],
        command: str = list(MENUS.keys())[0],
        bottom: bool = False,
        grab: bool = False,
        ignorecase: bool = False,
        wrap: bool = False,
        ifne: bool = False,
        nooverlap: bool = False,
        lines: int = None,
        monitor: typing.Union[str, int] = None,
        height: int = None,
        prompt: str = None,
        prefix: str = None,
        index: int = None,
        scrollbar: str = None,
        font: str = None,
        title_background: str = None,
        title_foreground: str = None,
        normal_background: str = None,
        normal_foreground: str = None,
        filter_background: str = None,
        filter_foreground: str = None,
        high_background: str = None,
        high_foreground: str = None,
        scroll_background: str = None,
        scroll_foreground: str = None,
        selected_background: str = None,
        selected_foreground: str = None,
        windowid: str = None,
        config_yml: str = None,
        **flags: str,
) -> str:
    '''
    Call <command> menu to collect interactive information.

    Args:
        opts: options to be offerred by menu.
        command: command to use [dmenu, bemenu, <other>]
        bottom: show bar at bottom
        grab: show menu before reading stdin (faster)
        ignorecase: match items ignoring case
        wrap: wrap cursor selection (only for bemenu)
        ifne: display only if opts (bemenu)
        nooverlap: do not overlap panels (bemenu w/ wayland)
        lines: list opts on vertical 'lines'
        monitor: show menu on (bemenu w/ wayland: -1: all)
        height: height of each menu line (bemenu)
        prompt: prompt string of menu
        prefix: prefix added highlighted item (bemenu)
        index: select index automatically (bemenu)
        scrollbar: display scrollbar [none, always, autohide] (bemenu)
        font: font to be used format: "FONT-NAME [SIZE (bemenu)]"
        title_background: #RRGGBB title background color (bemenu)
        title_foreground:  #RRGGBB title foreground color (bemenu)
        normal_background: #RRGGBB normal background color
        normal_foreground: #RRGGBB normal foreground color
        filter_background: #RRGGBB filter background color (bemenu)
        filter_foreground: #RRGGBB filter foreground color (bemenu)
        high_background: #RRGGBB highlight background color (bemenu)
        high_foreground: #RRGGBB highlight foreground color (bemenu)
        scroll_background: #RRGGBB scrollbar background color (bemenu)
        scroll_foreground: #RRGGBB scrollbar foreground color (bemenu)
        selected_background: #RRGGBB selected background color
        selected_foreground: #RRGGBB selected foreground color
        windowid: embed into windowid (dmenu)
        config_yml: path of yaml config file. Extends and overrides default.
        **flags: flagname='--flag' for <command>. Overrides config files.

    Raises:
        CommandError
        UsageError
        FlagNameNotFoundError
        ValueError: bad scrollbar options

    Returns:
        User's selected or overridden-entered opt else None [Esc]

    '''
    flag_name = MENUS.get(command) or {}

    if config_yml is not None and pathlib.Path(config_yml).exists():
        with open(config_yml, 'r') as yml_handle:
            flag_name |= yaml.safe_load(yml_handle)

    flag_name |= flags

    if not flag_name:
        raise FlagNameNotFoundError(command, 'any flag')

    cmd = [command]

    try:
        if bottom:
            cmd.append(flag_name['bottom'])

        if grab:
            cmd.append(flag_name['grab'])

        if ignorecase:
            cmd.append(flag_name['ignorecase'])

        # bemenu
        if wrap:
            cmd.append(flag_name['wrap'])

        if ifne:
            cmd.append(flag_name['ifne'])

        if nooverlap:
            cmd.append(flag_name['nooverlap'])

        if lines is not None:
            cmd.extend((flag_name['lines'], str(lines)))

        if monitor is not None:
            cmd.extend((flag_name['monitor'], str(monitor)))

        if height is not None:
            cmd.extend((flag_name['height'], str(height)))

        if prompt is not None:
            cmd.extend((flag_name['prompt'], prompt))

        # bemenu
        if prefix is not None:
            cmd.extend((flag_name['prefix'], prefix))

        if index is not None:
            cmd.extend((flag_name['index'], index))

        if scrollbar is not None:
            if scrollbar not in ['none', 'always', 'autohide']:
                raise ValueError(
                    f"""
                    scrollbar should be in ['none', 'always', 'autohide'],
                    got {scrollbar}
                    """
                )
            cmd.extend((flag_name['scrollbar'], scrollbar))

        if font is not None:
            cmd.extend((flag_name['font'], font))

        if title_background is not None:
            cmd.extend((flag_name['title background'], title_background))

        if title_foreground is not None:
            cmd.extend((flag_name['title foreground'], title_foreground))

        if normal_background is not None:
            cmd.extend((flag_name['normal background'], normal_background))

        if normal_foreground is not None:
            cmd.extend((flag_name['normal foreground'], normal_foreground))

        if filter_background is not None:
            cmd.extend((flag_name['filter background'], filter_background))

        if filter_foreground is not None:
            cmd.extend((flag_name['filter foreground'], filter_foreground))

        if high_background is not None:
            cmd.extend((flag_name['high background'], high_background))

        if high_foreground is not None:
            cmd.extend((flag_name['high foreground'], high_foreground))

        if scroll_background is not None:
            cmd.extend((flag_name['scroll background'], scroll_background))

        if scroll_foreground is not None:
            cmd.extend((flag_name['scroll foreground'], scroll_foreground))

        if selected_background is not None:
            cmd.extend((flag_name['selected background'], selected_background))

        if selected_foreground is not None:
            cmd.extend((flag_name['selected foreground'], selected_foreground))

        # dmenu
        if windowid is not None:
            cmd.extend((flag_name['windowid'], str(windowid)))

    except KeyError as err:
        raise FlagNameNotFoundError(command, err.args[0])

    return process_comm(cmd, pipe_inputs='\n'.join(opts)) or None
