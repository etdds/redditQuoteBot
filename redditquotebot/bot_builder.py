from redditquotebot.reddit import IReddit
from redditquotebot.utilities import CredentialLoader, CredentialStore, FileAssociator, FileTypes, Configuration, ConfigurationLoader
from redditquotebot import RedditQuoteBot
from typing import Type, Union


class BotBuilder():
    """Helper class for building instances of a RedditQuoteBot
    """

    def __init__(self):
        self._bot = RedditQuoteBot()
        self._reddit_instance = IReddit

    def credentials(self, credentials: Union[str, CredentialStore]):
        """Provide the credentials used for the bot.

        Args:
            credentials (Union[str, CredentialStore]): Either a path to file containing the credentials, or a configured CredentailStore object
        """
        if isinstance(credentials, CredentialStore):
            self._bot.credentials = credentials
        else:
            fa = FileAssociator(
                {
                    FileTypes.JSON: CredentialLoader.from_json
                }
            )
            self._bot.credentials = fa.read(credentials)

    def configuration(self, configuration: Union[str, Configuration]):
        """Provide the configuration used for the bot.

        Args:
            configurationn (Union[str, Configuration]): Either a path to file containing the configuration, or a configured configuration object
        """
        if isinstance(configuration, Configuration):
            self._bot.configuration = configuration
        else:
            fa = FileAssociator(
                {
                    FileTypes.JSON: ConfigurationLoader.from_json
                }
            )
            self._bot.configuration = fa.read(configuration)

    def reddit(self, reddit: Type[IReddit]):
        """Set the reddit implementation to use.

        Args:
            reddit (IReddit): Concrete class implementing the IReddit interface.
        """
        self._reddit_instance = reddit

    def bot(self) -> RedditQuoteBot:
        """Get the bot with built specifications

        Returns:
            RedditQuoteBot: The configured bot instance
        """
        # Reinstate the reddit class with the actual derived class specified
        self._bot.reddit = self._reddit_instance(self._bot.configuration, self._bot.credentials)
        return self._bot
