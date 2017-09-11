class GitIndex:
    def __init__(self, index):
        '''
            parse an index file
        '''
        self.contents = index
        self.magic_number = index[0:4]
        self.version = 0

        vb = index[5:8]
        for b in vb:
            self.version = 256 * self.version + int(b)
        
        self.filecount = 0
        fc = index[9:12]
        for b in fc:
            self.filecount += 256 * self.filecount + int(b)
