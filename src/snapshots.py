#!/usr/bin/env python
""" snapshots.py: How to use this file:
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

"""
import hashlib
from datetime import datetime
from os import path
from os import walk

from git.gitobjs import GitIndex

FILE = 'f'
DIR = 'd'


class Entry:
    """ An Entry represents either a file or a directory and stores information
    about the file such as the name, contents, hash, type, create date and
    modified date.
    """
    def __init__(self, name, contents=None, sha1=0, tp=DIR,
                 cdate=None, mdate=None, uid=None, gid=None, perms=None):
        self.name = name
        self.contents = contents
        self.sha1 = sha1
        self.type = tp
        self.cdate = cdate
        self.mdate = mdate
        self.uid = uid
        self.gid = gid
        self.perms = perms

        idx = name.index('.git')
        self.short_name = name[idx:]

    def __str__(self):
        return '[{}] {}'.format(self.type, self.short_name)

    def long_string(self):
        return '[{}] {} : {} : {}'.format(self.type, self.short_name, self.sha1,
                                    self.cdate, self.mdate) 
        
    def __repr__(self):
        return str(self)


class GitDirParser:
    """ Creates a time-indexed list of entries"""
    ext_to_ignore = ['swp']
    entries = []

    def __init__(self, mypath, verbose=True):
        self.path = mypath
        self.index = None
        if '.git' not in mypath:
            raise RuntimeError("Not a .git repository: " + mypath)
        for (dirpath, dirnames, fnames) in walk(mypath):
            for d in dirnames:
                dname = dirpath + '/' + d
                cdt = str(datetime.fromtimestamp(path.getctime(dname)))
                mdt = str(datetime.fromtimestamp(path.getmtime(dname)))
                self.entries.append(Entry(dname, contents=None, sha1=0, tp=DIR,
                                          cdate=cdt, mdate=mdt))
            for f in fnames:
                fname = path.join(dirpath, f)
                try:
                    with open(fname, 'rb') as afile:
                        contents = afile.read()
                        if fname.endswith('.git/index'):
                            self.index = GitIndex(contents,verbose)
                        contents = str(contents).encode('utf-8')

                    sha1hasher = hashlib.sha1()
                    sha1hasher.update(contents)
                    sha1 = sha1hasher.hexdigest()
                    cdt = str(datetime.fromtimestamp(path.getctime(fname)))
                    mdt = str(datetime.fromtimestamp(path.getmtime(fname)))
                    self.entries.append(Entry(fname, contents, sha1, tp=FILE,
                                              cdate=cdt, mdate=mdt))
                except Exception as e:
                    print("Error reading fname: " + fname + '. ' + dirpath, dirnames, fnames)
                    print(e)


class DiffObject:
    def __init__(self, fst, snd):
        """
            fst: GitDirSnapshot
            snd: GitDirSnapshot
            created: list of entries that were created (from fst to snd)
            removed: list of entries that were removed (from fst to snd)
            modified: list of entires that were modified (from fst to snd)
            static: list of entries that were unchanged (from fst to snd)
        """
        self.fst = fst
        self.snd = snd
        created  = []
        removed  = []
        modified = []
        static   = []

        if fst is None:
            for key in snd.entries.keys():
                created.append(snd.entries[key])

        else:
            fstkeys = fst.entries.keys()
            sndkeys = snd.entries.keys()
            allkeys = set(fstkeys).union(set(sndkeys))

            for key in allkeys:
                if key not in fstkeys:
                    # key must be in self.entries and hence created
                    created.append(snd.entries[key])

                elif key not in sndkeys:
                    removed.append(fst.entries[key])
                
                elif key in sndkeys and key in fstkeys:
                    new, old = snd.entries[key], fst.entries[key]
                    if new.type == 'd' and old.type == 'd':
                        static.append(new)

                    elif new.type == 'f' and old.type == 'f':
                        if new.sha1 == old.sha1:
                            static.append(new)
                        else:
                            modified.append(new)
                    else:
                        modified.append(new)

        self.created  = created
        self.removed  = removed
        self.modified = modified
        self.static   = static

    def print_diff(self, updated_only = True):
        print('+' + '-'*78 + '+')

        if self.fst and self.snd:
            s = 'Difference Object: {} -> {}'.format(self.fst.message, self.snd.message)
        elif self.snd:
            s = 'Difference Object - New Snapshot: {}'.format(self.snd.message)
        s = '{0: ^78}'.format(s)

        print('|' + s + '|')
        print('+' + '-'*78 + '+')

        print('| created [{}]:'.format(len(self.created)))
        for o in self.created:
            print('|    ', o)
        print('| modified [{}]:'.format(len(self.modified)))
        for o in self.modified:
            print('|    ', o)
        print('| removed [{}]:'.format(len(self.removed)))
        for o in self.removed:
            print('|    ', o)

        if not updated_only:
            print('| static [{}]:'.format(len(self.static)))
            for o in self.static:
                print('|    ', o)
        print('+' + '-'*78 + '+')


class GitDirSnapshot:
    """
        GitDirSnapshot holds a snapshot of the .git directory. This is the raw
        content and has little semantic meaning without being processed by a
        GitDir instance
    """
    def __init__(self, dir_to_parse, message='', verbose=True):
        self.entries = {}
        if message:
            self.message = message
        else:
            self.message = "{}".format(datetime.now().strftime('%m/%d/%y %H:%M:%S'))
        gdp = GitDirParser(dir_to_parse, verbose)
        for entry in gdp.entries:
            self.entries[entry.name] = entry

    def parse_git_directory(self, dir_to_parse):
        pass

    def diff(self, other):
        """ assuming that self is newer than other, calculate the difference
            in the .git directory tree
        """
        pass

    def __str__(self):
        return 'Snapshot[{}]'.format(self.message)

    def __repr__(self):
        return 'Snapshot[{}] with {} entries'.format(self.message, len(self.entries))


class GitDirLog:
    """ Takes a snapshot of the .git directory """
    def __init__(self, gitdir, autodiff=True):
        """
            gitdir: directory to track
            autodiff: track diffs (and print them) automatically
        """
        self.snapshots = []
        self.gitdir = gitdir
        self.autodiff = autodiff
        self.diffs = None # Default, we don't store diffs

        if autodiff:
            self.diffs = []

    def take_snapshot(self, message='', verbose=True):
        snap = GitDirSnapshot(self.gitdir, message, verbose)
        self.snapshots.append(snap)
        if self.autodiff:
            if len(self.snapshots) > 1:
                s1,s2 = self.snapshots[-2:]
            else:
                s1, s2 = None, self.snapshots[-1]
            diff = DiffObject(s1, s2)
            self.diffs.append(diff)
            if verbose:
                diff.print_diff()

        return snap
    
    def compute_diffs(self):
        diffs = []
        if len(self.snapshots) > 0:
            s1, s2 = None, self.snapshots[-1]
            diffs = [DiffObject(s1, s2)]        # Seed initial diff
        for i in range(1, len(self.snapshots)):
            s1, s2 = self.snapshots[i-1], self.snapshots[i]
            diffs.append(DiffObject(s1, s2))
        return diffs
    
    def print_diffs(self, start=0, end=-1):
        print("-=" * 40)
        print("|                         Printing Difference Objects                          |")
        print("-=" * 40)
        for diff in self.compute_diffs()[start:end]:
            diff.print_diff()
