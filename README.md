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
to read the man pages!_ That is our goal, and that is what we strive to do.

## How it works

While HOG is still under development it does have two functional modes of use.
First is the command line client that does some setup, points itself at a Git
repo of the user's choice, and then fires up a Python REPL with some extra
functionality: this can be accessed with the `hog` command in the root of this
project (this just calls into the `src/hogCLI.py` script). The second way to use
HOG is to run one of the Jupyter Notebooks. These are stored in `/src/notebooks`
and have interactive lessons.

## Development

This is still under development and the lessons are prototypes. Work is being
done with professors and educators to identify areas that students have the most
trouble with and try to give clear expositions on different subjects.

In addition to clarifying our pedagogical methods there is currently work being
done trying to develop a clean API that will model the Git directory.
