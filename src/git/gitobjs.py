"""
    gitobjs.py represents Git atomics - commits, HEAD, index, etc.
"""
from git.git_fs import GitIndex


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
