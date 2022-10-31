import unittest
from io import StringIO
from redditquotebot.reddit import Comment
from redditquotebot.utilities import RecordStorer, RecordLoader, RecordKeeper
import json


class UpdatingComments(unittest.TestCase):

    def test_fetching_comments_when_not_stored(self):
        records = RecordKeeper()
        self.assertEqual(len(records.logged_comments()), 0)

    def test_adding_single_comment(self):
        records = RecordKeeper()
        comment = Comment()
        records.log_comments(comment)
        self.assertEqual(len(records.logged_comments()), 1)

    def test_adding_multiple_comments(self):
        records = RecordKeeper()
        comments = [Comment(), Comment()]
        records.log_comments(comments)
        self.assertEqual(len(records.logged_comments()), 2)

    def test_adding_comments_multiple_times(self):
        records = RecordKeeper()
        comments = [Comment(), Comment()]
        seconds_comment = Comment()
        records.log_comments(comments)
        records.log_comments(seconds_comment)
        self.assertEqual(len(records.logged_comments()), 3)


class LoadingRecordsFromJSON(unittest.TestCase):

    def test_good_records(self):
        records = RecordKeeper()
        records.records = {
            "test": 12345
        }

        infile = StringIO()
        json.dump(records.to_dict(), infile, indent=2)
        infile.seek(0)

        loaded = RecordLoader.from_json(infile)
        self.assertEqual(loaded.records, {
            "test": 12345
        })

    def test_bad_keys(self):
        infile = StringIO()
        infile.write('{"badkey": "badvalue"}')
        infile.seek(0)
        self.assertRaises(KeyError, RecordLoader.from_json, infile)

    def test_json_decode_error(self):
        infile = StringIO()
        infile.write('I"m not it json format')
        infile.seek(0)
        self.assertRaises(json.JSONDecodeError, RecordLoader.from_json, infile)


class SavingRecordsToJSON(unittest.TestCase):

    def test_credentials_not_provided(self):
        records = RecordKeeper().to_dict()
        outfile = StringIO()
        RecordStorer.to_json(outfile)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(records, indent=2))

    def test_credentials_provided(self):
        records = RecordKeeper()
        records.records = {
            "test": 12345
        }
        outfile = StringIO()
        RecordStorer.to_json(outfile, records)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(records.to_dict(), indent=2))
