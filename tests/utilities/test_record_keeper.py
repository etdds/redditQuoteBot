import unittest
from io import StringIO
from urllib.parse import quote_plus
from redditquotebot.reddit import Comment, Reply
from redditquotebot.utilities import RecordStorer, RecordLoader, RecordKeeper
from redditquotebot.nlp import MatchedQuote
from redditquotebot.quotes import Quote
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

    def test_adding_comments_no_comment_limit(self):
        records = RecordKeeper()
        comments = [Comment(), Comment(), Comment(), Comment()]
        records.log_comments(comments)
        records.log_comments(comments)
        self.assertEqual(len(records.logged_comments()), 8)

    def test_adding_comments_with_comment_limit(self):
        records = RecordKeeper()
        records.maximum_comments(3)
        comments = [Comment(), Comment(), Comment(), Comment()]
        records.log_comments(comments)
        records.log_comments(comments)
        self.assertEqual(len(records.logged_comments()), 3)

    def test_adding_comments_with_no_comments_allowed(self):
        records = RecordKeeper()
        records.maximum_comments(0)
        comments = [Comment(), Comment(), Comment(), Comment()]
        records.log_comments(comments)
        records.log_comments(comments)
        self.assertEqual(len(records.logged_comments()), 0)

    def test_adding_comments_capping_limit(self):
        records = RecordKeeper()
        comments = [Comment(), Comment(), Comment(), Comment()]
        records.log_comments(comments)
        records.log_comments(comments)
        records.maximum_comments(2)
        self.assertEqual(len(records.logged_comments()), 2)


class RetrievingComments(unittest.TestCase):

    def setUp(self) -> None:
        self.records = RecordKeeper()
        self.comment = Comment()
        self.comment.body = "body"
        self.records.log_comments(self.comment)

    def test_retreive_comment_type_and_contents(self):
        comments = self.records.logged_comments()
        self.assertIsInstance(comments, list)
        self.assertIsInstance(comments[0], Comment)
        self.assertEqual(comments[0].body, "body")


class UpdatingMatches(unittest.TestCase):

    def test_fetching_matches_when_not_stored(self):
        records = RecordKeeper()
        self.assertEqual(len(records.logged_matches()), 0)

    def test_adding_single_match(self):
        records = RecordKeeper()
        match = MatchedQuote(Comment(), Quote("", "", []), 0.5)
        records.log_matched_quote(match)
        self.assertEqual(len(records.logged_matches()), 1)

    def test_adding_multiple_matches(self):
        records = RecordKeeper()
        match = MatchedQuote(Comment(), Quote("", "", []), 0.5)
        records.log_matched_quote([match, match])
        self.assertEqual(len(records.logged_matches()), 2)

    def test_adding_matches_multiple_times(self):
        records = RecordKeeper()
        match = MatchedQuote(Comment(), Quote("", "", []), 0.5)
        matches = [match, match]
        seconds_match = match
        records.log_matched_quote(matches)
        records.log_matched_quote(seconds_match)
        self.assertEqual(len(records.logged_matches()), 3)

    def test_adding_matches_mo_match_limit(self):
        records = RecordKeeper()
        match = MatchedQuote(Comment(), Quote("", "", []), 0.5)
        matches = [match, match, match, match]
        records.log_matched_quote(matches)
        records.log_matched_quote(matches)
        self.assertEqual(len(records.logged_matches()), 8)

    def test_adding_matches_with_match_limit(self):
        records = RecordKeeper()
        records.maximum_matches(3)
        match = MatchedQuote(Comment(), Quote("", "", []), 0.5)
        matches = [match, match, match, match]
        records.log_matched_quote(matches)
        records.log_matched_quote(matches)
        self.assertEqual(len(records.logged_matches()), 3)

    def test_adding_matches_with_no_matches_allowed(self):
        records = RecordKeeper()
        records.maximum_matches(0)
        match = MatchedQuote(Comment(), Quote("", "", []), 0.5)
        matches = [match, match, match, match]
        records.log_matched_quote(matches)
        records.log_matched_quote(matches)
        self.assertEqual(len(records.logged_matches()), 0)

    def test_adding_matches_capping_limit(self):
        records = RecordKeeper()
        match = MatchedQuote(Comment(), Quote("", "", []), 0.5)
        matches = [match, match, match, match]
        records.log_matched_quote(matches)
        records.maximum_matches(2)
        self.assertEqual(len(records.logged_matches()), 2)


class RetrievingMatches(unittest.TestCase):

    def setUp(self) -> None:
        self.records = RecordKeeper()
        self.match = MatchedQuote(Comment(), Quote("", "", []), 0.5)
        self.records.log_matched_quote(self.match)

    def test_retreive_match_type_and_contents(self):
        matches = self.records.logged_matches()
        self.assertIsInstance(matches, list)
        self.assertIsInstance(matches[0], MatchedQuote)
        self.assertEqual(matches[0].score, 0.5)


class UpdatingReplies(unittest.TestCase):

    def test_fetching_replies_when_not_stored(self):
        records = RecordKeeper()
        self.assertEqual(len(records.logged_replies()), 0)

    def test_adding_single_reply(self):
        reply = Reply(Comment(), Quote("", "", []))
        records = RecordKeeper()
        records.log_reply(reply)
        self.assertEqual(len(records.logged_replies()), 1)

    def test_adding_multiple_replies(self):
        reply = Reply(Comment(), Quote("", "", []))
        records = RecordKeeper()
        records.log_reply([reply, reply])
        self.assertEqual(len(records.logged_replies()), 2)

    def test_adding_replies_multiple_times(self):
        records = RecordKeeper()
        reply = Reply(Comment(), Quote("", "", []))
        replies = [reply, reply]
        second_reply = reply
        records.log_reply(replies)
        records.log_reply(second_reply)
        self.assertEqual(len(records.logged_replies()), 3)

    def test_adding_replies_no_limit(self):
        records = RecordKeeper()
        reply = Reply(Comment(), Quote("", "", []))
        replies = [reply, reply, reply, reply]
        records.log_reply(replies)
        records.log_reply(replies)
        self.assertEqual(len(records.logged_replies()), 8)

    def test_adding_matches_with_match_limit(self):
        records = RecordKeeper()
        records.maximum_replies(3)
        reply = Reply(Comment(), Quote("", "", []))
        replies = [reply, reply, reply, reply]
        records.log_reply(replies)
        records.log_reply(replies)
        self.assertEqual(len(records.logged_replies()), 3)

    def test_adding_matches_with_no_matches_allowed(self):
        records = RecordKeeper()
        records.maximum_replies(0)
        reply = Reply(Comment(), Quote("", "", []))
        replies = [reply, reply, reply, reply]
        records.log_reply(replies)
        records.log_reply(replies)
        self.assertEqual(len(records.logged_replies()), 0)

    def test_adding_matches_capping_limit(self):
        records = RecordKeeper()
        reply = Reply(Comment(), Quote("", "", []))
        replies = [reply, reply, reply, reply]
        records.log_reply(replies)
        records.log_reply(replies)
        records.maximum_replies(2)
        self.assertEqual(len(records.logged_replies()), 2)


class RetrievingQuotes(unittest.TestCase):

    def setUp(self) -> None:
        self.records = RecordKeeper()
        self.reply = Reply(Comment(), Quote("body", "", []))
        self.records.log_reply(self.reply)

    def test_retreive_reply_type_and_contents(self):
        replies = self.records.logged_replies()
        self.assertIsInstance(replies, list)
        self.assertIsInstance(replies[0], Reply)
        self.assertEqual(replies[0].quote.body, "body")


class GettingDict(unittest.TestCase):

    def test_to_dict(self):
        records = RecordKeeper()
        d = records.to_dict()["records"]
        self.assertEqual(len(d["comments"]), 0)
        self.assertEqual(len(d["matches"]), 0)
        self.assertEqual(len(d["replies"]), 0)


class LoadingRecordsFromJSON(unittest.TestCase):

    def test_good_records(self):
        records = RecordKeeper()
        infile = StringIO()
        json.dump(records.to_dict(), infile, indent=2)
        infile.seek(0)

        loaded = RecordLoader.from_json(infile)
        self.assertEqual(loaded.records, records.to_dict()["records"])

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

    def test_records_not_provided(self):
        records = RecordKeeper().to_dict()
        outfile = StringIO()
        RecordStorer.to_json(outfile)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(records, indent=2))

    def test_records_provided(self):
        records = RecordKeeper()
        outfile = StringIO()
        RecordStorer.to_json(outfile, records)
        outfile.seek(0)
        self.assertEqual(outfile.read(), json.dumps(records.to_dict(), indent=2))
