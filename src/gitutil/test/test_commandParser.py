from unittest import TestCase
from os import path as osp
import os

from gitutil.commands import *
from gitutil.session import GitSession

join = osp.join


class TestCommandParser(TestCase):

    def setUp(self):
        self.session = GitSession()

    def tearDown(self):
        self.session.cleanup()

    def test_parse_string(self):
        session = self.session
        directory = osp.dirname(osp.abspath(__file__))
        with open(join(directory, 'resources','parse-file1.txt')) as f:
            s = f.read()

        parser = CommandParser(session)
        parsed = parser.parse(s)
        for c in parsed:
            c.execute()
        expected = [CreateFile, CreateFile, CreateFile, CreateDirectory,
                    CreateDirectory, CreateDirectory, AppendLineToFile,
                    AppendLineToFile, AppendLineToFile, Add]

        for a, e in zip(parsed + ([None] * 20), expected):
            self.assertIsInstance(a,e)
