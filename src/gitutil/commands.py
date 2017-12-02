from os.path import join
import os
import sys

class Command:
    """
    A FileSystemAction represents an action on a file or a directory. This is
    a mixin that specifies that an action can be executed via method execute,
    which is parametrized by a file name.
    """
    def execute(self, file):
        raise NotImplementedError()


class Add(Command):
    """ Represents a call to GitAdd """
    args = 2

    def __init__(self, session, files=None):
        """
        :param files: list of files to add
        """
        self.session = session
        self.files = files

    def execute(self):
        """
        Execute git add files on a running session
        :return:
        """
        return self.session.git.add(self.files)


class Commit(Command):
    args = 2

    def __init__(self, session, message=None):
        self.session = session
        self.message = message
        if message is None:
            self.message = ""

    def execute(self):
        return self.session.repo().index.commit(self.message)


class CreateFile(Command):
    """
    Create a new file
    """
    args = 2

    def __init__(self, session, filepath):
        self.session = session
        self.path = filepath

    def execute(self):
        p = join(self.session.dir(), self.path)
        open(p, 'w').close()         # XXX: This works on Ubuntu :)


class CreateDirectory(Command):
    """
    Create a new file
    """
    args = 2

    def __init__(self, session, dirpath):
        self.session = session
        self.path = dirpath

    def execute(self):
        d = join(self.session.dir(), self.path)
        return os.makedirs(d)


class AppendLineToFile(Command):
    """
    Append line to file
    """
    args = 3

    def __init__(self, session, file, line):
        self.session = session
        self.file = file
        self.line = line

    def execute(self):
        f = open(join(self.session.dir(), self.file), 'a')
        f.write(self.line)
        f.close()


class AppendLinesToFile(Command):
    """
    Append lines to file
    """
    args = 3

    def __init__(self, session, file, lines):
        self.session = session
        self.file = file
        self.lines = lines

    def execute(self):
        file = join(self.session.dir(), self.file)
        f = open(file, 'a')
        f.write('\n'.join(self.lines))
        f.close()


class AppendStringToLine(Command):
    """
    Append a string to a particular line.
    """
    args = 4

    def __init__(self, session, file, line, string):
        self.session = session
        self.file = file
        self.line = line
        self.string = string

    def execute(self):
        file = join(self.session.dir(), self.file)
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        lines[self.line] = lines[self.line][:-1] + self.string + '\n'
        f = open(file, 'w')
        f.write(''.join(lines))
        f.close()


class InsertLineAfterLine(Command):  # NOTE: Untested
    args = 4

    def __init__(self, session, file, line, lineno):
        self.session = session
        self.file = file
        self.lineno = lineno
        self.line = line

    def execute(self):
        file = join(self.session.dir(), self.file)
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        lines = lines[:self.lineno] + [self.line] + lines[self.lineno:]
        f = open(file, 'w')
        f.write('\n'.join(lines))
        f.close()


class InsertLinesAfterLine(Command):  # NOTE: Untested
    args = 4

    def __init__(self, session, file, lines, lineno):
        self.session = session
        self.file = file
        self.lineno = lineno
        self.lines = lines

    def execute(self):
        file = join(self.session.dir(), self.file)
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        lines = lines[:self.line] + self.lines + lines[self.line:]
        f = open(file, 'w')
        f.write('\n'.join(lines))
        f.close()


class DeleteLine(Command):  # NOTE: Untested
    args = 3

    def __init__(self, session, file, line):
        self.session = session
        self.file = file
        self.line = line

    def execute(self):
        file = join(self.session.dir(), self.file)
        f = open(file, 'r')
        lines = f.read()
        f.close()

        lines = lines[:self.line] + lines[self.line + 1:]
        f = open(file, 'w')
        f.write('\n'.join(lines))
        f.close()


class ReadFile(Command):
    args = 2

    def __init__(self, session, file):
        self.session = session
        self.file = file

    def execute(self):
        file = join(self.session.dir(), self.file)
        with open(file) as f:
            contents = f.read()
        return contents


class ReadFileLines(Command):
    args = 2

    def __init__(self, session, file):
        self.session = session
        self.file = file

    def execute(self):
        file = join(self.session.dir(), self.file)
        with open(file) as f:
            lines = f.readlines()
        return lines


class CommandParser:
    consDict = {
        'add'                   : Add,
        'commit'                : Commit,
        'createfile'            : CreateFile,
        'createdirectory'       : CreateDirectory,
        'appendlinetofile'      : AppendLineToFile,
        'appendlinestofile'     : AppendLinesToFile,
        'appendstringtoline'    : AppendStringToLine,
        'insertlineafterline'   : InsertLineAfterLine,
        'insertlinesafterline'  : InsertLinesAfterLine,
        'deleteline'            : DeleteLine,
        'readfile'              : ReadFile,
        'readfilelines'         : ReadFileLines,
    }

    def __init__(self, session):
        self.session = session

    def parse_file(self, file):
        with open(file) as f:
            contents = f.read()
        return self.parse_string(contents)

    def parse_string(self, s):
        lines = s.split('\n')
        result = []
        for i, line in enumerate(lines):
            l = line.strip()
            if not l or l.startswith('#'):
                continue
            items = l.split(' ')
            key = items[0].lower()
            if key not in CommandParser.consDict:
                raise ParseError('Line {}: Unknown constructor {}'.format(items[0]))
            constructor = CommandParser.consDict[key]
            args = items[1:]
            if key != 'add' and	 len(args) != constructor.args - 1:
                raise ParseError('Line {}: When parsing {} command expected {} arguments but found {}'.format(
                    i, items[0], constructor.args, len(args)
                ))
            if key == 'add':
                result.append(self.parse_add(i, line))
            else:
                result.append(constructor(self.session, *args))

        return result

    def parse_add(self, i, line):
        if not line.lower().startswith('add '):
            raise ParseError('Line {}: Cannot parse_add: "{}"'.format(i, line))
        l = line[4:].strip()
        if not l.startswith('(') or not l.endswith(')'):
            raise ParseError('Line {}: ADD expects a tuple of arguments but found: "{}" '
                             .format(i, l))
        l = l[1,-1]
        args = l.split(',')
        return Add(self.session, args)



class ParseError(RuntimeError):
    def __init__(self, message):
        RuntimeError.__init__(self)
        print('[!]' + message, file=sys.stderr)
