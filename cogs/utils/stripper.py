def strip_name_amount(arg: str):
    strings = arg.split()

    try:
        first = ' '.join(strings[:-1])
        second = int(strings[-1])
    except (ValueError, IndexError):
        first = ' '.join(strings)
        second = 1

    return first, second
