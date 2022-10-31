import unittest
from unittest.mock import patch
from redditquotebot import BotBuilder
from redditquotebot.quotes import QuoteDB
from redditquotebot.utilities import CredentialStore, Configuration
from redditquotebot.reddit import Reddit


class SettingUpCredentials(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSettingCredentialsFromClass(self):
        credentials = CredentialStore()
        credentials.reddit.password = "test"
        builder = BotBuilder()
        builder.credentials(credentials)
        bot = builder._bot
        self.assertEqual(bot.credentials, credentials)

    def testSettingCredentialsFromFile(self):
        builder = BotBuilder()
        credentials = CredentialStore()
        credentials.reddit.password = "test"
        with patch("redditquotebot.utilities.file_associator.FileAssociator.read") as read_mock:
            read_mock.return_value = credentials
            builder.credentials("filepath.json")
            read_mock.assert_called_with("filepath.json")
            self.assertEqual(builder._bot.credentials, credentials)


class SettingUpConfiguration(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSettingConfigurationFromClass(self):
        configuration = Configuration()
        configuration.reddit.subreddits = ["subreddit"]
        builder = BotBuilder()
        builder.configuration(configuration)
        bot = builder._bot
        self.assertEqual(bot.configuration, configuration)

    def testSettingConfigurationFromFile(self):
        builder = BotBuilder()
        configuration = Configuration()
        configuration.reddit.subreddits = ["subreddit"]
        with patch("redditquotebot.utilities.file_associator.FileAssociator.read") as read_mock:
            read_mock.return_value = configuration
            builder.configuration("filepath.json")
            read_mock.assert_called_with("filepath.json")
            self.assertEqual(builder._bot.configuration, configuration)


class SettingUpQuotes(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testQuotesFromClass(self):
        quoteDB = QuoteDB([])
        builder = BotBuilder()
        builder.quotes(quoteDB)
        bot = builder._bot
        self.assertEqual(bot.quotes, quoteDB)

    def testQuotesFromFile(self):
        builder = BotBuilder()
        quotes = QuoteDB([])
        with patch("redditquotebot.utilities.file_associator.FileAssociator.read") as read_mock:
            read_mock.return_value = quotes
            builder.quotes("filepath.csv")
            read_mock.assert_called_with("filepath.csv")
            self.assertEqual(builder._bot.quotes, quotes)


class SettingRedditInstance(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPassingInConcreteInstance(self):
        configuration = Configuration()
        configuration.reddit.subreddits = ["subreddit"]
        builder = BotBuilder()
        builder.reddit(Reddit)
        # Manually override our handlers, so files can be build
        builder._bot.record_keeper_loader["handler"] = (lambda _: (_ == _))
        builder._bot.scrape_state_loader["handler"] = (lambda _: (_ == _))
        bot = builder.bot()
        self.assertIsInstance(bot.reddit, Reddit)


class SettingRecoredKeeping(unittest.TestCase):

    def testPassingInFile(self):
        builder = BotBuilder()
        builder.recored_keeper("path/to/file.json")
        bot = builder._bot
        self.assertEqual(bot.record_keeper_loader["filepath"], "path/to/file.json")
        self.assertEqual(bot.record_keeper_storer["filepath"], "path/to/file.json")


class SettingScrapeState(unittest.TestCase):

    def testPassingInFile(self):
        builder = BotBuilder()
        builder.scrape_state("path/to/scrape.json")
        bot = builder._bot
        self.assertEqual(bot.scrape_state_loader["filepath"], "path/to/scrape.json")
        self.assertEqual(bot.scrape_state_storer["filepath"], "path/to/scrape.json")
