"""Provide mechanism to broadcast imports from master to other processes.

This reduces file system strain.

Use:

  with broadcast_imports():
      <execute import statements>

This temporarily overrides the Python import mechanism so that

  1) master executes and caches import metadata and code
  2) import metadata and code are broadcast to all processes
  3) other processes execute the import statements from memory

Warning: Do not perform any parallel operations while broadcast imports
are enabled.  Non-master processes assume that they will receive module
data and will crash or deadlock if master sends anything else.
"""


import os
import sys
import marshal
import importlib
import importlib.util
from importlib.machinery import PathFinder, ModuleSpec

import _gpaw


if hasattr(_gpaw, 'Communicator'):
    if '_gpaw' not in sys.builtin_module_names:
        libmpi = os.environ.get('GPAW_MPI', 'libmpi.so')
        import ctypes
        try:
            ctypes.CDLL(libmpi, ctypes.RTLD_GLOBAL)
        except OSError:
            pass
    world = _gpaw.Communicator()
else:
    world = None  # type: ignore


def marshal_broadcast(obj):
    if world.rank == 0:
        buf = marshal.dumps(obj)
    else:
        assert obj is None
        buf = None

    buf = _gpaw.globally_broadcast_bytes(buf)
    try:
        return marshal.loads(buf)
    except ValueError as err:
        msg = ('Parallel import failure -- probably received garbage.  '
               'Error was: {}.  This may happen if parallel operations are '
               'performed while parallel imports are enabled.'.format(err))
        raise ImportError(msg)


class BroadcastLoader:
    def __init__(self, spec, module_cache):
        self.module_cache = module_cache
        self.spec = spec

    def load_module(self, fullname):
        if world.rank == 0:
            # Load from file and store in cache:
            code = self.spec.loader.get_code(fullname)
            metadata = (self.spec.submodule_search_locations, self.spec.origin)
            self.module_cache[fullname] = (metadata, code)
            # We could execute the default mechanism to load the module here.
            # Instead we load from cache using our own loader, like on the
            # other cores.

        return self.load_from_cache(fullname)

    def load_from_cache(self, fullname):
        metadata, code = self.module_cache[fullname]
        module = importlib.util.module_from_spec(self.spec)
        origin = metadata[1]
        module.__file__ = origin
        # __package__, __path__, __cached__?
        module.__loader__ = self
        sys.modules[fullname] = module
        exec(code, module.__dict__)
        return module

    def __str__(self):
        return ('<{} for {}:{} [{} modules cached]>'
                .format(self.__class__.__name__,
                        self.spec.name, self.spec.origin,
                        len(self.module_cache)))


class BroadcastImporter:
    def __init__(self):
        self.module_cache = {}
        self.cached_modules = []

    def find_spec(self, fullname, path=None, target=None):
        if world.rank == 0:
            spec = PathFinder.find_spec(fullname, path, target)
            if spec is None:
                return None

            if spec.loader is None:
                return None

            code = spec.loader.get_code(fullname)
            if code is None:  # C extensions
                return None

            loader = BroadcastLoader(spec, self.module_cache)
            assert fullname == spec.name

            searchloc = spec.submodule_search_locations
            spec = ModuleSpec(fullname, loader, origin=spec.origin,
                              is_package=searchloc is not None)
            if searchloc is not None:
                spec.submodule_search_locations += searchloc
            return spec
        else:
            if fullname not in self.module_cache:
                # Could this in principle interfere with builtin imports?
                return PathFinder.find_spec(fullname, path, target)

            searchloc, origin = self.module_cache[fullname][0]
            loader = BroadcastLoader(None, self.module_cache)
            spec = ModuleSpec(fullname, loader, origin=origin,
                              is_package=searchloc is not None)
            if searchloc is not None:
                spec.submodule_search_locations += searchloc
            loader.spec = spec  # XXX loader.loader is still None
            return spec

    def broadcast(self):
        if world.rank == 0:
            # print('bcast {} modules'.format(len(self.module_cache)))
            marshal_broadcast(self.module_cache)
        else:
            self.module_cache = marshal_broadcast(None)
            # print('recv {} modules'.format(len(self.module_cache)))

    def enable(self):
        if world is None:
            return

        # There is the question of whether we lose anything by inserting
        # ourselves further on in the meta_path list.  Maybe not, and maybe
        # that is a less violent act.
        sys.meta_path.insert(0, self)
        if world.rank != 0:
            self.broadcast()

    def disable(self):
        if world is None:
            return

        if world.rank == 0:
            self.broadcast()
        self.cached_modules += self.module_cache.keys()
        self.module_cache = {}
        myself = sys.meta_path.pop(0)
        assert myself is self

    def __enter__(self):
        self.enable()

    def __exit__(self, *args):
        self.disable()


broadcast_imports = BroadcastImporter()
