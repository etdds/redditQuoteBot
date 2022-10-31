import unittest
from redditquotebot.quotes import Quote, QuoteAuthorFilter


class TestQuoteAuthorFilter(unittest.TestCase):

    def testQuoteAuthorMatches(self):
        comment1 = Quote("", "ben", [])
        comment2 = Quote("", "ben", [])
        matcher = QuoteAuthorFilter(comment1)
        equal = matcher == comment2
        not_equal = matcher != comment2
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def testQuoteAuthorDoesntMatch(self):
        comment1 = Quote("", "ben", [])
        comment2 = Quote("", "ted", [])
        matcher = QuoteAuthorFilter(comment1)
        equal = matcher == comment2
        not_equal = matcher != comment2
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)

    def testQuoteAuthorMatchesString(self):
        comment1 = Quote("", "ben", [])
        matcher = QuoteAuthorFilter(comment1)
        equal = matcher == "ben"
        not_equal = matcher != "ben"
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def testQuoteAuthorDoesntMatchString(self):
        comment1 = Quote("", "ben", [])
        matcher = QuoteAuthorFilter(comment1)
        equal = matcher == "yo"
        not_equal = matcher != "yo"
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)
