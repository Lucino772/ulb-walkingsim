import typing as t

import tqdm

_PROGRESSBARS: t.MutableMapping[str, tqdm.tqdm] = {}


def create_pb(__name: str, *args, **kwargs):
    global _PROGRESSBARS
    if __name in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' already exists !")

    _PROGRESSBARS[__name] = tqdm.tqdm(*args, **kwargs)
    return _PROGRESSBARS[__name]


def set_pb_desc(__name: str, desc: str):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].set_description(desc)


def refresh_pb(__name: str):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].refresh()


def update_pb(__name: str, i: int = 1):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].update(i)


def reset_pb(__name: str, new_total: int = None):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].reset(new_total)


def close_pb(__name: str):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].close()


def close_all_pb():
    for value in _PROGRESSBARS.values():
        value.close()
