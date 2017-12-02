from unittest import TestCase

from os import path as osp
from os.path import join
from git.session import GitSession
from git.commands import (Command,
                          Add,
                          Commit,
                          AppendLineToFile,
                          AppendLinesToFile,
                          AppendStringToLine,
                          InsertLineAfterLine,
                          InsertLinesAfterLine,
                          DeleteLine
                          )


class TestCommand(TestCase):

    def setUp(self):
        self.session = GitSession()
        self.dir = self.session.dir()
        self.git = self.session.git
        self.repo = self.session.repo()

    def test_add1(self):
        f1 = join(self.dir, 'f1')
        add = Add([f1])

        with open(f1, 'w') as f:
            f.write('hello')

        add.execute(self.session)

