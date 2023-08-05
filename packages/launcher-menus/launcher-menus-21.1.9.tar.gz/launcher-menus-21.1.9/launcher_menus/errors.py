#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-
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
classes and functions
'''

from . import MENUS


class MenuError(Exception):
    '''<menu> errors Base'''
    pass


class FlagNameNotFoundError(MenuError):
    '''
    flag not found for <menu>:
    in menu-cfgs/<menu>.yml
    nor provided via kwargs['flags']
    '''
    def __init__(self, command, flag) -> None:
        super(MenuError, self).__init__(
            f'''
            flag name for '{flag}' of {command} was not found
            in supplied 'flags' dictionary or
            in the configuration file {command}.yml
            '''
        )


class CommandError(MenuError):
    '''<Menu> command failed'''

    def __init__(self, args, err) -> None:
        super(CommandError, self).__init__(
            f'''
            Bad menu command {args}:

            {err}

            Menus available:
            {MENUS}
            '''
        )


class UsageError(MenuError):
    '''<Menu> usage failed'''

    def __init__(self, args, err) -> None:
        super(UsageError, self).__init__(
            f'''
            Bad menu usage {args}:

            {err}
            '''
        )
