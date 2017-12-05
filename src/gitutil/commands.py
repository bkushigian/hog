from os.path import join
import os
import sys
import string

class Command:
    """
    A FileSystemAction represents an action on a file or a directory. This is
    a mixin that specifies that an action can be executed via method execute,
    which is parametrized by a file name.
    """
    def execute(self):
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

    def __str__(self):
        return "<Add {}>".format(self.files)

    def __repr__(self):
        return "<Add {}>".format(self.files)


class Commit(Command):
    args = 2
    commit_number = 1

    def __init__(self, session, message=None):
        self.session = session
        self.message = message
        self.number = Commit.commit_number
        Commit.commit_number += 1
        if message is None:
            self.message = "commit {}".format(self.number)

    def execute(self):
        return self.session.repo().index.commit(self.message)

    def __str__(self):
        return "<Commit {}: \"{}\">".format(self.number, self.message)

    def __repr__(self):
        return "<Commit {}: \"{}\">".format(self.number, self.message)


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

    def __str__(self):
        return "<CreateFile {}>".format(self.path)

    def __repr__(self):
        return "<CreateFile {}>".format(self.path)


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
        f.write(self.line + '\n')
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
    def __init__(self, session):
        self.session = session
        self.line = 1
        self.linepos = 0
        self.pos = 0
        self.last_result = None  # Track the result of the last consume

    def parse_file(self, file):
        with open(file) as f:
            contents = f.read()
        return self.parse(contents)

    def parse(self, script):
        length = len(script)
        s = script[self.pos:]
        result = []
        while s:
            _, s = self.consume_ws(s)
            # TODO: Consume comments
            word, s = self.consume_word(s)
            _, s = self.consume_ws(s)
            if word == '':
                break
            elif word == 'add':
                _, s = self.consume_tuple(s)
                files = self.last_result
                result.append(Add(self.session, files))

            elif word == 'commit':
                msg, s = self.consume_string(s)
                result.append(Commit(self.session, msg))

            elif word == 'touch':
                fpath, s = self.consume_word(s)
                result.append(CreateFile(self.session, fpath))

            elif word == 'mkdir':
                fpath, s = self.consume_word(s)
                result.append(CreateDirectory(self.session, fpath))

            elif word == 'append-to-file' or word == '>>':
                fname, s = self.consume_word(s)
                _, s = self.consume_ws(s)
                line, s = self.consume_string(s)
                result.append(AppendLineToFile(self.session, fname, line))
            elif word == 'append-to-line':
                raise NotImplementedError()
            elif word == 'insert-line':
                raise NotImplementedError()
            elif word == 'delete-line':
                raise NotImplementedError()
            elif word == 'read-file':
                raise NotImplementedError()
            elif word == 'read-file-lines':
                raise NotImplementedError()
            else:
                raise ParseError('Unrecognized Command')
            _, s = self.consume_ws(s)
        return result

    def consume_ws(self, s):
        self.last_result = None
        """
        Consume whitespace at the start of a string, keeping track of
        the current line number and the current position, and return a tuple
        (consumed, remaining)
        :param s: string to parse
        :return: (leading_ws, remaining)
        :invariant: leading_ws + remaining = s
        """
        pos = 0
        length = len(s)
        if length == 0:
            return '', ''
        c = s[0]
        while c in string.whitespace:
            self.linepos += 1
            if c == '\n':
                self.line += 1
                self.linepos = 0
            pos += 1
            if pos >= length:
                self.pos = -1
                return s, ''
            c = s[pos]

        self.pos += pos
        return s[:pos], s[pos:]

    def consume_string(self, s):
        self.last_result = None
        pos = 0
        length = len(s)
        if length == 0:
            return '', ''
        c = s[0]
        if c != "\"":
            return '', s
        quote_pos = self.linepos
        quote_line = self.line
        if length == 1:
            raise ParseError("({}:{}) Unmatched quote"
                             .format(self.line, self.linepos))
        pos += 1
        c = s[pos]
        self.linepos += 1
        while c != "\"":
            if c == "\\":
                pos += 2
                self.linepos += 2
                if pos >= length:
                    raise ParseError("({}:{}) Unmatched quote"
                                     .format(self.line, self.linepos))
                if s[pos - 1] == '\n':
                    self.line += 1
                    self.linepos = 0
                c = s[pos]
            elif c == "\n":
                raise ParseError("({}:{}) Unescaped newline in string"
                                 .format(self.line, self.linepos))
            else:
                pos += 1
                if pos >= length:
                    raise ParseError("({}:{}) Unmatched quote"
                                     .format(self.line, self.linepos))
                c = s[pos]
        pos += 1
        self.linepos += 1
        self.pos += pos
        return s[1:pos-1], s[pos:]

    def consume_tuple(self, s):
        self.last_result = None
        pos = 0
        length = len(s)
        if length is 0:
            return '', ''
        c = s[0]
        if c is not '(':
            return '', s
        pos += 1
        self.linepos += 1
        c = s[pos]

        entries = []
        entry_type = None

        while c is not ')':
            left, right = self.consume_ws(s[pos:])
            pos += len(left)
            if pos >= length:
                raise ParseError("({}:{}) Invalid tuple"
                                 .format(self.line, self.linepos))
            c = s[pos]
            if c == '"':
                if entry_type is None:
                    entry_type = 'str'
                elif entry_type is not 'str':
                    raise ParseError("({}:{}) Mixed tuple type"
                                     .format(self.line, self.linepos))
                left, right = self.consume_string(s[pos:])
                pos += len(left)
                entries.append(left)
                c = s[pos]

            elif c in ',':
                raise ParseError("({}:{}) Empty tuple entry"
                                 .format(self.line, self.linepos))

            else:
                if entry_type is None:
                    entry_type = 'word'
                elif entry_type is not 'word':
                    raise ParseError("({}:{}) Mixed tuple type"
                                     .format(self.line, self.linepos))
                left, right = self.consume_word(s[pos:], exclude='),')
                pos += len(left)
                entries.append(left)
                c = s[pos]
                if c is ',':
                    pos += 1
                    if pos >= length:
                        raise ParseError("Unmatched open parenthesis")

            left, right = self.consume_ws(s[pos:])
            pos += len(left)
            c = s[pos]
            if c is ',':
                pos += 1
                self.linepos += 1
                c = s[pos]

        pos += 1
        self.linepos += 1
        self.pos += pos
        self.last_result = entries   # Attach to global state
        return s[:pos], s[pos:]

    def consume_word(self, s, exclude=')"'):
        self.last_result = None
        pos = 0
        length = len(s)
        while pos < length and s[pos] not in string.whitespace \
                and s[pos] not in exclude:
            pos += 1
        self.pos += pos
        self.linepos += pos
        return s[:pos], s[pos:]

    def parse_add(self, i, line):
        if not line.lower().startswith('add '):
            raise ParseError('Line {}: Cannot parse_add: "{}"'.format(i, line))
        l = line[4:].strip()
        if not l.startswith('(') or not l.endswith(')'):
            raise ParseError('Line {}: ADD expects a tuple of arguments but found: "{}" '
                             .format(i, l))
        l = l[1: -1]
        args = list(map(lambda s: s.strip(),l.split(',')))
        return Add(self.session, args)


class ParseError(RuntimeError):
    def __init__(self, message):
        RuntimeError.__init__(self)
        print('[!]' + message, file=sys.stderr)
