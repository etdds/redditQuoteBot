import unittest
from redditquotebot.quotes import Quote, QuoteAuthorFilter, QuoteLengthFilter


class TestQuoteAuthorFilter(unittest.TestCase):

    def test_quote_length_author_matches(self):
        quote1 = Quote("", "ben", [])
        quote2 = Quote("", "ben", [])
        matcher = QuoteAuthorFilter(quote1)
        equal = matcher == quote2
        not_equal = matcher != quote2
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def test_quote_length_author_doesnt_matche(self):
        quote1 = Quote("", "ben", [])
        quote2 = Quote("", "ted", [])
        matcher = QuoteAuthorFilter(quote1)
        equal = matcher == quote2
        not_equal = matcher != quote2
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)

    def test_quote_length_author_matches_string(self):
        quote = Quote("", "ben", [])
        matcher = QuoteAuthorFilter(quote)
        equal = matcher == "ben"
        not_equal = matcher != "ben"
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def test_quote_length_author_doesnt_match_string(self):
        quote = Quote("", "ben", [])
        matcher = QuoteAuthorFilter(quote)
        equal = matcher == "yo"
        not_equal = matcher != "yo"
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)


class TestQuoteLengthFilter(unittest.TestCase):

    def test_quote_length_equal(self):
        quote = Quote("1234567890", "", [])
        print(quote.body)
        matcher = QuoteLengthFilter(quote)
        self.assertEqual(matcher == 10, True)

    def test_quote_length_not_equal(self):
        quote = Quote("1234567890", "", [])
        print(quote.body)
        matcher = QuoteLengthFilter(quote)
        self.assertEqual(matcher != 9, True)

    def test_quote_length_lt(self):
        quote = Quote("1234567890", "", [])
        print(quote.body)
        matcher = QuoteLengthFilter(quote)
        self.assertEqual(matcher < 11, True)

    def test_quote_length_le(self):
        quote = Quote("1234567890", "", [])
        print(quote.body)
        matcher = QuoteLengthFilter(quote)
        self.assertEqual(matcher <= 10, True)

    def test_quote_length_gt(self):
        quote = Quote("1234567890", "", [])
        print(quote.body)
        matcher = QuoteLengthFilter(quote)
        self.assertEqual(matcher > 9, True)

    def test_quote_length_ge(self):
        quote = Quote("1234567890", "", [])
        print(quote.body)
        matcher = QuoteLengthFilter(quote)
        self.assertEqual(matcher >= 10, True)
