from unittest import TestCase
from os import path as osp
import os

from gitutil.commands import *
from gitutil.session import GitSession

join = osp.join


class TestCommandParser(TestCase):

    def setUp(self):
        self.session = GitSession()
        self.parser = CommandParser(self.session)

    def tearDown(self):
        self.session.cleanup()

    def test_consume_string1(self):
        parser = self.parser
        head = "\"This is a test\""
        tail = " and this is another"
        s = head + tail
        left, right = parser.consume_string(s)
        self.assertEqual(head[1:-1], left)
        self.assertEqual(tail, right)

    def test_consume_string2(self):
        parser = self.parser
        head = "\"This is a test \\\" with an internal string\\\"\""
        tail = " and this is another"
        s = head + tail
        left, right = parser.consume_string(s)
        self.assertEqual(head[1:-1], left)
        self.assertEqual(tail, right)

    def test_consume_ws1(self):
        parser = self.parser
        head, tail = "          \n\n\n\n\n", "HELLO"
        s = head + tail
        left, right = parser.consume_ws(s)
        self.assertEqual(head, left)
        self.assertEqual(tail, right)
        self.assertEqual(6, parser.line)

    def test_consume_ws2(self):
        parser = self.parser
        head, tail = "", "HELLO"
        s = head + tail
        left, right = parser.consume_ws(s)
        self.assertEqual(head, left)
        self.assertEqual(tail, right)

    def test_consume_tuple1(self):
        parser = self.parser
        head, tail = "(this, is, a  ,   test)", "( and, this, is, another)"
        s = head + tail
        left, right = parser.consume_tuple(s)
        self.assertEqual(head, left)
        self.assertEqual(tail, right)

    def test_parse_add1(self):
        s = 'add (foo,bar,baz)\nadd (foo,baz,bar,bing)'
        parser = self.parser
        result = parser.parse(s)

        self.assertEqual(2, len(result))
        self.assertIsInstance(result[0], Add,
                              "add should, well, add...")
        self.assertEqual(3, len(result[0].files))
        self.assertIsInstance(result[1], Add,
                              "add should, well, add...")
        self.assertEqual(4, len(result[1].files))

    def test_parse_add2(self):
        s = 'add (foo)'
        parser = self.parser
        result = parser.parse(s)

        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], Add,
                              "add should, well, add...")
        self.assertEqual(1, len(result[0].files))
        self.assertEqual('foo', result[0].files[0])

    def test_parse_commit(self):
        s = 'commit "This is a commit message"'
        parser = self.parser
        result = parser.parse(s)

        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], Commit,
                              "commit should create a commit")

    def test_parse_branch(self):
        s = 'branch new-branch'
        parser = self.parser
        result = parser.parse(s)

        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], Branch,
                              "branch should return a Branch instance")
        self.assertEqual('new-branch', result[0].branch_name)

    def test_parse_checkout(self):
        s = 'checkout branch-name'
        parser = self.parser
        result = parser.parse(s)

        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], Checkout,
                              "checkout should return a Checkout instance")
        self.assertEqual('branch-name', result[0].branch_name)

    def test_parse_touch(self):
        parser = self.parser
        s = 'touch path/to/foo.txt'
        result = parser.parse(s)

        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], CreateFile,
                              "touch should create a file")

    def test_parse_mkdir(self):
        parser = self.parser
        s = 'mkdir path/to/dir'
        result = parser.parse(s)

        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], CreateDirectory,
                              "mkdir should create a directory")

    def test_parse_string(self):
        directory = osp.dirname(osp.abspath(__file__))
        with open(join(directory, 'resources', 'parse-file1.txt')) as f:
            s = f.read()

        parser = self.parser
        parsed = parser.parse(s)
        for c in parsed:
            c.execute()
        expected = [
                    CreateFile, CreateFile, CreateFile,
                    CreateDirectory, CreateDirectory, CreateDirectory,
                    CreateFile, CreateFile, CreateFile,
                    AppendLineToFile, AppendLineToFile, AppendLineToFile,
                    Add, Commit]

        for a, e in zip(parsed + ([None] * 20), expected):
            self.assertIsInstance(a,e)
