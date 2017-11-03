"""
filesystem.py represents files and directories
"""

class File:
    """ A file in the file system """
    def __init__(self, name, contents, parent=None):
        self.name = name
        self.contents = contents
        self.parent = parent

class Directory:
    """ A directory in the file system """

    def __init__(self, name, files=None, directories=None, parent=None):
        self.name = name
        self.files = files
        self.directories = directories
        self.parent = parent
