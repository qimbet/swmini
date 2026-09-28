def cell_to_position(cell):
    cell = cell.strip().upper()

    if len(cell) < 2:
        raise ValueError("Invalid cell ID")

    column = cell[0]
    row = cell[1:]

    if not column.isalpha() or not row.isdigit():
        raise ValueError("Invalid cell ID")

    x = ord(column) - ord("A")
    y = int(row) - 1

    return x, y


def position_to_cell(position):
    x, y = position

    if x < 0:
        raise ValueError("Invalid x coordinate")

    column = chr(ord("A") + x)
    row = y + 1

    return f"{column}{row}"