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
import pathlib
import subprocess
import yaml
from . import MENUS
from .errors import FlagNameNotFoundError, CommandError, UsageError


def process_comm(cmd: list, pipe_inputs: str = '',
                 timeout: float = None, **kwargs) -> str:
    '''
    Args:
        cmd: list form of commands to be passed to Popen as args
        pipe_inputs: inputs to be passed as stdin
        timeout: timeout of communication in seconds
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
        raise CommandError(cmd, err) from err

    stdout, stderr = proc.communicate(input=pipe_inputs, timeout=timeout)
    if stderr:
        if re.match('usage', stderr, re.I):
            raise UsageError(cmd, stderr)
        raise CommandError(cmd, stderr)
    return stdout.rstrip('\n')


def menu(opts: typing.List[str] = None, command: str = list(MENUS.keys())[0],
         config_yml: str = None, **flags: str) -> str:
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
        index: select index automatically (bemenu)
        prompt: prompt string of menu
        prefix: prefix added highlighted item (bemenu)
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
    bool_kwargs: typing.Dict[str, bool] = {
        'bottom': None,
        'grab': None,
        'ignorecase': None,
        'wrap': None,
        'ifne': None,
        'nooverlap': None,
    }

    input_kwargs: typing.Dict[str, str] = {
        'lines': None,
        'monitor': None,  # may be str, doesn't harm
        'height': None,
        'index': None,
        'prompt': None,
        'prefix': None,
        'scrollbar': None,
        'font': None,
        'title_background': None,
        'title_foreground': None,
        'normal_background': None,
        'normal_foreground': None,
        'filter_background': None,
        'filter_foreground': None,
        'high_background': None,
        'high_foreground': None,
        'scroll_background': None,
        'scroll_foreground': None,
        'selected_background': None,
        'selected_foreground': None,
        'windowid': None,
    }

    # parse bool_kwargs
    for key in {**bool_kwargs, **input_kwargs}:
        if key in flags:
            bool_kwargs[key] = flags[key]
            del flags[key]

    flag_name = MENUS.get(command) or {}

    if config_yml is not None and pathlib.Path(config_yml).exists():
        with open(config_yml, 'r') as yml_handle:
            flag_name.update(yaml.safe_load(yml_handle))
            # NEXT: in python3.9, the following
            # flag_name |= yaml.safe_load(yml_handle)

    flag_name.update(flags)
    # NEXT: in python3.9, the following
    # flag_name |= flags

    if not flag_name:
        raise FlagNameNotFoundError(command, 'any flag')

    cmd = [command]

    try:
        for key, value in bool_kwargs.items():
            if value is not None:
                cmd.append(flag_name[key])

        for key, value in input_kwargs.items():
            if value is not None:
                if key == 'scrollbar' and value not in ['none',
                                                        'always', 'autohide']:
                    raise ValueError(
                        f"""
                        scrollbar should be in ['none', 'always', 'autohide'],
                        got {value}
                        """
                    )
                cmd.extend((flag_name[key], str(value)))

    except KeyError as err:
        raise FlagNameNotFoundError(command, err.args[0]) from err

    if opts is None:
        opts = []
    return process_comm(cmd, pipe_inputs='\n'.join(opts)) or None
