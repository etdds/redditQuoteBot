import unittest
from redditquotebot.quotes import Quote, QuoteDB, QuoteAuthorFilter


class AccessingQuotes(unittest.TestCase):
    def testByIndex(self):
        quote1 = Quote("body", "ben", ["nice"])
        quote2 = Quote("body", "henry", ["nice"])
        db = QuoteDB([quote1, quote2])
        self.assertEqual(db[0].author, "ben")
        self.assertEqual(db[1].author, "henry")

    def testByLength(self):
        quote1 = Quote("body", "ben", ["nice"])
        quote2 = Quote("body", "henry", ["nice"])
        db = QuoteDB([quote1, quote2])
        self.assertEqual(len(db), 2)


class ApplyingQuoteFilters(unittest.TestCase):
    def testByIndexAndLength(self):
        quote1 = Quote("body", "ben", ["nice"])
        quote2 = Quote("body", "henry", ["nice"])
        db = QuoteDB([quote1, quote2])
        filtered = db.apply(lambda q: QuoteAuthorFilter(q) == "ben")
        self.assertEqual(len(db), 2)
        self.assertEqual(len(filtered), 1)
