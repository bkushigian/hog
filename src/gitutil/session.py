import os
from os import path as osp
import shutil
import tempfile
import git

from gitutil.commands import CommandParser

join = osp.join


class GitSession:
    """
    Represents a temporary git session stored in a temporary directory. This
    is used to allow the student to have small working examples of Git
    repositories. GitSession is responsible for creating a temp directory
    (if one is not provided) and initializing a git repository in it. If a
    directory is provided and there is already a repository, throw an exception.
    """
    def __init__(self, dir=None, create_repo=True):
        """
        Create a new GitSession
        :param dir: directory to work in (default creates a tmp directory)
        :param create_repo: True to initialize a repository (Not implemented)
        """
        self._dir = dir
        if dir is None:
            self._dir = tempfile.mkdtemp()

        if create_repo:
            # TODO: Ensure that a git repo doesn't already exist
            #       if it does, throw an exception

            git.Git(self._dir).init()
            pass

        self._repo = git.Repo(self._dir)
        self.git = self._repo.git

    def dir(self):
        return self._dir

    def repo(self):
        return self._repo

    def cleanup(self):
        shutil.rmtree(self._dir)
        del self._repo
        del self.git

    def load_script(self, script_name):
        with open(script_name) as f:
            script = f.read()

        parser = CommandParser(self)
        commands = parser.parse(script)
        return commands

    def run_script(self, script_name):
        commands = self.load_script(script_name)
        for c in commands:
            c.execute()


class AutoGenGitRepo:
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
