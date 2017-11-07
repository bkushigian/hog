import os
import tempfile
import git

class GitSession:
    """
    Represents a temporary git session stored in a temporary directory. This
    is used to allow the student to have small working examples of Git
    repositories. GitSession is responsible for creating a temp directory
    (if one is not provided) and initializing a git repository in it. If a
    directory is provided and there is already a repository, throw an exception.
    """
    def __init__(self, dir=None):
        self.dir = dir
        if dir is None:
            self.dir = tempfile.mkdtemp()

        self.git = git.Git(self.dir)


class AutoGeneratedGitRepo:
    """
    In the interest of automatically creating a git repository, this class
    generates a commit history for a particular lesson.
    """
    def __init__(self, session, to_run=None):
        """
        :param session: The session in which this repository will live.
        :param to_run: A list of commands to run
        """
        self.session = session
        self.to_run = to_run