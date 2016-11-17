import argparse, contextlib, json, os, platform, sys

"""
https://virtualenv.pypa.io/en/latest/userguide/#using-virtualenv-without-bin-python
https://stackoverflow.com/questions/436198
"""

def add(args):
    if not args.task:
        raise ValueError('add command needs a task')
    args.tasks.append(args.task)
    open(args.config, 'w').writelines(t + '\n' for t in args.tasks)


def list_tasks(args):
    print(*args.tasks, sep='\n')

def remove(args):
    if not args.task:
        raise ValueError('remove command needs a task')



COMMANDS = dict(
    add=add,
    list=list_tasks,
    remove=remove,
    run=run,
    )

PARSER = argparse.ArgumentParser(description='Run Python tasks on startup.')
PARSER.add_argument('command', choices=COMMANDS.keys(), default='help')
PARSER.add_argument('task', default='')
PARSER.add_argument('--config', '-c', default=default_config_file())
PARSER.add_argument('--force', '-f', default='store_true')

# TODO: where to put this?
USAGE = """USAGE:
  startuppy [help] - prints this message.
  startuppy add <filename or python path>[:<virtualenv>] - add a task.
  startuppy list - prints the list of registered startup tasks.
  startuppy remove <filename or python path>[:[<virtualenv>]] - remove a task by name.
  startuppy run - runs the stored tasks.

  The optional --config allows you to select a configuration file.
"""

def is_root():
    # https://stackoverflow.com/questions/2806897
    return os.getenv('HOME') == '/root'


def default_config_file():
    d = '/etc' if is_root() else os.path.expanduser('~/.config')
    return os.path.join(d, 'startuppy.conf')


def canonicalize_filename(name):
    return os.path.abspath(os.path.expanduser(name))


def check_exists(name, prompt=True):
    if not os.path.exists(name):
        if prompt:
            ch = raw_input('File %s doesn\'t exist. Continue? (yN) ' % name)
            if ch.lower().startswith('y'):
                return
        raise ValueError('File not found %s' % name)


def add(args):
    if not 1 <= len(args) <= 2:
        raise ValueError('`startuppy add` takes just one or two arguments.')
    executable = canonicalize_file(args[0])
    if len(args) == 1:
        virtualenv = ''

    elif len(args) == 2:

    else:
    executable, virtualenv = args

    if executable.endswith('.py'):
    else:
        # Do a bit of validation of a Python path - we can't just load the
        # symbol because we probably aren't in the right virtualenv.
        if not all(p.isidentifier() for p in executable.split('.')):
            raise ValueError('%s is not a valid Python executable path')

    name = '%s:%s' % (executable, virtualenv)) if virtualenv else executable
    if name in config:
        raise ValueError('Task %s has already been added.' % name)
    config.append(name)


def list_s(_, config):
    print(*config, sep='\n')
    if args:
        print('WARNING: list takes no arguments')


def startuppy(args):
    filename, command, task = parse_args(args)

    def add(executable):
        executable = canonicalize_file(task)
        if len(args) == 1:
            virtualenv = ''

        elif len(args) == 2:

        else:
        executable, virtualenv = args

        if executable.endswith('.py'):
        else:
            # Do a bit of validation of a Python path - we can't just load the
            # symbol because we probably aren't in the right virtualenv.
            if not all(p.isidentifier() for p in executable.split('.')):
                raise ValueError('%s is not a valid Python executable path')

        name = '%s:%s' % (executable, virtualenv)) if virtualenv else executable
        if name in config:
            raise ValueError('Task %s has already been added.' % name)
        config.append(name)

    def error():
        print(USAGE)
        raise ValueError('Unknown command %s' % command)

    original_config = config[:]
    COMMANDS.get(command, error)(config, args)
    if config != original_config:
        open(filename, 'w').writelines(c + '\n' for c in config)


def startuppy():
    args = PARSER.parse_args()
    if args.task:
        args.executable, *rest = args.task.split(':', 1)
        args.virtualenv = (rest and rest[0]) or ''

        if '/' in args.executable:
            args.executable = canonicalize_filename(args.executable)
            check_exists(args.executable)

        else:
            if not all(p.isidentifier() for p in args.executable.split('.')):
                raise ValueError('%s is not a valid Python executable path')

        args.task = args.executable
        if args.virtualenv:
            args.task += ':' + args.virtualenv

    try:
        args.tasks = [i.strip() for i in open(args.config)]
    except:
        args.tasks = []

    COMMANDS[args.command](args)


if __name__ == '__main__':
    startuppy()
