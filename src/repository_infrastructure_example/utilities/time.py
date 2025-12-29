import datetime


def get_current_time_utc() -> datetime.datetime:
    """
    Get the current time in UTC.

    :return: The current time in UTC.
    """
    return datetime.datetime.now(tz=datetime.timezone.utc)
