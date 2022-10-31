import unittest
from redditquotebot.quotes import Quote
from redditquotebot.reddit import Comment
from redditquotebot.nlp import QuoteCommentMatcher, QuoteCommentLengthMatcher


class GettingAttributes(unittest.TestCase):

    def test_accessing_members(self):
        matcher = QuoteCommentMatcher()
        self.assertEqual(matcher.score(), 0)


class TestingQuoteCommentLengthMatcher(unittest.TestCase):

    def setUp(self):
        self.quote = Quote("I had a dream!", "", [])

    def test_comment_and_quote_body_same_length(self):
        comment = Comment()
        comment.body = "I had a dream!"
        matcher = QuoteCommentLengthMatcher()
        matcher.compare(comment, self.quote)
        self.assertEqual(matcher.score(), 1)

    def test_comment_length_half_of_quote(self):
        comment = Comment()
        comment.body = "I had a"
        matcher = QuoteCommentLengthMatcher()
        matcher.compare(comment, self.quote)
        self.assertEqual(matcher.score(), 0.5)

    def test_quote_length_half_of_comment(self):
        comment = Comment()
        comment.body = "I had a dream I had a dream!"
        matcher = QuoteCommentLengthMatcher()
        matcher.compare(comment, self.quote)
        self.assertEqual(matcher.score(), 0.5)

    def test_quote_length_is_zero(self):
        comment = Comment()
        comment.body = "I had a dream I had a dream!"
        quote = Quote("", "", [])
        matcher = QuoteCommentLengthMatcher()
        matcher.compare(comment, quote)
        self.assertEqual(matcher.score(), 0.0)

    def test_comment_length_is_zero(self):
        comment = Comment()
        matcher = QuoteCommentLengthMatcher()
        matcher.compare(comment, self.quote)
        self.assertEqual(matcher.score(), 0.0)
