"""Defines custom expections for the reddit module"""


class RedditConnectionError(Exception):
    """Exception called when connection to reddit is not working as expected
    """

    def __init__(self, message):
        super().__init__(message)
