import unittest
from redditquotebot.quotes import Quote


class UsingAccessors(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCanCallPrint(self):
        quote = Quote("body", "ben", ["nice"])
        print(quote)

    def testRetrieveAsDictionary(self):
        quote = Quote("body", "ben", ["nice"])
        q = quote.to_dict()
        self.assertEqual(q["author"], "ben")
        self.assertEqual(q["category"], ["nice"])
        self.assertEqual(q["body"], "body")


class TestingEquality(unittest.TestCase):

    def testQuoteIsEqual(self):
        quote1 = Quote("body", "ben", ["nice"])
        quote2 = Quote("body", "ben", ["nice"])
        self.assertEqual(quote1, quote2)

    def testQuoteIsNotEqual(self):
        quote1 = Quote("body1", "ben", ["nice"])
        quote2 = Quote("body", "ben", ["nice"])
        self.assertNotEqual(quote1, quote2)
