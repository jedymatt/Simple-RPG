def strip_name_amount(arg: str):
    strings = arg.split(' ')

    size = len(strings)
    try:
        first = strings[:size - 1]
        second = int(strings[size - 1])
    except ValueError:
        first = arg
        second = 1

    return first, second
