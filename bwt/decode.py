from bwt import START_CHAR, END_CHAR


def decode(string: str) -> str:
    length: int = len(string)
    table: [str] = ['' for _ in range(length)]

    for _ in range(length):
        for i in range(length):
            table[i] = string[i] + table[i]
        table = sorted(table)

    return_string: str = ''
    for s in table:
        if s[0] == START_CHAR and s[-1] == END_CHAR:
            return_string = s
            break
    return return_string[1:-1]
