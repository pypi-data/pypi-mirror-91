""" Cli interface for libvis modules and dev """
import click
import libvis_mods

from libvis_mods.config import with_libvis_config
from libvis_mods.publish import publish
from libvis_mods.utils import only_required_kwargs_call, configure_cli_logging
from libvis_mods.download import repository
from loguru import logger as log

from libvis_mods.config.paths import (
    web_user_mods, python_user_mods
)


@click.group()
def cli():
    configure_cli_logging('INFO')

name = click.argument('modname', required=False)
back = click.argument('back_src'
                      , type=click.Path(exists=True), required=False)
front = click.argument('front_src'
                       , type=click.Path(exists=True), required=False)

files = lambda x: back( front(
    with_libvis_config(x)
))


## ## ## User ## ## ##

@cli.command()
@name
@files
def install(*args, **kwargs):
    """ Install a module from directory.

        Arguments can be omitted if the command is run
        in a directory with libvis-mod.conf
    """
    log.debug('install arguments: {}', kwargs)
    if any([
        'modname' not in kwargs,
        'front_src' not in kwargs,
        'back_src' not in kwargs
    ]):
        log.error('Please provide install arguments, `libvis-mods install --help`, or run in a directory with libvis-mod.conf')
        return 1

    return only_required_kwargs_call(
        libvis_mods.install, *args, **kwargs)


@cli.command('list')
def list_():
    """ list installed modules """
    mods = libvis_mods.installed()
    print("\n".join(mods))

@cli.command()
@name
def uninstall(**kwargs):
    """ Uninstall module """
    return libvis_mods.uninstall(kwargs['modname'])

## ## ## Utils ## ## ##

@cli.command()
@click.option('-o', '--output-dir', 'output_dir', default='.')
@click.argument('source')
def download(source, output_dir):
    """ Download source for the module into ./`module_name`"""
    repository.determine_repo_dir(source, output_dir)

@cli.command()
@click.option('--front', 'request', flag_value='front')
@click.option('--back', 'request', flag_value='back')
@click.option('--both', 'request', flag_value='both', default=True)
def where(request):
    """ Prints locations of where modules are installed """
    if request == 'back':
        print(python_user_mods.absolute())
    elif request == 'front':
        print(web_user_mods.absolute())
    else:
        print('back: {}'.format(python_user_mods))
        print('front: {}'.format(web_user_mods))

## ## ## Developer ## ## ##

@cli.command()
@name
@files
def develop(*args, **kwargs):
    """ Run the web server in development mode with hot reload """
    log.debug("debug args={}  kwargs={}",args, kwargs)
    return only_required_kwargs_call(
        libvis_mods.develop, *args, **kwargs)


@cli.command()
@click.option('-o', '--output-dir', 'output_dir', default='.')
@name
def init_file(modname, output_dir):
    libvis_mods.init_file(modname, output_dir=output_dir)

@cli.command()
@click.option('-o', '--output-dir', 'output_dir', default='.')
@name
def init_dir(modname, output_dir):
    libvis_mods.init_dir(modname, output_dir=output_dir)


cli.command()(publish)

if __name__ == '__main__':
    cli()
