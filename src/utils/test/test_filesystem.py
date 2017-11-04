from unittest import TestCase
from utils.filesystem import File, Directory, Path


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
        root = Directory('')
        path = root.calculate_absolute_path()
        self.assertEqual(1, len(path), 'path {} should have single element: {}'.format(
            path, root ))

    def test_equals(self):
        f = File('f')
        g = File('g')

        self.assertEqual(f, f, '{} and {} are the same file'.format(f, f))
        self.assertNotEqual(f, g, '{} and {} are different files'.format(f, g))


class TestDirectory(TestCase):

    def setUp(self):
        self.f1 = File('f1.txt', 'Contents of f1')
        self.f2 = File('f2.txt', 'Contents of f2')
        self.f3 = File('f3.txt', 'Contents of f3')
        self.f4 = File('f4.txt', 'Contents of f4')
        self.root = Directory('')
        self.d1 = Directory('d1')
        self.d2 = Directory('d2')
        self.d3 = Directory('d3')
        self.d4 = Directory('d4')
        self.files = [self.f1, self.f2, self.f3, self.f4]

    def test_add_file1(self):
        new_file = File('new_file.txt', 'Contents of new file')
        d = Directory('', files=self.files)
        self.assertNotIn(new_file, d)
        self.assertIsNone(new_file.parent)
        d.add_file(new_file)
        self.assertIn(new_file, d)
        self.assertEqual(d, new_file.parent)

    def test_add_file2(self):
        d1 = self.d1
        d2 = self.d2
        f1 = self.f1
        d1.add_file(f1)
        self.assertEqual(d1, f1.parent)
        self.assertIn(f1, d1)

        d2.add_file(f1)
        self.assertEqual(d2, f1.parent)
        self.assertIn(f1, d2)
        self.assertNotIn(f1, d1)

        d1.add_file(f1)
        self.assertEqual(d1, f1.parent)
        self.assertIn(f1, d1)
        self.assertNotIn(f1, d2)

    def test_add_directory1(self):
        root = self.root
        d1 = self.d1
        d2 = self.d2
        root.add_directory(d1)
        root.add_directory(d2)
        self.assertIn(d1, root)
        self.assertIn(d2, root)
        self.assertEqual(root, d1.parent)
        self.assertEqual(root, d2.parent)

    def test_add_directory1(self):
        root = self.root
        d1 = self.d1
        d2 = self.d2
        root.add_directory(d1)
        root.add_directory(d2)
        d1.add_directory(d2)
        self.assertIn(d1, root)
        self.assertNotIn(d2, root)
        self.assertIn(d2, d1)
        self.assertEqual(d1, d2.parent)

    def test_calculate_absolute_path(self):
        pass

    def test_set_parent(self):
        d1 = self.d1
        f1 = self.f1
        d1.add_file(f1)
        self.assertEqual(d1, f1.parent)
        self.assertIn(f1, d1)


class TestPath(TestCase):
    def test_basic_constructor1(self):
        path = Path()
        self.assertTrue(path.is_empty())

    def test_basic_constructor2(self):
        root = Directory('')
        path = Path(root)
        self.assertFalse(path.is_empty())
        self.assertTrue(1, len(path))
        self.assertTrue(path.check_invariant())

    def test_basic_constructor3(self):
        root = Directory('')
        path = Path([root])
        self.assertFalse(path.is_empty())
        self.assertTrue(1, len(path))
        self.assertTrue(path.check_invariant())

    def test_get_item(self):
        d = Directory('d')
        p = Path(d)
        self.assertEquals(d,p[0])

    def test_iadd(self):
        d1 = Directory('d1')
        d2 = Directory('d2')
        p1 = Path([d1])
        p2 = Path([d2])
        p3 = p1 + p2
        self.assertEqual(2, len(p3))
        self.assertEqual(p3[0], d1)
        self.assertEqual(p3[1], d2)

