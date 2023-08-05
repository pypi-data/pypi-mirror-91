import re
import json
from docopt import docopt
from localstack import config
from localstack_ext import constants as ext_constants
from localstack_ext.bootstrap import licensing, pods_client


def cmd_login(argv, args):
    """
Usage:
  localstack login [options]

Options:
  --provider=<>           OAuth provider for login (default: github)
  --username=<>           OAuth username for login
    """
    args.update(docopt(cmd_login.__doc__.strip(), argv=argv))
    auth = import_auth()

    try:
        provider = args['--provider'] or 'github'
        auth.login(provider, args['--username'])
        print('Successfully logged in via provider: %s' % provider)
    except Exception as e:
        print('Authentication error: %s' % e)


def cmd_ci(argv, args):
    """
Usage:
  localstack ci <subcommand> [options]

Commands:
  init                  Initialize CI configuration for a new repository
  repos                 List continuous integration repositories

Options:
  --provider=<>         CI provider (default: travis)
  --repo=<>             Repository identifier
  --token=<>            API access token for CI provider
    """
    args.update(docopt(cmd_ci.__doc__.strip(), argv=argv))
    auth = import_auth()

    if args['<subcommand>'] == 'repos':
        provider = args['--provider'] or 'travis'
        result = auth.get_ci_repos(provider)
        print(result)
    elif args['<subcommand>'] == 'init':
        provider = opt_params(args, ['--provider']) or 'travis'
        repo, token = mand_params(args, ['--repo', '--token'])
        auth.init_ci_repo(repo, token, provider=provider)
        print(repo, token)


def cmd_logout(argv, args):
    """
Usage:
  localstack logout
    """
    args.update(docopt(cmd_logout.__doc__.strip(), argv=argv))
    auth = import_auth()

    auth.logout()


def cmd_config(argv, args):
    """
Usage:
  localstack config [ <key> ]
  localstack config <key> <value>

Arguments:
  <key>             Key of configuration property to read or write
  <value>           Value of configuration property to write
    """
    args.update(docopt(cmd_config.__doc__.strip(), argv=argv))
    auth = import_auth()

    if args['<value>']:
        auth.set_user_config(args['<key>'], args['<value>'])
        print('Successfully updated configuration value')
    else:
        result = auth.retrieve_user_config()
        if args['<key>']:
            all_values = result
            result = {}
            for key, value in all_values.items():
                if re.match(args['<key>'], key):
                    result[key] = value
        print(json.dumps(result, indent=4))


def cmd_daemons(argv, args):
    """
Usage:
  localstack daemons [ <subcommand> ]

Commands:
  start        Start local daemon processes
  stop         Stop local daemon processes
    """
    args.update(docopt(cmd_daemons.__doc__.strip(), argv=argv))

    from localstack_ext.bootstrap import local_daemon

    if args['<subcommand>'] in [None, 'start']:
        print('Starting local daemons processes ...')
        local_daemon.start_in_background()
    elif args['<subcommand>'] in ['stop']:
        print('Stopping local daemons processes ...')
        local_daemon.kill_servers()


def cmd_pod(argv, args):
    """
Usage:
  localstack pod <subcommand> [ <name> ]

Commands:
  push <name>      Push the state of a local cloud pod
  pull <name>      Pull the state to launch a cloud pod locally
    """
    args.update(docopt(cmd_pod.__doc__.strip(), argv=argv))

    if args['<subcommand>'] == 'push':
        print('Pushing local persistence state to server ...')
        pods_client.push_state(args['<name>'], args)
    elif args['<subcommand>'] == 'pull':
        print('Pulling persistence state from server ...')
        pods_client.pull_state(args['<name>'], args)


def cmd_status(argv, args):
    from localstack.utils.cli import print_status
    print_status()
    print('\nExtended Details:')
    print('------------------')
    print('Pro Version:\t\t%s' % ext_constants.VERSION)
    # at this point we can assume that the API key has been validated...
    print('API Key:\t\tvalidated')


def register_commands():
    config.CLI_COMMANDS['daemons'] = {
        'description': 'Manage local daemon processes',
        'parameters': [],
        'function': cmd_daemons
    }
    config.CLI_COMMANDS['pod'] = {
        'description': 'Manage state of local cloud pods',
        'parameters': [],
        'function': cmd_pod
    }
    if 'status' in config.CLI_COMMANDS:
        config.CLI_COMMANDS['status']['function'] = cmd_status

    # TODO enable commands below?
    return

    config.CLI_COMMANDS['config'] = {
        'command': '  localstack config',
        'description': 'Manage configuration values',
        'parameters': [],
        'function': cmd_config
    }
    config.CLI_COMMANDS['login'] = {
        'description': 'Log in using an external OAuth provider (e.g., Github)',
        'function': cmd_login
    }
    config.CLI_COMMANDS['logout'] = {
        'description': 'Log out and delete any session tokens',
        'function': cmd_logout
    }
    config.CLI_COMMANDS['ci'] = {
        'description': 'Manage continuous integration repositories and settings',
        'function': cmd_ci
    }


# -----------------
# HELPER FUNCTIONS
# -----------------

def import_auth():
    try:
        with licensing.prepare_environment():
            from localstack_ext.utils import auth
            return auth
    except Exception:
        raise Exception('Command not available in this version')


def mand_params(args, names=[]):
    return get_params(args, names, mandatory=True)


def opt_params(args, names=[]):
    return get_params(args, names, mandatory=False)


def get_params(args, names=[], mandatory=True):
    result = ()
    for name in names:
        value = None
        if name in args:
            value = args[name]
        if not value and mandatory:
            raise Exception('Please provide %s=... parameter' % name)
        result += (value,)
    if len(result) == 1:
        return result[0]
    return result
