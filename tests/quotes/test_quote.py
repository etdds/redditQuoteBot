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
