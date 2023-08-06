"""
Dynamically created classes.
"""
import inspect
import sys
from functools import wraps
from types import ModuleType
from typing import Callable


def dynamic_class(submodule: str) -> Callable:
    """Decorator to register a dynamic class. The decorated function should
    return the dynamic class to be registered.

    Parameters
    ----------
    submodule : str
        the submodule name that the class should be registered under
        e.g. `types`

    Returns
    -------
    Callable
        decorator for dynamic class
    """

    def customized_decorator(func: Callable):
        @wraps(func)
        def decorator(*args, **kwargs):
            cls = func(*args, **kwargs)
            register_dynamic_class(cls, submodule)
            return cls

        return decorator

    return customized_decorator


def register_dynamic_class(cls: type, submodule: str):
    """
    Registers the class to the given dynamic
    submodule.
    """
    assert inspect.isclass(cls)
    module_name = f"qctrl.dynamic.{submodule}"
    cls.__module__ = module_name
    cls.__package__ = module_name

    # module exists
    if module_name in sys.modules:
        module = sys.modules[module_name]

    # create new module
    else:
        module = ModuleType(module_name)
        sys.modules[module_name] = module

    setattr(module, cls.__name__, cls)


__all__ = ["dynamic_class", "register_dynamic_class"]
