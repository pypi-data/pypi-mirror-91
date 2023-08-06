from os import makedirs
import os
import time
import sys
from pathlib import Path
from loguru import logger as log

from . import utils
from .python_hot_reload import python_dev_server
from .imports import (
      index_import_py , root_import_py
    , index_import_js , root_import_js
    , clean_broken_links
)

from libvis_mods.config.paths import (
    manager_path,
    web_src, web_user_mods,
    build_dir, python_user_mods
)

def _prepare_dir_struct(src, usr_mods, modname, action):
    """
    :arg src: source directory of module
    :arg usr_mods: a root directory of modules installed
    :arg modname: module name
    :arg action: copy, link or whatever function that takes src and moddir
    """
    moddir = usr_mods / modname
    #makedirs(usr_mods, exist_ok=True)
    if src.is_file():
        log.debug('Making directory {}', moddir)
        makedirs(moddir, exist_ok=True)
    action(src.absolute(), moddir)
    return moddir

def _reindex_imports():
    index_import_py(python_user_mods)
    index_import_js(web_user_mods)
    clean_broken_links(web_user_mods)
    clean_broken_links(python_user_mods)

def _process_py(modname, back_src, action=utils.copy):
    back_moddir = _prepare_dir_struct(back_src, python_user_mods, modname,
                                      action=action)
    if back_src.is_file():
        root_import_py(back_src, back_moddir)

def _process_js(modname, front_src, action=utils.copy):
    front_moddir = _prepare_dir_struct(front_src, web_user_mods, modname,
                                           action=action)
    if front_src.is_file():
        root_import_js(front_src, front_moddir)

## ## ## API ## ## ##  

def develop(modname, back_src, front_src, pre_cmd=None):
    #log.remove()
    #log.add(sys.stdout, level='DEBUG')
    utils.configure_cli_logging('DEBUG')
    back_src, front_src = Path(back_src), Path(front_src)
    try:
        _process_py(modname, back_src, action=utils.ln)
        _process_js(modname, front_src, action=utils.ln)
    except Exception as e:
        log.error(f'Error linking module {modname} {e}, rolling back.')
        uninstall(modname)
        raise
    finally:
        _reindex_imports()
    if pre_cmd:
        try:
            log.info("running pre install {}", pre_cmd)
            utils.run_cmd(pre_cmd.split())
        except Exception as e:
            log.error(f'Error running pre-install command {pre_cmd} module {modname} {e}, rolling back.')
            uninstall(modname)
            raise
        finally:
            _reindex_imports()

    log.info(f"Watching python src dir {back_src}")
    observer = python_dev_server(modname, back_src)

    log.info(f"Running webpack devolopment server from {web_src}...")

    p = os.getcwd()
    os.chdir(web_src)
    try:
        utils.run_cmd([manager_path/'develop.sh', web_src])
    except KeyboardInterrupt:
        log.debug("KeyboardInterrupt")
    except Exception as e:
        log.error("Error running webpack devolopment server {}", e)
        print('ex')
        raise
    finally:
        log.info('Stoppnig python hot reload server.')
        observer.stop()
        observer.join()
        os.chdir(p)

def install(modname, back_src, front_src,
            post_cmd=None, pre_cmd=None
           ):
    try:
        back_src, front_src = Path(back_src), Path(front_src)
        _process_py(modname, back_src, action=utils.copy)
        _process_js(modname, front_src, action=utils.copy)

        if pre_cmd:
            log.info("running pre install {}", pre_cmd)
            utils.run_cmd(pre_cmd.split())

        _reindex_imports()
        ## Build the front and copy dist
        log.info(f"Building the app from {web_src}...")
        utils.run_cmd([manager_path/'build.sh', web_src])
        utils.copy(web_src/'dist', build_dir)
        if post_cmd:
            log.info("Running post install", post_cmd)
            utils.run_cmd(post_cmd.split())
        log.info(f"Successfully installed module {modname}")
    except Exception as e:
        log.error(f'Failed to install module {modname}, rolling back.')
        uninstall(modname)
        log.error(e)
        sys.exit(1)
    finally:
        _reindex_imports()

def uninstall(modname):
    utils.rm(python_user_mods / modname)
    utils.rm(web_user_mods / modname)
    _reindex_imports()
    log.info(f"Uninstalled module {modname}")

def installed():
    try:
        import libvis.modules.installed as installed
    except Exception as e:
        print(f"Broken install: {e.__str__()}.")
        print(f"Reindexing... ", end='')
        _reindex_imports()
        print(f"OK")
        print()

    import libvis.modules.installed as installed


    return [x for x in installed.__dir__() if x[0] != '_']
