import unittest
from unittest.mock import patch
from redditquotebot.backtesting import combine_records, Backtester
from redditquotebot.utilities import RecordKeeper, RecordLoader
from redditquotebot.reddit import Comment, Reply
from redditquotebot.quotes import Quote
from redditquotebot.nlp import MatchedQuote, QuoteDetector, QuoteCommentLengthMatcher


class CombiningRecords(unittest.TestCase):
    def setUp(self):
        self.comments = []
        self.matches = []
        self.replies = []
        for i in range(10):
            c = Comment()
            c.uid = str(i)
            m = MatchedQuote(c, Quote("", "", []), 0)
            r = Reply(c, Quote("", "", []))
            self.comments.append(c)
            self.matches.append(m)
            self.replies.append(r)

    def test_comments_with_no_duplicates(self):
        record1 = RecordKeeper()
        record2 = RecordKeeper()
        record1.log_comments(self.comments[0:5])
        record2.log_comments(self.comments[5::])
        combined = combine_records([record1, record2]).logged_comments()
        self.assertEqual(len(combined), len(self.comments))
        self.assertEqual(self.comments, combined)

    def test_comments_with_duplicates(self):
        record1 = RecordKeeper()
        record2 = RecordKeeper()
        record1.log_comments(self.comments[0:5])
        record2.log_comments(self.comments[0:5])
        combined = combine_records([record1, record2]).logged_comments()
        self.assertEqual(len(combined), len(record1.logged_comments()))
        self.assertEqual(record1.logged_comments(), combined)

    def test_with_one_empty_comment(self):
        record1 = RecordKeeper()
        record2 = RecordKeeper()
        record1.log_comments(self.comments[0:5])
        combined = combine_records([record1, record2]).logged_comments()
        self.assertEqual(len(combined), len(record1.logged_comments()))
        self.assertEqual(record1.logged_comments(), combined)

    def test_with_two_empty_comments(self):
        record1 = RecordKeeper()
        record2 = RecordKeeper()
        combined = combine_records([record1, record2]).logged_comments()
        self.assertEqual(len(combined), 0)

    def test_matches_with_no_duplicates(self):
        record1 = RecordKeeper()
        record2 = RecordKeeper()
        record1.log_matched_quote(self.matches[0:5])
        record2.log_matched_quote(self.matches[5:10])
        combined = combine_records([record1, record2]).logged_matches()
        self.assertEqual(len(combined), len(self.matches))
        self.assertEqual(self.matches, combined)

    def test_matches_with_duplicates(self):
        record1 = RecordKeeper()
        record2 = RecordKeeper()
        record1.log_matched_quote(self.matches)
        record2.log_matched_quote(self.matches)
        combined = combine_records([record1, record2]).logged_matches()
        self.assertEqual(len(combined), len(self.matches))
        self.assertEqual(self.matches, combined)

    def test_replies_with_no_duplicates(self):
        record1 = RecordKeeper()
        record2 = RecordKeeper()
        record1.log_reply(self.replies[0:5])
        record2.log_reply(self.replies[5:10])
        combined = combine_records([record1, record2]).logged_replies()
        self.assertEqual(len(combined), len(self.replies))

    def test_replies_with_duplicates(self):
        record1 = RecordKeeper()
        record2 = RecordKeeper()
        record1.log_reply(self.replies)
        record2.log_reply(self.replies)
        combined = combine_records([record1, record2]).logged_replies()
        self.assertEqual(len(combined), len(self.replies))


class BasicBacktesting(unittest.TestCase):

    def setUp(self):
        self.quotes = [
            Quote("1234567890", "", []),
            Quote("12345", "", [])
        ]
        comment = Comment()
        comment.body = "123456789"
        self.comments = [comment]
        self.matcher = QuoteCommentLengthMatcher()
        self.backtester = Backtester(self.quotes, QuoteDetector)

    def test_no_matches(self):
        self.backtester.set_parameters(self.matcher, 1, 1, False)
        matches = self.backtester.get_matches(self.comments)
        self.assertEqual(len(matches), 0)

    def test_one_match(self):
        self.backtester.set_parameters(self.matcher, 0.8, 1, False)
        matches = self.backtester.get_matches(self.comments)
        self.assertEqual(len(matches), 1)

    def test_two_matches(self):
        self.backtester.set_parameters(self.matcher, 0.1, 2, False)
        matches = self.backtester.get_matches(self.comments)
        self.assertEqual(len(matches), 1)
        self.assertEqual(len(matches[0]), 2)
