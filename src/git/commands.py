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
    def __init__(self, files=None):
        """
        :param files: list of files to add
        """
        self.files = files

    def execute(self):
        pass


class Commit(Command):
    def __init__(self, message=None):
        self.message = message
        if message is None:
            self.message = ""

    def execute(self):
        pass

class AppendLineToFile(Command):
    """
    Append line to file
    """
    def __init__(self, line):
        self.line = line

    def execute(self, file):
        f = open(file, 'a')
        f.write(self.line)
        f.close()


class AppendLinesToFile(Command):
    """
    Append lines to file
    """
    def __init__(self, lines):
        self.lines = lines

    def execute(self, file):
        f = open(file, 'a')
        f.write('\n'.join(self.lines))
        f.close()


class AppendStringToLine(Command):
    """
    Append a string to a particular line.
    """
    def __init__(self, line, string):
        self.line = line
        self.string = string

    def execute(self, file):
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        lines[self.line] = lines[self.line][:-1] + self.string + '\n'
        f = open(file, 'w')
        f.write(''.join(lines))
        f.close()


class InsertLineAfterLine(Command):
    def __init__(self, lineno, line):
        self.lineno = lineno
        self.line = line

    def execute(self, file):
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        lines = lines[:self.lineno] + [self.line] + lines[self.lineno:]
        f = open(file, 'w')
        f.write('\n'.join(lines))
        f.close()


class InsertLinesAfterLine(Command):
    def __init__(self, line, lines):
        self.line = line
        self.lines = lines

    def execute(self, file):
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        lines = lines[:self.line] + self.lines + lines[self.line:]
        f = open(file, 'w')
        f.write('\n'.join(lines))
        f.close()

class DeleteLine(Command):
    def __init__(self, line):
        self.line = line

    def execute(self, file):
        f = open(file, 'r')
        lines = f.read()
        f.close()

        lines = lines[:self.line] + lines[self.line + 1:]
        f = open(file, 'w')
        f.write('\n'.join(lines))
        f.close()
