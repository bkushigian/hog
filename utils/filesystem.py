"""
filesystem.py represents files and directories
"""

import os

class File:
    """ A file in the file system """
    def __init__(self, name, contents='', parent=None):
        self.name = name
        self.contents = contents
        self.parent = parent
        self.absolute_path = self.calculate_absolute_path()

    def calculate_absolute_path(self):
        return os.path.join(self.parent.absolute_path, self.name)

    def set_parent(self, directory):
        self.parent = directory

    def __eq__(self, other):
        """ This does not compare contents - only name and parent """
        return self.name == other.name and self.parent == other.parent

    def __hash__(self):
        return hash(hash(self.name, hash(self.parent)))

    def __repr__(self):
        return 'File(' + self.name + '/)'

    def __str__(self):
        return self.name


class Directory:
    """ A directory in the file system """

    def __init__(self, name, files=None, directories=None, parent=None):
        self.name = name
        self.files = files
        self.directories = directories
        self.parent = parent
        self.absolute_path = self.calculate_absolute_path()

        if files is None:
            self.files = []
        if directories is None:
            self.directories = []

    def add_file(self, file):
        """ add a file to self """
        if file not in self.files:
            self.files.append(file)
            file.set_parent(self)

    def add_directory(self, directory):
        """ add a directory to self """
        if directory not in self.directories:
            self.directories.append(directory)

    def calculate_absolute_path(self):
        if self.parent is None:
            return os.path.join(self.name)
        return os.path.join(self.parent.absolute_path, self.name)

    def set_parent(self, directory):
        self.parent = directory

    def __eq__(self, other):
        """ Compare directories """
        return self.name == other.name and self.parent == other.parent

    def __hash__(self):
        return hash(hash(self.name, hash(self.parent)))

    def __repr__(self):
        return 'Directory(' + self.name + '/)'

    def __str__(self):
        return self.name
