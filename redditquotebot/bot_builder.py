from redditquotebot.reddit import Reddit
from redditquotebot.utilities import *
from redditquotebot.quotes import QuoteDB, QuoteLoader
from redditquotebot.nlp import QuoteCommentMatcher, QuoteDetector
from redditquotebot import RedditQuoteBot
from typing import Type, Union, Callable


class BotBuilder():
    """Helper class for building instances of a RedditQuoteBot
    """

    def __init__(self):
        self._bot = RedditQuoteBot()
        self._quotes = QuoteDB([])
        self._quote_detector_instance = QuoteDetector

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

    def loaded_configuration(self) -> Configuration:
        """Get the instance of the loaded configuration

        The returned value is undefined if the configuration has not already been loaded with self.configuration

         Returns:
            Configuration: The configuration loaded with self.configuration
        """
        return self._bot.configuration

    def scrape_state(self, path: Union[str, None]):
        """Provide the path of the file which logs current comment logger (scraper) states.

        Args:
            path (str): Path to the file, pass None to use a RAM based scrape state.
        """
        if path is not None:
            self._bot.ram_based_scrape_state = False
            self._bot.scrape_state_loader["handler"] = self._get_scrape_state_loader()
            self._bot.scrape_state_loader["filepath"] = path
            self._bot.scrape_state_storer["handler"] = self._get_scrape_state_storer()
            self._bot.scrape_state_storer["filepath"] = path
        else:
            self._bot.ram_based_scrape_state = True

    def recored_keeper(self, path: Union[str, None]):
        """Provide the path of the file which keeps a log of comments, replies and matches for the bot

        Args:
            path (str): Path to the file. Pass None to use a RAM based scrape state
        """
        if path is not None:
            self._bot.ram_based_records = False
            self._bot.record_keeper_loader["handler"] = self._get_record_keeper_loader()
            self._bot.record_keeper_loader["filepath"] = path
            self._bot.record_keeper_storer["handler"] = self._get_record_keeper_storer()
            self._bot.record_keeper_storer["filepath"] = path
        else:
            self._bot.ram_based_records = True

    def quotes(self, quotes: Union[str, QuoteDB]):
        """Provide the path or objcet to the quote database to use

        Args:
            quotes (Union[str, QuoteDB]): Either a path to file containing the quotes, or a configured quoteDB object
        """
        if isinstance(quotes, QuoteDB):
            self._quotes = quotes
        else:
            fa = FileAssociator(
                {
                    FileTypes.CSV: QuoteLoader.from_csv
                }
            )
            self._quotes = fa.read(quotes)

    def quote_matcher(self, matcher: QuoteCommentMatcher, threshold: float):
        """Provide the matcher used to correlate comments and quotes.

        Args:
            matcher (QuoteCommentMatcher): A configured matcher to use.
            theshold (float): The threshold to use for accepting a match, between 0 and 1
        """
        self._bot.quote_matcher = matcher
        self._bot.quote_threshold = threshold

    def quote_detector(self, detector: Type[QuoteDetector]):
        """Provide the quote detector used for quotes

        Args:
            matcher (QuoteDetector): A configured matcher to use.
        """
        self._quote_detector_instance = detector

    def bot(self) -> RedditQuoteBot:
        """Get the bot with built specifications

        Returns:
            RedditQuoteBot: The configured bot instance
        """
        # Reinstate the reddit class with the actual derived class specified
        self._bot.reddit = Reddit(self._bot.configuration, self._bot.credentials)
        self._bot.detector = self._quote_detector_instance(self._quotes)

        # Create the scrape state and record keeper files if needed.
        if not self._bot.ram_based_scrape_state:
            try:
                self._bot.scrape_state_loader["handler"](self._bot.scrape_state_loader["filepath"])
            except FileNotFoundError:
                self._bot.scrape_state_storer["handler"](self._bot.scrape_state_storer["filepath"])

        if not self._bot.ram_based_records:
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
