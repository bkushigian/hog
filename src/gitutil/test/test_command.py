from unittest import TestCase

from os import path as osp
from os import walk
from os.path import join
from gitutil.session import GitSession
from gitutil.commands import (Command,
                              Add,
                              Branch,
                              Checkout,
                              Commit,
                              CreateFile,
                              CreateDirectory,
                              AppendLineToFile,
                              AppendLinesToFile,
                              AppendStringToLine,
                              InsertLineAfterLine,
                              InsertLinesAfterLine,
                              DeleteLine,
                              ReadFile,
                              ReadFileLines,
                              )


class TestCommand(TestCase):

    def setUp(self):
        self.session = GitSession()
        self.dir = self.session.dir()
        self.git = self.session.git
        self.repo = self.session.repo()

    def tearDown(self):
        self.session.cleanup()
        self.dir = None
        self.git = None
        self.repo = None

    def test_add1(self):
        f1 = join(self.dir, 'f1')
        add = Add(self.session, [f1])

        with open(f1, 'w') as f:
            f.write('hello')

        add.execute()
        entries = [t[0] for t in self.repo.index.entries.keys()]
        self.assertIn('f1', entries)

    def test_add2(self):
        f1 = join(self.dir, 'f1')
        f2 = join(self.dir, 'f2')

        with open(f1, 'w') as f:
            f.write('This is file 1')

        with open(f2, 'w') as f:
            f.write('This is file 2')

        Add(self.session, [f1, f2]).execute()
        entries = [t[0] for t in self.repo.index.entries.keys()]
        self.assertIn('f1', entries)
        self.assertIn('f2', entries)

    def test_branch1(self):
        f1 = join(self.dir, 'f1')
        f2 = join(self.dir, 'f2')

        with open(f1, 'w') as f:
            f.write('This is file 1')

        with open(f2, 'w') as f:
            f.write('This is file 2')

        Add(self.session, [f1, f2]).execute()
        Commit(self.session, 'first commit').execute()
        Branch(self.session, 'new-branch').execute()

        heads = self.session.repo().heads
        self.assertEqual('master', heads[0].name)
        self.assertEqual('new-branch', heads[1].name)

    def test_checkout1(self):
        f1 = join(self.dir, 'f1')
        f2 = join(self.dir, 'f2')

        with open(f1, 'w') as f:
            f.write('This is file 1')

        with open(f2, 'w') as f:
            f.write('This is file 2')

        Add(self.session, [f1, f2]).execute()
        Commit(self.session, 'first commit').execute()
        Branch(self.session, 'new-branch').execute()

        with open(f1, 'w') as f:
            f.write('This is an updated file 1')

        with open(f2, 'w') as f:
            f.write('This is an updated file 2')

        Add(self.session, [f1, f2]).execute()
        Commit(self.session, 'second commit').execute()
        Checkout(self.session, 'new-branch').execute()
        self.assertEqual('new-branch', self.session.repo().head.ref.name)

    def test_commit1(self):
        f1 = join(self.dir, 'f1')
        f2 = join(self.dir, 'f2')

        with open(f1, 'w') as f:
            f.write('This is file 1')

        with open(f2, 'w') as f:
            f.write('This is file 2')

        Add(self.session, [f1, f2]).execute()
        Commit(self.session, 'first commit').execute()
        c = self.session.repo().commit()
        self.assertEqual('first commit', c.message)


    def test_create_file(self):
        cmd = CreateFile(self.session, 'f1')
        cmd.execute()  # Creates a file named f1

        top_level_fs = next(walk(self.dir))[2]
        self.assertIn('f1', top_level_fs)

    def test_create_directory(self):
        CreateDirectory(self.session, 'd').execute()
        CreateDirectory(self.session, 'e').execute()
        top_level_fs = next(walk(self.dir))[1]
        self.assertIn('d', top_level_fs)
        self.assertIn('e', top_level_fs)

    def test_append_line_to_file(self):
        CreateFile(self.session, 'f').execute()
        AppendLineToFile(self.session, 'f', 'this is a test').execute()
        self.assertEqual('this is a test\n', ReadFile(self.session, 'f').execute())

    def test_append_lines_to_file(self):
        lines = [
            'this is the first line',
            'this is the second line',
            'this is the third line',
            '',
            'this is the fourth line!'
        ]

        expected = '\n'.join(lines)

        CreateFile(self.session, 'f').execute()
        AppendLinesToFile(self.session, 'f', lines).execute()
        self.assertEqual(expected, ReadFile(self.session, 'f').execute())

    def test_append_string_to_line(self):

        lines = [
            'this is the first line',
            'this is the second line',
            'this is the third line',
            '',
            'this is the fourth line!'
        ]

        expected = '\n'.join(lines)

        CreateFile(self.session, 'f').execute()
        AppendLinesToFile(self.session, 'f', lines).execute()
        AppendStringToLine(self.session, 'f', 0, ' TEST1').execute()
        AppendStringToLine(self.session, 'f', 1, ' TEST2').execute()
        AppendStringToLine(self.session, 'f', 2, ' TEST3').execute()
        AppendStringToLine(self.session, 'f', 3, ' TEST4').execute()
        result = ReadFileLines(self.session, 'f').execute()
        self.assertEqual(lines[0] + ' TEST1\n', result[0])
        self.assertEqual(lines[1] + ' TEST2\n', result[1])
        self.assertEqual(lines[2] + ' TEST3\n', result[2])
        self.assertEqual(lines[3] + ' TEST4\n', result[3])
        self.assertEqual(lines[4]             , result[4])

