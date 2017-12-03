# Command Scripts

To automate the creation of Git repositories for lessons, etc, we have a basic
script that allows you to create a file system and a commit history. It is still
rudimentary right now but it should get the job done for most simple use cases.
As lessons become more advanced we will update this to accommodate nuanced use
cases.

## Example

The following is a basic example (explained below)

    touch f1
    touch f2
    touch f3

    mkdir d1
    mkdir d2
    mkdir d3

    touch d1/f1
    touch d2/f1
    touch d3/f1

    append-to-file f1 "this is the first file"
    append-to-file f2 "this is the second file"
    append-to-file f3 "this is the third file"

    add (f1,f2,f3,d1/f1,d2/f1,d3/f1)

    commit "Created some stuff"

* `touch`: this creates a file. Currently only supports a single file at a time

* `mkdir`: like touch, but creates a directory. Currently only supports a single
  directory at a time

* `append-to-file` (AKA `>>`): Append a line to a file. The line must be
  surrounded by double quotes

* `add`: This is short for `git add ...`. The arguments to be added are
  contained in a tuple

* `commit`: This represents a `git commit -m msg`. `commit` takes a single
  argument representing the message.

That's it! Some more functionality will be added as time goes on but that's all
for now.
