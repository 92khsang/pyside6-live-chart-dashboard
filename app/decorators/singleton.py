from __future__ import annotations


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:  # Check if the instance exists
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
