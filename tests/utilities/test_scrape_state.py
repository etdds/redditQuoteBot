import unittest
from io import StringIO
from redditquotebot.utilities import ScrapeStateLoader, ScrapeState, ScrapeStateStorer, scrape_state
import json


class UpdatingLatestSubredditUTC(unittest.TestCase):
    def test_updating_latest_comment_time(self):
        scrape_state = ScrapeState()
        scrape_state.update_latest_subreddit_utc("test", 1234)
        self.assertEqual(scrape_state.latest_comments["test"], 1234)
        self.assertEqual(scrape_state.latest_subreddit_utc("test"), 1234)

    def test_updating_latest_comment_time_earlier_than_previous(self):
        scrape_state = ScrapeState()
        scrape_state.update_latest_subreddit_utc("test", 1234)
        scrape_state.update_latest_subreddit_utc("test", 1111)
        self.assertEqual(scrape_state.latest_comments["test"], 1234)
        self.assertEqual(scrape_state.latest_subreddit_utc("test"), 1234)

    def test_updating_latest_comment_time_later_than_previous(self):
        scrape_state = ScrapeState()
        scrape_state.update_latest_subreddit_utc("test", 1234)
        scrape_state.update_latest_subreddit_utc("test", 2222)
        self.assertEqual(scrape_state.latest_comments["test"], 2222)
        self.assertEqual(scrape_state.latest_subreddit_utc("test"), 2222)

    def test_updating_latest_comment_same_time_as_previous(self):
        scrape_state = ScrapeState()
        scrape_state.update_latest_subreddit_utc("test", 1234)
        scrape_state.update_latest_subreddit_utc("test", 1234)
        self.assertEqual(scrape_state.latest_comments["test"], 1234)
        self.assertEqual(scrape_state.latest_subreddit_utc("test"), 1234)

    def test_query_subreddit_not_stored(self):
        scrape_state = ScrapeState()
        self.assertEqual(scrape_state.latest_subreddit_utc("test"), 0)


class LoadingStateFromJson(unittest.TestCase):

    def test_good_credentials(self):
        scrape_state = ScrapeState()
        scrape_state.latest_comments = {
            "test": 12345
        }

        infile = StringIO()
        json.dump(scrape_state.to_dict(), infile, indent=2)
        infile.seek(0)

        store = ScrapeStateLoader.from_json(infile)
        self.assertEqual(store.latest_comments, {
            "test": 12345
        })

    def test_bad_keys(self):
        infile = StringIO()
        infile.write('{"badkey": "badvalue"}')
        infile.seek(0)
        self.assertRaises(KeyError, ScrapeStateLoader.from_json, infile)

    def test_json_decode_error(self):
        infile = StringIO()
        infile.write('I"m not it json format')
        infile.seek(0)
        self.assertRaises(json.JSONDecodeError, ScrapeStateLoader.from_json, infile)


class SavingStateToJson(unittest.TestCase):

    def test_credentials_not_provided(self):
        state = ScrapeState().to_dict()
        outfile = StringIO()
        ScrapeStateStorer.to_json(outfile)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(state, indent=2))

    def test_credentials_provided(self):
        scrape_state = ScrapeState()
        scrape_state.latest_comments = {
            "test": 12345
        }
        outfile = StringIO()
        ScrapeStateStorer.to_json(outfile, scrape_state)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(scrape_state.to_dict(), indent=2))
