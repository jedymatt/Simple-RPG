def strip_name_amount(arg: str):
    """

    Strip the name and the last position integer

    Args:
        arg: string

    Returns:
        string and integer with the default value 1

    """

    strings = arg.split()

    try:
        first = ' '.join(strings[:-1])
        second = int(strings[-1])
    except (ValueError, IndexError):
        first = ' '.join(strings)
        second = 1

    return first, second
