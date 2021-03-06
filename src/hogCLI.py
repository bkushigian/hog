#!/usr/bin/python3
import code
from os import getcwd
from sys import argv, exit

from snapshots import GitDirLog

welcome_msg = '+' + ('-=' * 39) + '+' + """
| Hello, and welcome to hog, the higher order Git program. Basically, just feed
| me a .git directory and tell me when to take a snapshot (by entering `snap()`
| into the REPL below) and I'll tell you what's happened to the .git directory.
| 
| Yup, that's about it. Enjoy!
| 
| Oh! One other thing... If you call me _from_ a .git directory you don't need
| to give me any arguments, I'll just figure it out. Also, if you call me on a
| non .git directory and call snap() I may try to read and track your entire
| hard drive. So don't do that. That would be dumb.
|
| ...Now that I'm thinking about it, this might be a bug...
|
| Anyways, you've been WARNED!
|
| Oh, and one last thing. You have a full fledged Python REPL below, which
| means you can do whatever you want. Feel free to explore by looking at
| the code and checking things out. Alright, bye for now...
""" + '+' + ('-=' * 39) + '+' '\n'

help_msg = ('-=' * 40) + """
                                   Help Menu
snap(msg='', verbose=True): Take a snapshot of the .git repository. You can add
        an optional message or set verbose=False to supress printing to stdout.
        This second option is particularly useful if you are taking a snapshot
        of a large repository.

print_diffs(start=0, end=-1): Print the difference objects that you've tracked
        so far. You can choose to start on the nth difference object by setting 
        start=n, and likewise cut off our printing by choosing end=m. In
        particular, you can enter print_diffs(start=-3,end=-1) to print the last
        two items, print_diffs(start=5, end=7) to print items 5 and 6, etc.

helpme(): Print this help screen.
""" + ('-=' * 40)


def usage():
    """ Usage:
        hog [<git-directory>]

        If no directory is provided, track the directory that you are currently
        in. Otherwise, track the directory provided as an argument.
    """


def main():
    print(welcome_msg)
    gitdir = getcwd()
    if len(argv) == 2:
        gitdir = argv[1]
    elif len(argv) > 2:
        usage()
        exit(1)
    print("Inspecting directory " + gitdir)

    log = GitDirLog(gitdir)
    repl(log)


def repl(log):
    def snap(m='', verbose=True):
        log.take_snapshot(m, verbose)

    def print_diffs(start=0, end=-1):
        log.print_diffs(start, end)

    def helpme():
        print(help_msg)

    global_vars = globals().copy()
    global_vars.update(locals())
    shell = code.InteractiveConsole(global_vars)
    shell.interact()


if __name__ == '__main__':
    main()
