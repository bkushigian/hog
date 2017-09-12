ZEROBYTES    = bytes('\x00'.encode('utf-8'))
NEWLINEBYTES = bytes('\n'.encode('utf-8'))
SPACEBYTES   = bytes(' '.encode('utf-8'))

class GitIndex:
    def __init__(self, index):
        '''
            parse an index file
        '''
        self.contents = index
        self.magic_number = index[0:4]
        self.version = self.bytes_to_int(index[5:8])
        self.filecount = self.bytes_to_int(index[9:12])
        self.indexEntries = []
        xs = index[12:]
        while xs:
            xs.strip(ZEROBYTES)
            if xs.startswith('TREE'.encode('utf-8')):
                cached_tree_entries, xs = self.read_cached_tree(xs)
                break
            else:
                entry, xs = self.read_index_entry(xs)


    def read_cached_tree(self, bs):
        # XXX: Only reads one entry right now
        if not bs.startswith("TREE".encode('utf-8')):
            return (None, bs)
        xs = bs[4:]
        print(xs)
        xs = xs.strip(ZEROBYTES)
        print(xs)
        path_comp, xs = self.read_bytes_til_nul(xs)
        entries_in_index, xs = self.read_bytes_til(xs, delim=SPACEBYTES)
        xs = xs[1:] # pass the space
        number_of_subtrees, xs = self.read_bytes_til(xs, delim=NEWLINEBYTES)
        xs = xs[1:] # pass the newline
        sha1 = ''.join(['{:02x}'.format(c) for c in xs[:40]])
        print('TREE', 'path_comp:', path_comp, 
            '\nentries_in_index:', entries_in_index, '\nnumber_of_subtrees:',number_of_subtrees, 
            '\nsha1:', sha1)

        return None, xs


    def read_index_entry(self, bs):
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
        entry['name'] = name
        print("ENTRY:" + str(entry))
        print()
        xs = self.strip_zeros_from_bytes(xs)
        self.indexEntries.append(entry) # Just a dictionary for now
        return (entry, xs)
        
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

def main():
    with open('.git/index', 'rb') as afile:
        stuff = afile.read()
    index = GitIndex(stuff)
if __name__ == '__main__':
    main()
