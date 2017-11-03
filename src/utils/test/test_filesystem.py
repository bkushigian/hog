from unittest import TestCase
from utils.filesystem import File, Directory


class TestFile(TestCase):
    def test_basic_constructor(self):
        f = File('f')
        self.assertEquals('f', f.name)
        self.assertEquals('', f.contents)
        self.assertIsNone(f.parent)

    def test_constructor_with_contents(self):
        f = File('f', contents='contents')
        self.assertEquals('f', f.name)
        self.assertEquals('contents', f.contents)
        self.assertIsNone(f.parent)

    def test_constructor_with_parent(self):
        root = Directory('')
        f = File('f', parent=root)
        self.assertEqual('f', f.name)
        self.assertEqual(root, f.parent)
        self.assertIn(f, root.files)

    def test_set_parent(self):
        root = Directory('')
        d1 = Directory('foo', parent=root)
        f = File('f', parent=root)
        f.set_parent(d1)

        self.assertEqual(d1, f.parent)
        self.assertIn(f, d1.files)
        self.assertNotIn(f, root.files)

        f.set_parent(root)

        self.assertEqual(root, f.parent)
        self.assertIn(f, root.files)
        self.assertNotIn(f, d1.files)

    def test_calculate_absolute_path(self):
        pass

    def test_is_child_of(self):
        root = Directory('')
        f = File('f', parent=root)
        self.assertTrue(f.is_child_of(root))

    def test_is_child_of__deep(self):
        root = Directory('')
        d1 = Directory('foo', parent=root)
        d2 = Directory('foo', parent=d1)
        d3 = Directory('foo', parent=d2)
        d4 = Directory('foo', parent=d3)
        f = File('f', parent=d4)

        self.assertTrue(f.is_child_of(d4))
        self.assertTrue(f.is_child_of(d3))
        self.assertTrue(f.is_child_of(d2))
        self.assertTrue(f.is_child_of(d1))
        self.assertTrue(f.is_child_of(root))

    def test_equals(self):
        f = File('f')
        g = File('g')

        self.assertEqual(f, f, '{} and {} are the same file'.format(f, f))
        self.assertNotEqual(f, g, '{} and {} are different files'.format(f, g))


class TestDirectory(TestCase):

    def test_add_file(self):
        pass

    def test_add_directory(self):
        pass

    def test_calculate_absolute_path(self):
        pass

    def test_set_parent(self):
        pass


class TestPath(TestCase):

    def test_iadd(self):
        pass

