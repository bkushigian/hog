"""
filesystem.py represents files and directories
"""

import os


class File:
    """ A file in the file system """
    def __init__(self, name, contents='', parent=None):
        """
        Create a new File object
        :param name: str representing the name of the file (i.e., 'foo.txt')
        :param contents: optional str representing the contents o the file
        :param parent: optional Directory instance representing the parent
        directory of this file. If this is None (i.e., unspecified) then the
        parent is undefined.
        """
        assert isinstance(name, (bytes, str)), \
            'name must be type bytes or str but found {} instead'.format(type(name))
        assert isinstance(contents, (bytes, str)), \
            'contents must be type bytes or str but found {} instead'.format(type(contents))
        self.name = name
        self.contents = contents
        self.parent = None
        self.set_parent(parent)
        self.absolute_path = None

    def calculate_absolute_path(self):
        if self.parent is None:
            return None
        return os.path.join(self.parent.absolute_path, self.name)

    def is_child_of(self, directory):
        if directory is None:
            return False

        if self in directory.files:
            return True

        if self.parent:
            return self.parent.is_child_of(directory)

        return False

    def set_parent(self, parent):
        """ Set self's parent and add self to parent.files """
        if self.parent == parent:
            return
        if self.parent is not None:
            self.parent.files.remove(self)
        self.parent = parent
        if parent:
            parent.add_file(self)

    def __eq__(self, other):
        """ This does not compare contents - only name and parent """
        if not isinstance(other, File):
            return False
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
        self.absolute_path = None

        if files is None:
            self.files = []
        if directories is None:
            self.directories = []

    def add_file(self, file):
        """ add a file to self """
        if not isinstance(file, File):
            raise TypeError()

        if file not in self.files:
            self.files.append(file)
            file.set_parent(self)

    def add_directory(self, directory):
        """ add a directory to self """
        if not isinstance(directory, Directory):
            raise TypeError()

        if directory not in self.directories:
            self.directories.append(directory)
            directory.set_parent(self)

    def calculate_absolute_path(self):
        """ calculate the absolute path of this directory """
        if self.parent is None:
            Path(self)
        else:
            self.absolute_path = os.path.join(self.parent.absolute_path, self.name)
        return self.absolute_path

    def is_child_of(self, directory):
        """
        Determines if self is an ancestor of directory
        :param directory:
        :return: True if self is a child of directory; False otherwise
        """
        if directory is None:
            return False

        if self.parent == directory:
            return True

        if self.parent:
            return self.parent.is_child_of(directory)

        return False

    def set_parent(self, parent):
        """
        Set the parent Directory of this Directory.
        :param parent: the new parent Directory of self
        :return: None
        """
        if self.parent == parent:
            return
        if self.parent is not None:
            self.parent.directories.remove(self)
        self.parent = parent
        if parent:
            parent.add_directory(self)

    def __eq__(self, other):
        """ Compare directories """
        if not isinstance(other, Directory):
            return False
        return self.name == other.name and self.parent == other.parent

    def __hash__(self):
        return hash(hash(self.name, hash(self.parent)))

    def __contains__(self, item):
        if isinstance(item, File):
            return item in self.files

        if isinstance(item, Directory):
            return item in self.directories

        return False

    def __repr__(self):
        return 'Directory(' + self.name + '/)'

    def __str__(self):
        return self.name


class Path:
    def __init__(self, path=None):
        """
        :param path: a File, a Directory, or a list of Directories possibly
        ending with a File
        """
        if path is None:
            self.path = []
        elif isinstance(path, Directory) or isinstance(path, File):
            self.path = [path]
        else:
            self.path = path
        self.assert_invariant()

    def is_empty(self):
        return len(self) == 0

    def check_invariant(self):
        """
            A path should consist solely of directories except for the last
            entry which may be a file. This returns true when these are
            satisfied.
        """

        if self.is_empty():
            return True

        for entry in self.path[:-1]:
            if not isinstance(entry, Directory):
                return False

        return isinstance(self.path[-1], Directory) or isinstance(self.path[-1], File)

    def assert_invariant(self):
        if not self.check_invariant():
            raise InvalidPathException("Invalid path: {}".format(str(self)))

    def __add__(self, other):
        """ Add this path to another """
        assert isinstance(other, Path)
        result = Path(self.path + other.path)
        result.assert_invariant()
        return result

    def __getitem__(self, item):
        assert isinstance(item, int)
        return self.path[item]

    def __len__(self):
        return len(self.path)

    def __repr__(self):
        if self.path:
            strings = []
            for e in self.path:
                print(e.__str__())
                strings.append(str(e))
            return 'Path({})'.format(os.path.join(*strings))
        return 'EmptyPath'

    def __str__(self):
        if self.path:
            return os.path.join(*map(str, self.path))
        return ''


class InvalidPathException(Exception):
    def __init__(self, message=''):
        self.message = message

    def __repr__(self):
        return 'InvalidPathException({})'.format(self.message)

    def __str__(self):
        return 'InvalidPathException({})'.format(self.message)

