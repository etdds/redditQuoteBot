import unittest
from redditquotebot.quotes import Quote


class UsingAccessors(unittest.TestCase):

    def test_can_print(self):
        quote = Quote("body", "ben", ["nice"])
        print(quote)


class TestingEquality(unittest.TestCase):

    def test_quote_is_equal(self):
        quote1 = Quote("body", "ben", ["nice"])
        quote2 = Quote("body", "ben", ["nice"])
        self.assertEqual(quote1, quote2)

    def test_quote_is_not_equal(self):
        quote1 = Quote("body1", "ben", ["nice"])
        quote2 = Quote("body", "ben", ["nice"])
        self.assertNotEqual(quote1, quote2)


class TestingUsingDictionaries(unittest.TestCase):

    def test_quote_from_dictionary(self):
        d = {
            "author": "ben",
            "body": "body",
            "category": ["love"]
        }
        quote = Quote.from_dict(d)
        self.assertEqual(quote.author, "ben")
        self.assertEqual(quote.category, ["love"])
        self.assertEqual(quote.body, "body")

    def test_to_dictionary(self):
        quote = Quote("body", "ben", ["nice"])
        q = quote.to_dict()
        self.assertEqual(q["author"], "ben")
        self.assertEqual(q["category"], ["nice"])
        self.assertEqual(q["body"], "body")
