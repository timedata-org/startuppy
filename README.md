# startuppy

Run Python code at startup.

# Usage

`startuppy [list]` - prints the list of registered startup tasks.
`startuppy add <filename or python path> [<virtualenv>]` - add a task.
`startuppy remove <taskname>` - remove a task by name.
`startuppy run` - runs the stored tasks

Optional command line flag `--config=<filename>` to use a different
configuration file.

If `--config` is missing, the default configuration file is used, which is
probably determined by the user and the operating system.
