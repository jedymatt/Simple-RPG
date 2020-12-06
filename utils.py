from datetime import datetime, timedelta


def time_left(*, last_updated: datetime, interval):
    now = datetime.now()
    elapsed = now.timestamp() - last_updated.timestamp()
    return timedelta(seconds=interval - (elapsed % interval))


def occurrence(last_changed: datetime, interval):
    now = datetime.now()
    # elapsed = now.timestamp() - last_updated.timestamp()
    return int(now.timestamp() - last_changed.timestamp()) // interval

# time_left(last_updated=datetime.now(), interval=4)
