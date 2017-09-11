#!/usr/bin/env python
''' snapshots.py: How to use this file:
    this is a basic git directory tracker (super low functionality). What does
    it do? First, create a GitDirLog with

        import snapshots
        log = snapshots.GitDirLog(path_to_git_directory)

    Note that the git directory is the actual .git/ directory (not your repo!)
    Then go ahead and create a snapshot with:

        log.take_snapshot('optional message')

    Note that the message is pretty important for knowing what each snapshot is.
    Okay, now that you've taken a snapshot go make a change to your repository
    (with a git add, git commit, git branch, git checkout, etc) and take another
    snapshot:

        log.take_snapshot('I made a change and I liked iiiit')

    Note that this will return the snapshot object

'''
from os import walk
from os import path
from datetime import datetime
import hashlib

FILE='f'
DIR='d'

class Entry:
    def __init__(self, name, contents = None, sha1 = 0, tp=DIR, 
                 cdate = -1, mdate = -1):
        self.name = name
        self.contents = contents
        self.sha1 = sha1
        self.type = tp
        self.cdate = cdate
        self.mdate = mdate

    def __str__(self):
        return '[{}] {}'.format(self.type, self.name) 

    def long_string(self):
        return '[{}] {} : {} : {}'.format(self.type, self.name, self.sha1, 
                                    self.cdate, self.mdate) 
        
    def __repr__(self):
        return str(self)

class GitDirParser:
    ext_to_ignore = ['swp']
    entries = []
    def __init__(self, mypath):
        self.path  = mypath
        for (dirpath, dirnames, fnames) in walk(mypath):
            for d in dirnames:
                dname = dirpath + '/' + d
                contents = None
                sha1 = 0
                cdt = str(datetime.fromtimestamp(path.getctime(dname)))
                mdt = str(datetime.fromtimestamp(path.getmtime(dname)))
                self.entries.append(Entry(dname, contents=None, sha1=0, tp=DIR,
                                      cdate = cdt, mdate = mdt))
            for f in fnames:
                fname = path.join(dirpath, f)
                try:
                    with open(fname, 'rb') as afile:
                        contents = str(afile.read()).encode('utf-8')
                    sha1hasher = hashlib.sha1()
                    sha1hasher.update(contents)
                    sha1 = sha1hasher.hexdigest()
                    cdt = str(datetime.fromtimestamp(path.getctime(fname)))
                    mdt = str(datetime.fromtimestamp(path.getmtime(fname)))
                    self.entries.append(Entry(fname, contents, sha1, tp=FILE,
                            cdate=cdt, mdate=mdt))
                except:
                    print("Error reading fname: " + fname + '. ' + dirpath, dirnames, fnames)



class DiffObject:
    def __init__(self, fst, snd, created, removed, modified, static):
        '''
            fst: GitDirSnapshot
            snd: GitDirSnapshot
            created: list of entries that were created (from fst to snd)
            removed: list of entries that were removed (from fst to snd)
            modified: list of entires that were modified (from fst to snd)
            static: list of entries that were unchanged (from fst to snd)
        '''
        self.fst = fst
        self.snd = snd
        self.created = created
        self.removed = removed
        self.modified = modified
        self.static = static

    def print_diff(self, updated_only = True):
        print('+' + '-'*78 + '+')

        s = 'Difference Object: {} -> {}'.format(self.fst.message, self.snd.message)
        s = '{0: ^78}'.format(s)

        print('|' + s + '|')
        print('+' + '-'*78 + '+')

        print('| created [{}]:'.format(len(self.created)))
        for o in self.created:
            print('|    ',o)
        print('| modified [{}]:'.format(len(self.modified)))
        for o in self.modified:
            print('|    ',o)
        print('| removed [{}]:'.format(len(self.removed)))
        for o in self.removed:
            print('|    ',o)

        if not updated_only:
            print('| static [{}]:'.format(len(self.static)))
            for o in self.static:
                print('|    ',o)
        print('+' + '-'*78 + '+')

class GitDirSnapshot:
    def __init__(self, dir_to_parse, message = ''):
        self.entries = {}
        self.message = message
        gdp = GitDirParser(dir_to_parse)
        for entry in gdp.entries:
            self.entries[entry.name] = entry

    def parse_git_directory(self, dir_to_parse):
        pass

    def diff(self, other):
        ''' assuming that self is newer than other, calculate the difference
            in the .git directory tree'''
        mykeys = self.entries.keys()
        otherkeys = other.entries.keys()
        allkeys = set(mykeys).union(set(otherkeys))

        created = []
        removed = []
        modified = []
        static  = []

        for key in allkeys:

            if key not in other.entries:
                # key must be in self.entries and hence created
                created.append(self.entries[key])
            
            elif key in self.entries and key in other.entries:

                this,that = self.entries[key], other.entries[key]
                if this.type == 'd' and that.type == 'd':
                    static.append(this)

                elif this.type == 'f' and that.type == 'f':
                    if this.sha1 == that.sha1:
                        static.append(this)
                    else:
                        modified.append(this)
                else:
                    modified.append(this)

            elif key not in self.entries:
                removed.append(other.entries[key])
                
        return DiffObject(other, self, created=created, 
                                       removed=removed, 
                                       modified=modified, 
                                       static=static)

    def __str__(self):
        return 'Snapshot[{}]'.format(self.message)

    def __repr__(self):
        return 'Snapshot[{}] with {} entries'.format(self.message, len(self.entries))

class GitDirLog:
    '''takes a snapshot of the .git directory'''
    def __init__(self, gitdir, autodiff=True):
        '''
            gitdir: directory to track
            autodiff: track diffs (and print them) automatically
        '''
        self.snapshots = []
        self.gitdir = gitdir
        self.autodiff = autodiff

    def take_snapshot(self, message = ''):
        snap = GitDirSnapshot(self.gitdir, message)
        self.snapshots.append(snap)
        if self.autodiff and len(self.snapshots) > 1:
            s1,s2 = self.snapshots[-2:]
            s2.diff(s1).print_diff()
        return snap
    
    def compute_diffs(self):
        diffs = []
        for i in range(1, len(self.snapshots)):
            s1, s2 = self.snapshots[i-1], self.snapshots[i]
            diffs.append(s2.diff(s1))
        return diffs

