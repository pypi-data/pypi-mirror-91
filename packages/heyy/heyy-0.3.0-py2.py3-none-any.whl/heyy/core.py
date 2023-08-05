from functools import wraps
from os import chdir, getcwd
from pathlib import Path
from typing import Any, Optional, Iterable

from .pathtool import PathTool

pathtool = PathTool()


def with_folder(folder, create_if_not_exists=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            path = Path(folder).resolve()
            if not path.exists():
                if create_if_not_exists:
                    path.mkdir(parents=True)
                else:
                    raise ValueError(f'Folder <{path}> do not exists')
            cwd = getcwd()
            chdir(path)
            try:
                res = func(*args, **kw)
            finally:
                chdir(cwd)
            return res
        return wrapper
    return decorator


AttrNames = Iterable[str]


def reflect(obj, *, skip_callable=False, exclude: Optional[AttrNames] = None):
    exclude_attrs = set(exclude) if exclude is not None else set()
    for attr in dir(obj):
        if attr in exclude_attrs:
            continue
        if attr.startswith('__'):
            continue
        try:
            value = getattr(obj, attr)
        except Exception as e:
            value = f'[Error: <{repr(e)}>]'
        if skip_callable and callable(value):
            continue
        print(attr, value)


class DictObj:

    __reserved_attrs = frozenset(filter(lambda x: not x.startswith('__'), dir(dict)))

    def __init__(self, data: Optional[dict] = None):
        if data is None:
            data = {}
        self.__dict__.update(data)

    def __str__(self):
        return self.__dict__.__str__()

    def __repr__(self):
        return self.__dict__.__repr__()

    def __len__(self):
        return self.__dict__.__len__()

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def __setitem__(self, key, value):
        return self.__dict__.__setitem__(key, value)

    def __delitem__(self, key):
        return self.__dict__.__delitem__(key)

    def __contains__(self, item):
        return self.__dict__.__contains__(item)

    def __iter__(self):
        return iter(self.__dict__)

    def __getattr__(self, name: str):
        try:
            return getattr(self.__dict__, name)
        except AttributeError:
            pass
        return self.__getattribute__(name)

    def __setattr__(self, name: str, value):
        if name in self.__reserved_attrs:
            raise ValueError(f'Invalid attr name <{name}>')
        return super().__setattr__(name, value)


def json2obj(data: Any, *, ignore_case=False):
    dict_obj_class = DictObj if not ignore_case else CaseInsensitiveDictObj
    if isinstance(data, dict):
        data = data.copy()
        for k, v in data.items():
            data[k] = json2obj(v, ignore_case=ignore_case)
        return dict_obj_class(data)
    elif isinstance(data, list):
        data = data.copy()
        for i, v in enumerate(data):
            data[i] = json2obj(v, ignore_case=ignore_case)
        return data
    elif isinstance(data, tuple):
        return json2obj(list(data), ignore_case=ignore_case)
    else:
        return data


class CaseInsensitiveDictObj(DictObj):

    def __init__(self, data: Optional[dict] = None):
        if isinstance(data, dict):
            data = {
                (k.lower() if isinstance(k, str) else k): v
                for k, v in data.items()
            }
        super().__init__(data)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.lower()
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            key = key.lower()
        super().__setitem__(key, value)

    def __delitem__(self, key):
        if isinstance(key, str):
            key = key.lower()
        super().__delitem__(key)

    def __contains__(self, item):
        if isinstance(item, str):
            item = item.lower()
        return super().__contains__(item)

    def __getattr__(self, name: str):
        return super().__getattr__(name.lower())

    def __setattr__(self, name: str, value):
        super().__setattr__(name.lower(), value)

    def __delattr__(self, name: str) -> None:
        super().__delattr__(name.lower())
