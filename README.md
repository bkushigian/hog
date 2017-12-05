# HOG: Higher Order Git

HOG is a Git learning tool with an eye towards teaching how the `.git/`
directory updates as a repository evolves. A developer who uses Git on the daily
should know some of the nitty gritty details about his or her tools and we aim
to help them do just that.

## The Basics

Git is a difficult piece of software to learn and has developed quite the
reputation. The typical learning pattern is usually

1. Learn `git add` and `git commit`
2. Learn `git status`
3. Learn `push` and `pull`
4. Pull down a conflict, delete the repository, and start over again.

The issue is that after the basics there is a whole lot of information and a lot
of concepts that must be learned at the same time for Git to make sense. After
this has been done it in hindsight seems easy.

The solution, then, is to get the students to learn Git well enough that they
can teach themselves whatever they need to know; that is, _we teach them enough
to read the man pages!_ That is our goal, and to do this we focus on both the
plumbing and the porcelain of Git.

## How it works

While HOG is still under development it does have two functional modes of use.

* First is the command line client that does some setup, points itself at a Git
  repo of the user's choice, and then fires up a Python REPL with some extra
  functionality: this can be accessed with the `hog` command in the root of this
  project (this just calls into the `src/hogCLI.py` script in the `src`
  directory). 

* The second way to use HOG is to run one of the Jupyter Notebooks.  These are
  stored in `/src/notebooks` and have interactive lessons that introduce the
  student to new concepts.

## Development

This is still under development and the lessons are prototypes. Work is being
done with professors and educators to identify areas that students have the most
trouble with and try to give clear expositions on different subjects.

In addition to clarifying our pedagogical methods there is currently work being
done trying to develop a clean API that will model the Git directory.

### Development Goals

Right now we are in a prototyping phase. Enough functionality exists that we can
create basic Git repositories with a simple scripting language. This allows us
to build up lessons and provide students with a scenarios that illustrate
certain concepts. While some basic commands are implemented in the scripting
language we do not yet have a robust enough set of primitives to create all
scenarios that we would like to. Some additions would be

- `branch`: Create a new branch
- `tag`: Create a new tag
- `checkout`: Checkout a commit
- `rm`: Remove a file
- `rmdir`: Remove a directory
- `rebase`: Run `git rebase`
- `revert`: Run `git revert`
- `reset`: Run `git reset`

Additionally, the entirety of the `.git` directory is tracked in a naive manner
at each snapshot. We aim to wrap this in a mock file system to add some
semantics to the different parts of the `.git` directory. Also, while the
`index` file is currently parsed (although there are bugs in the parser) it is
worth investigating how we could parse other binary files. It is our goal to
model all players in the `.git` repo and allow the user to interact with these
in real time.

Another goal is to create a `Lesson` class that can either be used by a Jupyter
notebook or by the command line client. It would be nice to be able to group
common themed lessons together.

As far as the Jupyter notebooks are concerned, it would be nice to be able to
auto-generate parts of our notebooks and output specific Python commands based
on the current state of the program. For example, it would be great to be able
to capture the current temporary Git session location and include that in the
Markdown sections directly.

Finally, we would like to create a larger set of lessons and get feedback from
folks at different learning stages of Git.
