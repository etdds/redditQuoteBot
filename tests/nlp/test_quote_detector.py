from nis import match
import unittest
from redditquotebot.quotes import Quote
from redditquotebot.reddit import Comment
from redditquotebot.nlp import MatchedQuote, QuoteDetector, QuoteCommentLengthMatcher


class MatchingComments(unittest.TestCase):
    def setUp(self):
        self.quotes = [
            Quote("1", "", []),
            Quote("12", "", []),
            Quote("as", "", []),
            Quote("123", "", []),
            Quote("1234", "", []),
            Quote("abcd", "", []),
            Quote("zxcv", "", []),
            Quote("12345", "", []),
        ]
        self.comments = []
        index = 0
        for quote in self.quotes:
            comment = Comment()
            comment.body = quote.body
            comment.uid = str(index)
            self.comments.append(comment)
            index += 1

        self.detector = QuoteDetector(self.quotes, self.comments)

    def testGettingCommentsOneMatch(self):
        matcher = QuoteCommentLengthMatcher()
        self.detector.apply(matcher, 1)
        matches = self.detector.get_matches(self.comments[3])
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[3])

    def testGettingCommentsMultiple(self):
        matcher = QuoteCommentLengthMatcher()
        self.detector.apply(matcher, 1)
        matches = self.detector.get_matches(self.comments[2])
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].quote, self.quotes[1])
        self.assertEqual(matches[1].quote, self.quotes[2])

    def testGettingCommentsMultipleLimitedToMaximum(self):
        matcher = QuoteCommentLengthMatcher()
        self.detector.apply(matcher, 1)
        matches = self.detector.get_matches(self.comments[2], 1)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[1])

    def testGettingCommentsMultipleSorted(self):
        matcher = QuoteCommentLengthMatcher()
        self.detector.apply(matcher, 0.5)
        matches = self.detector.get_matches(self.comments[2])
        self.assertEqual(len(matches), 7)

        self.detector.reset()
        self.detector.apply(matcher, 0.5)
        matches = self.detector.get_matches(self.comments[2], 2)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].quote, self.quotes[1])
        self.assertEqual(matches[1].quote, self.quotes[2])
