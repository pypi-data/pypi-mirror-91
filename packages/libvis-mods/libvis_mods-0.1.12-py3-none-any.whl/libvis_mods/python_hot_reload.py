from importlib import reload
import time
import importlib
from watchdog import observers, events
from types import ModuleType
from loguru import logger as log

def _ismodule(mod):
    """ Module can be considered a file, it does not
    have a __path__ attribute,
    but has __name__ (which is path + name.py) """
    return hasattr(mod, '__name__')

def rreload(module):
    """Recursively reload modules."""
    log.debug('reload', module)
    if 'libvis' not in module.__file__:
        # Reload only libvis. Some packages raise recursion error
        return
    reload(module)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if type(attribute) is ModuleType:
            rreload(attribute)
    return module

class ModHotReload(events.PatternMatchingEventHandler):
    @log.catch
    def __init__(self, modname, vis, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_event = time.time()
        self._timedelta = .5
        self.modname = modname
        modules = importlib.import_module('libvis.modules.installed')

        # We may already have libvis modules in cache, 
        # so better reload them, modules/installed/__init__.py should 
        # contain import string for a new module if it was
        # installed after first import of libvis.modules.installed
        reload(modules)
        log.debug('develop: libvis modules loaded:', modules.__dict__.keys())
        mod = getattr(modules, self.modname)
        # mod can be ModuleType or Class, depending on what user 
        # choses to export
        self._exported = mod
        log.debug('develop: hot reloading module:', self._exported)

        if not isinstance(self._exported, ModuleType):
            log.info(f'develop: assuming {mod} is a class')
            parent_name = mod.__module__
            name = mod.__name__
        else:
            parent_name = 'libvis.modules.installed'
            name = modname

        self.parent = importlib.import_module(parent_name)
        self.name = name

        self.test_data = {}
        self.vis = vis
        self.set_testmod()
        log.info('develop: started')

    def on_any_event(self, event):
        if time.time() - self._last_event > self._timedelta:
            log.info('develop: Module changed', event)
            self.set_testmod()
            self._last_event = time.time()

    def set_testmod(self):
        m = self._init_mod()
        self.vis.vars.test = m

    @log.catch
    def _update_module(self):
        if not isinstance(self._exported, ModuleType):
            module = self.parent
        else:
            module = self._exported
        rreload(module)

    def _init_mod(self):
        self._update_module()
        Mod = getattr(self.parent, self.name)
        log.debug("develop: Module dict:", Mod.__dict__)
        with log.catch():
            if hasattr(Mod, "test_object"):
                m = Mod.test_object()
            else:
                try:
                    m = Mod()
                except Exception as e:
                    log.error(f"develop: Faled to initialize module {self.modname} without arguments. You may need to define 'test_object' classmethod or provide defaults for all arguments of __init__.", e)
                    return None
            #print('Fix the module, save the file, libvis will reload it for you.')
            log.debug('develop: loaded module')
            return m

def python_dev_server(modname, path):
    observer = observers.Observer()
    # -- libvis and its stopping
    libvis = importlib.import_module('libvis')
    vis = libvis.Vis(debug=True)
    _thread_stop_orig = observer.on_thread_stop
    def on_thread_stop():
        _thread_stop_orig()
        vis.stop()
    observer.on_thread_stop = on_thread_stop
    # --
    if path.is_file():
        handler = ModHotReload(modname, vis=vis, patterns=['*.py'])
        print(f"Watching {path.parent}")
        observer.schedule(handler, str(path.parent), recursive=False)
    else:
        handler = ModHotReload(modname, vis=vis)
        observer.schedule(handler, str(path), recursive=True)
    observer.start()
    return observer
