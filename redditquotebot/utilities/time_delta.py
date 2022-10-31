import time


class TimeDelta():
    """Time utility for logging progressive timestamps
    """

    def __init__(self):
        self._timestamp = time.time()

    def elapsed(self) -> float:
        """
        Get the number of seconds elapsed since the object was initialised, or the last elapsed call, whichever happened last.

        Returns:
            float: The number of seconds since the last call.
        """
        old_timestamp = self._timestamp
        self._timestamp = time.time()
        return time.time() - old_timestamp
