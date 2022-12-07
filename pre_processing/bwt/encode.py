from pre_processing.bwt import START_CHAR, END_CHAR


def encode(string: str) -> str:
    string: str = '{}{}{}'.format(START_CHAR, string, END_CHAR)
    length: int = len(string)

    table: [str] = []

    # get rotations
    for i in range(length):
        rotated: str = string[i:] + string[:i]
        table.append(rotated)

    table = sorted(table)
    last_column = ''.join([x[-1] for x in table])

    return last_column
