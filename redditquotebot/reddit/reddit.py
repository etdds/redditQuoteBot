
from redditquotebot.reddit import IReddit, RedditConnectionError
from redditquotebot.utilities import Configuration, CredentialStore
import praw


class Reddit(IReddit):
    """Interface around praw, for interacting with Reddit
    """

    def __init__(self, configuration: Configuration, credentials: CredentialStore):
        """Initialise module

        Args:
            configuration (Configuration): The configuration to use.
            credentials (CredentialStore): Credentials to use for connecting to Reddit.
        """
        super().__init__(configuration, credentials)

    def connect(self):
        """Connect to Reddit

        Raises:
            exp: An unknown exception occured. Could be one of https://praw.readthedocs.io/en/v3.6.2/pages/exceptions.html
            RedditConnectionError: The username supplied did not match that associated with praw, after connection.
        """
        try:
            self._reddit = praw.Reddit(
                user_agent=self.credentials.reddit.user_agent,
                client_id=self.credentials.reddit.client_id,
                client_secret=self.credentials.reddit.client_secret,
                username=self.credentials.reddit.username,
                password=self.credentials.reddit.password
            )
        except Exception as exp:
            raise exp from exp

        if self._reddit.user.me() != self.credentials.reddit.username:
            raise RedditConnectionError("Unexpected username occrred after connecting to Reddit.")

    def disconnect(self):
        # No special handling required
        pass
