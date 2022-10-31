import unittest
from unittest.mock import patch
from redditquotebot import BotBuilder
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
        bot = builder.bot()
        self.assertEqual(bot.credentials, credentials)

    def testSettingCredentialsFromFile(self):
        builder = BotBuilder()
        credentials = CredentialStore()
        credentials.reddit.password = "test"
        with patch("redditquotebot.utilities.file_associator.FileAssociator.read") as read_mock:
            read_mock.return_value = credentials
            builder.credentials("filepath.json")
            read_mock.assert_called_with("filepath.json")
            self.assertEqual(builder.bot().credentials, credentials)


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
        bot = builder.bot()
        self.assertEqual(bot.configuration, configuration)

    def testSettingConfigurationFromFile(self):
        builder = BotBuilder()
        configuration = Configuration()
        configuration.reddit.subreddits = ["subreddit"]
        with patch("redditquotebot.utilities.file_associator.FileAssociator.read") as read_mock:
            read_mock.return_value = configuration
            builder.configuration("filepath.json")
            read_mock.assert_called_with("filepath.json")
            self.assertEqual(builder.bot().configuration, configuration)


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
        bot = builder.bot()
        self.assertIsInstance(bot.reddit, Reddit)


class SettingRecoredKeeping(unittest.TestCase):

    def testPassingInFile(self):
        builder = BotBuilder()
        builder.recored_keeper("path/to/file")
        bot = builder.bot()
        self.assertEqual(bot.record_keeper_file, "path/to/file")


class SettingScrapeState(unittest.TestCase):

    def testPassingInFile(self):
        builder = BotBuilder()
        builder.scrape_state("path/to/scrape")
        bot = builder.bot()
        self.assertEqual(bot.scrape_state_file, "path/to/scrape")
