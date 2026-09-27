def normalize_position(position):
    """
    Convert an external position representation into the
    canonical engine representation.

    Canonical internal representation:
        (x, y)

    Supported input:
        None
        {"x": x, "y": y}
        [x, y]
        (x, y)
    """

    if position is None:
        return None

    if isinstance(position, dict):
        return (
            position["x"],
            position["y"],
        )

    if len(position) != 2:
        raise ValueError(
            f"Position must contain exactly two coordinates: {position}"
        )

    return tuple(position)