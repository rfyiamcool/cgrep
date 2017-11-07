#!/usr/bin/env python

import sys
import re
import getopt

from termcolor import colored, COLORS
from itertools import starmap


class Colorer:
    def __init__(self, regex, color):
        self.regex = re.compile(regex)
        self.color = color

    def __call__(self, line):
        return self.regex.sub(lambda x: colored(x.group(0), self.color[0], attrs=["reverse", "blink"]), line)


def process(line):
    for colorer in COLORERS:
        line = colorer(line)
    return line


def main():
    if len(sys.argv) == 1:
        sys.stderr.write("Usage: tail -f some.log | %s 'one.*pattern' 'another'\n" % sys.argv[0])
        sys.exit(1)

    if len(sys.argv[1:]) > len(COLORS):
        sys.stderr.write('Num arguments should not be more than %s.\n' % len(COLORS))
        sys.exit(1)

    try:
        for line in sys.stdin.xreadlines():
            sys.stdout.write(process(line))
    except (IOError, KeyboardInterrupt):
        pass


COLORS = sorted([c for c in COLORS.keys() if c not in ('grey', 'white')])
COLORS = zip(COLORS, [[]] * len(COLORS)) + zip(COLORS, [['reverse']] * len(COLORS))
COLORERS = list(starmap(Colorer, zip(sys.argv[1:], COLORS)))
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

    try:
        opts, regex_args = getopt.getopt(sys.argv[1:], "vhi:e:", ["re"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()

        elif opt == "-v":
            is_v = True

        elif opt == "-i":
            is_ignore_upper = True

        elif opt == "-a":
            is_show_all = True


if __name__ == '__main__':
    main()
