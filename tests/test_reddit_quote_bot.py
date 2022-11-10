from distutils.cmd import Command
import unittest
from unittest.mock import patch
from redditquotebot import BotBuilder
from redditquotebot.nlp import MatchedQuote, QuoteDetector
from redditquotebot.reddit import Reddit
from redditquotebot.utilities import CredentialStore, Configuration, RecordKeeper, ScrapeState
from redditquotebot import BotBuilder
from redditquotebot.reddit import Reddit, Comment, Reply
from redditquotebot.quotes import QuoteLoader, Quote, QuoteDB
from redditquotebot.nlp import QuoteCommentLengthMatcher


class GettingMatchingQuotes(unittest.TestCase):
    def setUp(self):
        configuration = Configuration()
        configuration.reddit.subreddits = [
            "test",
        ]
        configuration.reddit.max_comments_per_request = 100
        configuration.nlp.discard_comments_with_author = False
        self.records = RecordKeeper()
        self.quotes = QuoteDB([
            Quote("Quote 101", "", []),
            Quote("Quote 2", "", [])
        ])

        comment1 = Comment()
        comment1.body = "Comment 1"
        comment2 = Comment()
        comment1.body = "Comment 2"
        self.comments = [comment1, comment2]

        self.matcher = QuoteCommentLengthMatcher()
        self.threshold = 1.0

        builder = BotBuilder()
        builder.configuration(configuration)
        builder.credentials(CredentialStore())
        builder.quotes(self.quotes)
        builder.scrape_state(None)
        builder.recored_keeper(None)
        builder.quote_matcher(self.matcher, self.threshold)
        builder.quote_detector(QuoteDetector)
        self.bot = builder.bot()

    def tearDown(self):
        pass

    def test_get_matching_quotes(self):
        matches = self.bot.get_matching_quotes(self.comments, self.records)
        self.assertEqual(len(matches), 2)
        self.assertEqual(len(matches[0]), 1)
        self.assertEqual(len(matches[1]), 1)
        self.assertEqual(len(matches[1]), 1)
        self.assertEqual(matches[0][0].comment, self.comments[0])
        self.assertEqual(matches[0][0].quote, self.quotes[0])
        self.assertEqual(matches[1][0].comment, self.comments[1])
        self.assertEqual(matches[1][0].quote, self.quotes[0])
        self.assertEqual(len(self.records.logged_matches()), 2)

    def test_no_comments_passed(self):
        matches = self.bot.get_matching_quotes([], self.records)
        self.assertEqual(len(matches), 0)
        self.assertEqual(len(self.records.logged_matches()), 0)


class ReplyingToComments(unittest.TestCase):
    def setUp(self):
        self.records = RecordKeeper()
        builder = BotBuilder()
        builder.configuration(Configuration())
        builder.credentials(CredentialStore())
        builder.scrape_state(None)
        builder.recored_keeper(None)
        self.bot = builder.bot()

    def tearDown(self):
        pass

    def test_reply_to_comments(self):
        comment1 = Comment()
        comment1.body = "comment 1"
        comment2 = Comment()
        comment2.body = "comment 2"
        matches = [
            [
                MatchedQuote(comment1, Quote("quote 1", "", []), 0.8),
                MatchedQuote(comment1, Quote("quote 2", "", []), 0.7),
            ],
            [
                MatchedQuote(comment2, Quote("quote 2", "", []), 0.9),
                MatchedQuote(comment2, Quote("quote 1", "", []), 0.7),
            ]
        ]
        replies = self.bot.reply_to_comments(matches, 0.85,  self.records)
        self.assertEqual(len(replies), 1)
        self.assertEqual(len(self.records.logged_replies()), 1)
        self.assertEqual(replies[0].comment.body, "comment 2")
        self.assertEqual(replies[0].quote.body, "quote 2")

    def test_no_matches_passed(self):
        replies = self.bot.reply_to_comments([], 0.85, self.records)
        self.assertEqual(len(replies), 0)
        self.assertEqual(len(self.records.logged_replies()), 0)
