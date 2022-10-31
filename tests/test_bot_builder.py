import unittest
from unittest.mock import patch
from redditquotebot import BotBuilder
from redditquotebot.utilities import CredentialStore, Configuration


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
