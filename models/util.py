import random
from datetime import datetime, timedelta, timezone


def time_left(last_updated: datetime, interval: float) -> timedelta:
    """

    Args:
        last_updated: last updated
        interval: interval in seconds

    Returns: remaining time

    """
    now = datetime.now()
    elapsed = now - last_updated
    return timedelta(seconds=interval - (elapsed.total_seconds() % interval))


def occurrence(last_updated: datetime, interval: float) -> int:
    """

    Args:
        last_updated: last updated
        interval: interval in seconds

    Returns: number of occurrences

    """
    if interval == 0:
        return 0

    now = datetime.now(tz=timezone.utc)
    elapsed = now - last_updated
    return int(elapsed.total_seconds() // interval)


# TODO: add helper
def add_exp(character, base_exp):
    pass


def level_up(character, base_exp):
    pass


def random_boolean(chance):
    rand = random.random()
    return rand <= chance
