# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
from .subcmds import all_commands
import optparse
import sys
import os
from .tools import *

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

__version__ = "2.0.16"

global_options = optparse.OptionParser(
    usage="thead COMMAND [ARGS]"
)


class YocCommand:
    def __init__(self):
        self.commands = all_commands
        self.commands['help'] = all_commands['help']

    def _ParseArgs(self, argv):
        """Parse the main `thead` command line options."""
        name = None
        glob = []

        for i in range(len(argv)):
            if not argv[i].startswith('-'):
                name = argv[i]
                if i > 0:
                    glob = argv[:i]
                argv = argv[i + 1:]
                break
        if not name:
            glob = argv
            name = 'help'
            argv = []
        gopts, _gargs = global_options.parse_args(glob)
        return (name, gopts, argv)

    def _Run(self, name, gopts, argv):
        result = 0
        try:
            cmd = self.commands[name]

        except KeyError:
            put_string("thead: '%s' is not a thead command.  See 'thead help'." %
                       name, file=sys.stderr)
            return 1

        try:
            copts, cargs = cmd.OptionParser.parse_args(argv)
            copts = cmd.ReadEnvironmentOptions(copts)
        except Exception as e:
            put_string('error: in `%s`: %s' % (' '.join([name] + argv), str(e)),
                       file=sys.stderr)
            put_string('error: manifest missing or unreadable -- please run init',
                       file=sys.stderr)
            return 1
        try:
            cmd.ValidateOptions(copts, cargs)
            result = cmd.Execute(copts, cargs)
        except Exception as e:
            put_string("YocCommand error:", e)
            pass
        return result

    def Execute(self, argv):
        name, gopts, argv = self._ParseArgs(argv)

        self._Run(name, gopts, argv)


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '-V' or sys.argv[1] == '--version':
            put_string(__version__)
            return
    cmd = YocCommand()
    cmd.Execute(sys.argv[1:])

def cct_main():
    try:
        cmd = all_commands['cct']
        parser = cmd.OptionParser
        parser.set_usage(cmd.helpUsage.strip().replace('%prog', cmd.NAME))
        copts, cargs = parser.parse_args(sys.argv[1:])
        copts = cmd.ReadEnvironmentOptions(copts)
    except Exception as e:
        put_string('error: manifest missing or unreadable -- please run init',
                    file=sys.stderr)
        return 1
    try:
        cmd.ValidateOptions(copts, cargs)
        cmd.Execute(copts, cargs)
    except Exception as e:
        put_string("AosCommand error:", e)
        pass
