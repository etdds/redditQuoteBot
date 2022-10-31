from redditquotebot.reddit import IReddit
from redditquotebot.utilities import *
from redditquotebot.quotes import QuoteDB, QuoteLoader
from redditquotebot import RedditQuoteBot, QuoteCommentMatcher
from typing import Type, Union, Callable


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

    def scrape_state(self, path: str):
        """Provide the path of the file which logs current comment logger (scraper) states.

        Args:
            path (str): Path to the file
        """
        self._bot.scrape_state_loader["handler"] = self._get_scrape_state_loader()
        self._bot.scrape_state_loader["filepath"] = path
        self._bot.scrape_state_storer["handler"] = self._get_scrape_state_storer()
        self._bot.scrape_state_storer["filepath"] = path

    def recored_keeper(self, path: str):
        """Provide the path of the file which keeps a log of comments, replies and matches for the bot

        Args:
            path (str): Path to the file
        """
        self._bot.record_keeper_loader["handler"] = self._get_record_keeper_loader()
        self._bot.record_keeper_loader["filepath"] = path
        self._bot.record_keeper_storer["handler"] = self._get_record_keeper_storer()
        self._bot.record_keeper_storer["filepath"] = path

    def quotes(self, quotes: Union[str, QuoteDB]):
        """Provide the path or objcet to the quote database to use

        Args:
            quotes (Union[str, QuoteDB]): Either a path to file containing the quotes, or a configured quoteDB object
        """
        if isinstance(quotes, QuoteDB):
            self._bot.quotes = quotes
        else:
            fa = FileAssociator(
                {
                    FileTypes.CSV: QuoteLoader.from_csv
                }
            )
            self._bot.quotes = fa.read(quotes)

    def quote_comment_matcher(self, matcher: QuoteCommentMatcher):
        self._bot.matcher = matcher

    def bot(self) -> RedditQuoteBot:
        """Get the bot with built specifications

        Returns:
            RedditQuoteBot: The configured bot instance
        """
        # Reinstate the reddit class with the actual derived class specified
        self._bot.reddit = self._reddit_instance(self._bot.configuration, self._bot.credentials)

        # Create the scrape state and record keeper files if needed.
        try:
            self._bot.scrape_state_loader["handler"](self._bot.scrape_state_loader["filepath"])
        except FileNotFoundError:
            self._bot.scrape_state_storer["handler"](self._bot.scrape_state_storer["filepath"])

        try:
            self._bot.record_keeper_loader["handler"](self._bot.record_keeper_loader["filepath"])
        except FileNotFoundError:
            self._bot.record_keeper_storer["handler"](self._bot.record_keeper_storer["filepath"])

        return self._bot

    def _get_scrape_state_loader(self) -> Callable:
        fa = FileAssociator(
            {
                FileTypes.JSON: ScrapeStateLoader.from_json
            }
        )
        return fa.read

    def _get_scrape_state_storer(self) -> Callable:
        fa = FileAssociator(
            {
                FileTypes.JSON: ScrapeStateStorer.to_json
            }
        )
        return fa.write

    def _get_record_keeper_loader(self) -> Callable:
        fa = FileAssociator(
            {
                FileTypes.JSON: RecordLoader.from_json
            }
        )
        return fa.read

    def _get_record_keeper_storer(self) -> Callable:
        fa = FileAssociator(
            {
                FileTypes.JSON: RecordStorer.to_json
            }
        )
        return fa.write
