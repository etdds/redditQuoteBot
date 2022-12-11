import unittest
from io import StringIO
from redditquotebot.utilities import ConfigurationLoader, Configuration, ConfigurationGenerator
import json


class LoadingCredentialsFromJson(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_good_configuration(self):
        config = Configuration()
        config.reddit.subreddits = ["test", "me"]
        config.reddit.new_submissions_per_request = 5

        infile = StringIO()
        json.dump(config.to_dict(), infile, indent=2)
        infile.seek(0)

        store = ConfigurationLoader.from_json(infile)
        self.assertEqual(store.reddit.subreddits, ["test", "me"])
        self.assertEqual(store.reddit.new_submissions_per_request, 5)

    def test_bad_keys(self):
        infile = StringIO()
        infile.write('{"badkey": "badvalue"}')
        infile.seek(0)
        self.assertRaises(KeyError, ConfigurationLoader.from_json, infile)

    def test_json_decode_error(self):
        infile = StringIO()
        infile.write('I"m not it json format')
        infile.seek(0)
        self.assertRaises(json.JSONDecodeError, ConfigurationLoader.from_json, infile)


class SavingCredentialToJson(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_configuration_not_provided(self):
        configuration = Configuration().to_dict()
        outfile = StringIO()
        ConfigurationGenerator.to_json(outfile)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(configuration, indent=2))

    def test_configuration_provided(self):
        config = Configuration()
        config.reddit.subreddits = ["test"]
        config.reddit.new_submission_per_request = 5
        outfile = StringIO()
        ConfigurationGenerator.to_json(outfile, config)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(config.to_dict(), indent=2))


class CheckAllCredential(unittest.TestCase):

    def test_all(self):
        config = Configuration()
        config.reddit.subreddits = ["test"]
        config.reddit.new_submissions_per_request = 5
        config.reddit.max_comments_per_request = 100
        config.reddit.minimum_comment_length = 200
        config.bot.reply_to_comments = True
        config.bot.matched_quotes_to_log = 1
        config.bot.reply_threshold = 0.1
        config.bot.remove_own_comments = False
        config.bot.remove_comment_threshold = -10
        config.nlp.match_store_threshold = 0.2
        config.nlp.quote_comment_length_delta = 0.1
        config.nlp.minimum_comment_sentence_word_length = 2
        config.nlp.quote_length_bonus_coefficient = 5
        config.nlp.quote_length_bonus_start = 0
        config.nlp.quote_length_bonus_end = 20
        config.nlp.matched_sentence_coefficient = 1
        config.nlp.discard_comments_with_author = False
        config.records.maximum_comment_count = 0
        config.records.maximum_match_count = None
        config.records.maximum_reply_count = 100
        config.records.maximum_removed_comment_count = 8

        outfile = StringIO()
        ConfigurationGenerator.to_json(outfile, config)
        outfile.seek(0)
        loaded = ConfigurationLoader.from_json(outfile)

        self.assertEqual(loaded.reddit.subreddits, ["test"])
        self.assertEqual(loaded.reddit.new_submissions_per_request, 5)
        self.assertEqual(loaded.reddit.max_comments_per_request, 100)
        self.assertEqual(loaded.reddit.minimum_comment_length, 200)
        self.assertEqual(loaded.bot.reply_to_comments, True)
        self.assertEqual(loaded.bot.reply_threshold, 0.1)
        self.assertEqual(loaded.bot.matched_quotes_to_log, 1)
        self.assertEqual(loaded.bot.remove_own_comments, False)
        self.assertEqual(loaded.bot.remove_comment_threshold, -10)
        self.assertEqual(loaded.nlp.match_store_threshold, 0.2)
        self.assertEqual(loaded.nlp.quote_comment_length_delta, 0.1)
        self.assertEqual(loaded.nlp.minimum_comment_sentence_word_length, 2)
        self.assertEqual(loaded.nlp.quote_length_bonus_coefficient, 5)
        self.assertEqual(loaded.nlp.quote_length_bonus_start, 0)
        self.assertEqual(loaded.nlp.quote_length_bonus_end, 20)
        self.assertEqual(loaded.nlp.matched_sentence_coefficient, 1)
        self.assertEqual(loaded.nlp.discard_comments_with_author, False)
        self.assertEqual(loaded.records.maximum_comment_count, 0)
        self.assertEqual(loaded.records.maximum_match_count, None)
        self.assertEqual(loaded.records.maximum_reply_count, 100)
        self.assertEqual(loaded.records.maximum_removed_comment_count, 8)
