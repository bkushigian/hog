"""
    gitobjs.py represents Git atomics - commits, HEAD, index, etc.
"""

import utils.filesystem as fs

ZEROBYTES    = bytes('\x00'.encode('utf-8'))
NEWLINEBYTES = bytes('\n'.encode('utf-8'))
SPACEBYTES   = bytes(' '.encode('utf-8'))


class GitDir(fs.Directory):
    """
        This should take a parsed git directory and extract the relevant info,
        wrapping the content in the semantics of the Git dir. This represents a moment
        in time and stores the data in a snapshot.
    """
    def __init__(self, parsed):
        super().__init__('.git', [], [], None)
        self.branches = None
        self.COMMIT_EDITMSG = None
        self.config = None
        self.description = None
        self.HEAD = None
        self.hooks = None
        self.index = None
        self.info = None
        self.logs = None
        self.objects = None
        self.refs = None


class GitBranch:
    """GitBranch represents a branch in Git."""
    pass


class GitCommitObj:
    """Represents a commit"""
    pass


class Git_COMMIT_EDITMSG:
    pass


class GitHead:
    """GitHead represents the HEAD ref"""
    pass


class GitIndex:
    def __init__(self, index, verbose=True):
        """
            parse an index file
        """
        self.contents = index
        self.magic_number = index[0:4]
        self.version = self.bytes_to_int(index[5:8])
        self.filecount = self.bytes_to_int(index[9:12])
        self.cached_tree_entries = []
        self.indexEntries = []
        xs = index[12:]
        while xs:
            xs.strip(ZEROBYTES)
            if xs.startswith('TREE'.encode('utf-8')):
                self.cached_tree_entries, xs = self.read_tree_extension(xs, verbose)
                break
            else:
                entry, xs = self.read_index_entry(xs, verbose)

    def read_tree_extension(self, bs, verbose = True):
        if verbose:
            print("Reading tree extension")
        if not bs.startswith("TREE".encode('utf-8')):
            if verbose:
                print("Not a valid cached-tree extension")
            return (None, bs)
        xs = bs[4:]
        xs.strip(ZEROBYTES)
        trees = []
        t,xs = self.read_cached_tree(xs, verbose)
        if t == None:
            return trees, xs # This should throw an error...
        while xs:
            t,xs = self.read_cached_tree(xs, verbose)
            if t == None:
                break
            trees.append(t)
        return (trees, xs)

    def read_cached_tree(self, bs, verbose=True):
        if verbose:
            print("Reading a cached tree")
        result = {}
        # First, clear zeros from left
        xs = bs
        xs = xs.strip(ZEROBYTES)

        path_comp, xs = self.read_bytes_til_nul(xs)
        xs.strip(ZEROBYTES)

        entries_in_index, xs = self.read_bytes_til(xs, delim=SPACEBYTES)
        xs = xs[1:] # pass the space

        number_of_subtrees, xs = self.read_bytes_til(xs, delim=NEWLINEBYTES)
        xs = xs[1:] # pass the newline

        objname = ''.join(['{:02x}'.format(c) for c in xs[:20]])
        xs = xs[20:]
        xs = xs.strip(ZEROBYTES)

        if path_comp is None or entries_in_index is None or number_of_subtrees is None:
            return (None, bs)
        result['path comp'] = str(path_comp)
        result['entries in index'] = str(entries_in_index)
        result['number of subtrees'] = str(number_of_subtrees)
        result['object-name'] = str(objname)

        if verbose:
            self.print_cached_tree(result)

        return result, xs

    def print_cached_tree(self, tree):
        print('+' + '-'*78 + '+')
        s = 'Cached Tree'
        s = '{0: ^78}'.format(s)
        print(s)
        print('+' + '-'*78 + '+')
        fields = [
            'path comp',
            'entries in index',
            'number of subtrees',
            'object-name',
        ]

        for key in fields:
            print('| {:20}'.format(key + ':') + tree[key])

        print('+' + ('-'*78) + '+')
        print()

    def read_index_entry(self, bs, verbose = True):
        xs = bs
        entry = {}
        fields = [
            ('ctime-sec', 4),
            ('ctime-nano', 4),
            ('mtime-sec', 4),
            ('mtime-nano', 4),
            ('dev', 4),
            ('ino', 4),
            ('mode', 4),
            ('uid', 4),
            ('gid', 4),
            ('file size', 4),
            ('sha1', 20),
            ('flags', 2),
        ]

        for (key, size) in fields:
            entry[key] = hex(self.bytes_to_int(xs[:size]))
            xs = xs[size:]

        name = xs[:xs.find(0)]
        xs = xs[xs.find(0):]
        entry['name'] = str(name)

        self.indexEntries.append(entry) # Just a dictionary for now
        if verbose:
            self.print_index_entry(entry)

        xs = self.strip_zeros_from_bytes(xs)
        return (entry, xs)
        
    def print_index_entry(self, entry):
        fields = [
            'name',
            'ctime-sec',
            'ctime-nano',
            'mtime-sec',
            'mtime-nano',
            'dev',
            'ino',
            'mode',
            'uid',
            'gid',
            'file size',
            'sha1',
            'flags',
        ]
        print('+' + '-'*78 + '+')
        s = 'Index Entry'
        s = '{0: ^78}'.format(s)
        print('|' + s + '|')
        print('+' + '-'*78 + '+')

        for key in fields:
            print('| {:11}:'.format(key) + entry[key])

        print('+' + ('-'*78) + '+')
        print()

    def bytes_to_int(self, bs):
        result = 0
        for b in bs:
            result += 256 * result + int(b)
        return result

    def strip_zeros_from_bytes(self, bs):
        size = len(bs)
        i = 0
        while i < size and bs[i] == 0:
            i += 1
        return bs[i:]

    def read_bytes_til_nul(self, bs, strip_nul = True):
        i = bs.find(ZEROBYTES)
        if i < 0:
            return (None, bs)
        if strip_nul:
            return (bs[:i], bs[i:].strip(ZEROBYTES))
        return (bs[:i], bs[i:])

    def read_bytes_til(self, xs, delim = ZEROBYTES):
        i = xs.find(delim)
        if i < 1:
            return None, xs
        return xs[:i], xs[i:]


class GitObjects:
    pass


class GitRef:
    pass


class GitTree:
    """Represents a tree object"""
    pass


def main():
    with open('.git/index', 'rb') as afile:
        stuff = afile.read()
    index = GitIndex(stuff)

if __name__ == '__main__':
    main()
