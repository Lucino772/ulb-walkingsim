import pychrono as chrono


def _tuple_to_chrono_vector(_tuple: tuple):
    if len(_tuple) != 3:
        raise RuntimeError(
            f"Cannot convert tuple[{len(_tuple)}] to chrono.ChVectorD"
        )

    return chrono.ChVectorD(_tuple[0], _tuple[1], _tuple[2])
