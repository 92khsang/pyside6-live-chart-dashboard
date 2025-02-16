from __future__ import annotations

from functools import wraps


def lock_instance_method(func):
    """Decorator to wrap instance methods with self._lock."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "_lock"):
            raise AttributeError(f"Instance {self} has no '_lock' attribute.")
        with self._lock:
            return func(self, *args, **kwargs)

    return wrapper


def lock_class_method(func):
    """Decorator to wrap class methods with cls._lock."""

    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        if not hasattr(cls, "_lock"):
            raise AttributeError(f"Class {cls.__name__} has no '_lock' attribute.")
        with cls._lock:
            return func(cls, *args, **kwargs)

    return wrapper


def lock_methods(cls):
    """Automatically wrap all suitable methods in the class with locking."""
    for attr_name, attr_value in cls.__dict__.items():
        # Skip special methods and methods marked to skip lock
        if attr_name.startswith("_") or getattr(attr_value, "__skip_lock__", False):
            continue

        if isinstance(attr_value, staticmethod):
            # Skip static methods
            continue

        if isinstance(attr_value, classmethod):
            # Wrap class methods
            wrapped = lock_class_method(attr_value.__func__)
            setattr(cls, attr_name, classmethod(wrapped))
        elif callable(attr_value):
            # Wrap instance methods
            wrapped = lock_instance_method(attr_value)
            setattr(cls, attr_name, wrapped)
    return cls


def skip_lock(func):
    """Decorator to mark a method to skip locking."""
    func.__skip_lock__ = True
    return func
