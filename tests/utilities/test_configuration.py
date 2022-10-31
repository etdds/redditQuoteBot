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
