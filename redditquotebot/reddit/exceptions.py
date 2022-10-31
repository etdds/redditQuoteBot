"""Defines custom expections for the reddit module"""


class RedditConnectionError(Exception):
    """Exception called when connection to reddit is not working as expected
    """

    def __init__(self, message):
        super().__init__(message)


class RedditReplyError(Exception):
    """Exception called when posting a reply to reddit failed.
    """

    def __init__(self, message):
        super().__init__(message)
