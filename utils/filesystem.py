"""
filesystem.py represents files and directories
"""

class File:
    """ A file in the file system """
    def __init__(self, name, contents, parent=None):
        self.name = name
        self.contents = contents
        self.parent = parent

    def __eq__(self, other):
        """ This does not compare contents - only name and parent """
        return self.name == other.name and self.parent == other.parent


class Directory:
    """ A directory in the file system """

    def __init__(self, name, files=None, directories=None, parent=None):
        self.name = name
        self.files = files
        self.directories = directories
        self.parent = parent

        if files is None:
            self.files = []
        if directories is None:
            self.directories = []

    def add_file(self, file):
        """ add a file to self """
        if file not in self.files:
            self.files.append(file)

    def add_directory(self, directory):
        """ add a directory to self """
        if directory not in self.directories:
            self.directories.append(directory)

    def __eq__(self, other):
        """ Compare directories """
        return self.name == other.name and self.parent == other.parent
