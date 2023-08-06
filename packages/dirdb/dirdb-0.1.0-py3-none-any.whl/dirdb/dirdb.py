
from pathlib import Path
import functools
import filelock
import pickle
import json


PROTOCOL = pickle.DEFAULT_PROTOCOL


class jsdict(dict):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__dict__ = self


@functools.total_ordering
class dbentry():
  def __init__(self, name, meta=None, pickler=pickle):
    self._meta = meta
    self._name = name  # full path name
    self.pickler = pickler

  def __enter__(self):
    self._lock = filelock.FileLock(self._suffix('lock'))
    self._lock.acquire()
    return self

  def __exit__(self, *args):
    self.update_meta()
    self._lock.release()

  def __str__(self):
    return f'dbentry({self.name})'

  def __repr__(self):
    return f"DB:{self._name.absolute()}"

  def __eq__(self, other):
    return repr(self) == repr(other)

  def __lt__(self, other):
    return repr(self) < repr(other)

  def __bool__(self):
    return self._suffix('pickle').exists()

  @property
  def name(self):
    return self._name.name

  @property
  def meta(self):
    if self._meta is None:
      js = self._suffix('json')
      if not js.is_file():
        self._meta = jsdict()
      else:
        with js.open('r') as fil:
          self._meta = jsdict(json.load(fil))

    return self._meta

  @meta.setter
  def meta(self, obj):
    if obj is None:
      js = self._suffix('json')
      if js.is_file():
        js.unlink()
      self._meta = None
    else:
      self._meta = jsdict(obj)
    self.update_meta()

  def _suffix(self, suff):
    return self._name.with_name(f"{self._name.name}.{suff}")

  def put_data(self, obj, meta=None):
    "Saves the given object into this file. Automatically updates meta as well."
    with self._suffix('pickle').open('wb') as fil:
      self.pickler.dump(obj, fil, protocol=PROTOCOL, fix_imports=False)
    if meta is not None:
      self.meta = meta
    else:
      self.update_meta()

  def update_meta(self):
    """Saves the JSON metadata to disk, if set.

    This is called automatically when setting the `.meta` attribute,
    calling `put_data()`, or going out of a `with` block scope.
    """
    if self._meta is None:
      return
    with self._suffix('json').open('w') as fil:
      json.dump(self._meta, fil)

  def get_data(self, custom_pickle=None):
    "Gets the actual data in this file."
    with self._suffix('pickle').open('rb') as fil:
      return self.pickler.load(fil)

  def has_data(self):
    return bool(self)


class dirdb():
  """Provides a database-like interface to a directory of pickled
  objects.
  """

  def __init__(self, name, create_ok=True, pickler=None):
    if not isinstance(name, Path):
      name = Path(name)
    if not name.exists() and create_ok:
      name.mkdir(parents=True)
    if not name.is_dir():
      raise ValueError(f"{name} needs to be a directory")
    self.pickler = pickler or pickle
    self.directory = name.resolve()
    assert hasattr(self.pickler, 'dump')
    assert hasattr(self.pickler, 'load')

  def __contains__(self, name):
    dest = self.directory / (name + '.pickle')
    return dest.exists()

  def __getitem__(self, name):
    pth = self.directory / name
    assert pth.name == name
    return dbentry(pth, pickler=self.pickler)

  def __setitem__(self, k, v):
    self.save(k, v)

  def __iter__(self):
    return self.entries()

  def save_data(self, name, obj, meta=None):
    "Directly save a dataset with `name`."
    with self[name] as entry:
      entry.put_data(obj, meta)

  def get_data(self, name):
    "Directly loads the dataset associated with `name`."
    with self[name] as entry:
      return entry.get_data()

  def update_meta(self, name, meta):
    "Directly update the JSON metadata of `name`."
    with self[name] as entry:
      entry.update_meta()

  def entries(self):
    "Iterates over the entries in this database (pickle files)."
    for k in self.directory.iterdir():
      if k.suffix == '.pickle':
        # Should this be locked?
        yield self[k.stem]

  def subdirs(self):
    "Iterates over sub-directories returning dirdb() instances for them."
    for k in self.directory.iterdir():
      if k.is_dir():
        # Should this be locked?
        yield self.subdb(k.name)

  def subdb(self, name, **kwargs):
    "Returns or creates a sub-directory and returns it as a dirdb() instance."
    return dirdb(self.directory / str(name), pickler=self.pickler, **kwargs)


