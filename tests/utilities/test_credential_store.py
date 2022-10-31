import unittest
from io import StringIO
from redditquotebot.utilities import CredentialLoader, CredentialGenerator, CredentialStore
import json


class LoadingCredentialsFromJson(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_good_credentials(self):
        credentials = CredentialStore()
        credentials.reddit.user_agent = "test_user_agent"
        credentials.reddit.client_id = "test_client_id"
        credentials.reddit.client_secret = "test_client_secret"
        credentials.reddit.username = "test_username"
        credentials.reddit.password = "test_password"

        infile = StringIO()
        json.dump(credentials.to_dict(), infile, indent=2)
        infile.seek(0)

        store = CredentialLoader.from_json(infile)
        self.assertEqual(store.reddit.user_agent, "test_user_agent")
        self.assertEqual(store.reddit.client_id, "test_client_id")
        self.assertEqual(store.reddit.client_secret, "test_client_secret")
        self.assertEqual(store.reddit.username, "test_username")
        self.assertEqual(store.reddit.password, "test_password")

    def test_bad_keys(self):
        infile = StringIO()
        infile.write('{"badkey": "badvalue"}')
        infile.seek(0)
        self.assertRaises(KeyError, CredentialLoader.from_json, infile)

    def test_json_decode_error(self):
        infile = StringIO()
        infile.write('I"m not it json format')
        infile.seek(0)
        self.assertRaises(json.JSONDecodeError, CredentialLoader.from_json, infile)


class SavingCredentialToJson(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_credentials_not_provided(self):
        credentials = CredentialStore().to_dict()
        outfile = StringIO()
        CredentialGenerator.to_json(outfile)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(credentials, indent=2))

    def test_credentials_provided(self):
        credentials = CredentialStore()
        credentials.reddit.user_agent = "user_agent"
        credentials.reddit.client_id = "client_id"
        credentials.reddit.client_secret = "client_secret"
        credentials.reddit.username = "username"
        credentials.reddit.password = "password"
        outfile = StringIO()
        CredentialGenerator.to_json(outfile, credentials)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(credentials.to_dict(), indent=2))
