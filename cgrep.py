#!/usr/bin/env python

import sys
import re
import getopt

from itertools import starmap
from termcolor import colored, COLORS


class ReplaceColor:
    def __init__(self, regex, color):
        self.regex = re.compile(regex)
        self.color = color

    def __call__(self, line):
        if not line:
            return False, None

        res = self.regex.search(line)
        if not res:
            return False, None

        return True, self.regex.sub(colored(res.group(0), self.color[0], attrs=["reverse", "bold"]), line)


def process(line):
    m = False
    cline = line
    for colorer_call in colorers:
        status, cline = colorer_call(cline)
        if status:
            m = status

    if is_show_all and not m:
        return line

    if is_show_all and m:
        return cline

    if not is_show_all and not m:
        return None

    if not is_show_all and m:
        return cline

    return line


COLORS = sorted([c for c in COLORS.keys() if c not in ('grey', 'white')])
COLORS = zip(COLORS, [[]] * len(COLORS)) + zip(COLORS, [['reverse']] * len(COLORS))
colorers = None
is_show_all = False
is_v = False
regex_args = ""
is_ignore_upper = False


def usage():
    print("Usage:%s [-v|-i|-a|-h] args...."%sys.argv[0])


def parse_cmd():
    global is_show_all
    global is_v
    global regex_args
    global is_ignore_upper
    global colorers

    try:
        opts, regex_args = getopt.getopt(sys.argv[1:], "avhi:e:", ["re"])
        colorers = list(starmap(ReplaceColor, zip(regex_args, COLORS)))

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(2)

        elif opt == "-v":
            is_v = True

        elif opt == "-i":
            is_ignore_upper = True

        elif opt == "-a":
            is_show_all = True


def main():
    parse_cmd()
    if len(sys.argv) == 1:
        sys.stderr.write("Usage: tail -f debug.log | %s 'one.*pattern' 'another'\n" % sys.argv[0])
        sys.exit(1)

    if len(sys.argv[1:]) > len(COLORS):
        sys.stderr.write('Num arguments should not be more than %s.\n' % len(COLORS))
        sys.exit(1)

    try:
        for line in sys.stdin.xreadlines():
            cline = process(line)
            if cline:
                sys.stdout.write(cline)
    except (IOError, KeyboardInterrupt):
        pass


if __name__ == '__main__':
    main()
