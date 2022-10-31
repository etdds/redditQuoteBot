import unittest
from redditquotebot.quotes import Quote
from redditquotebot.reddit import Comment
from redditquotebot.nlp import MatchedQuote


class GettingAttributes(unittest.TestCase):

    def test_accessing_members(self):
        comment = Comment()
        comment.author = "ben"
        quote = Quote("body", "", [])
        score = 0.5
        match = MatchedQuote(comment, quote, score)
        self.assertEqual(match.score, score)
        self.assertEqual(match.comment, comment)
        self.assertEqual(match.quote, quote)

    def test_print(self):
        comment = Comment()
        comment.author = "ben"
        quote = Quote("body", "", [])
        score = 0.5
        match = MatchedQuote(comment, quote, score)
        print(match)


class DictionaryOperations(unittest.TestCase):

    def test_to_dict(self):
        comment = Comment()
        comment.author = "ben"
        quote = Quote("body", "", [])
        score = 0.5
        match = MatchedQuote(comment, quote, score)
        d = match.to_dict()
        self.assertEqual(d["score"], score)
        self.assertEqual(d["comment"]["author"], "ben")
        self.assertEqual(d["quote"]["body"], "body")

    def test_from_dict(self):
        comment = Comment()
        comment.author = "ben"
        quote = Quote("body", "", [])
        score = 0.5
        d = {
            "comment": comment.to_dict(),
            "quote": quote.to_dict(),
            "score": score
        }
        match = MatchedQuote.from_dict(d)
        self.assertEqual(match.comment, comment)
        self.assertEqual(match.quote, quote)
        self.assertEqual(match.score, score)


class OperatorsOnScore(unittest.TestCase):
    def setUp(self):
        quote = Quote("body", "", [])
        comment = Comment()
        score = 0.5
        self.match = MatchedQuote(comment, quote, score)

    def test_eq(self):
        self.assertEqual(self.match, 0.5)

    def test_ne(self):
        self.assertNotEqual(self.match, 0.1)

    def test_lt(self):
        self.assertEqual(self.match < 0.8, True)

    def test_le(self):
        self.assertEqual(self.match <= 0.5, True)

    def test_ge(self):
        self.assertEqual(self.match >= 0.5, True)

    def test_gt(self):
        self.assertEqual(self.match > 0.1, True)


class OperatorsQuote(unittest.TestCase):
    def setUp(self):
        quote = Quote("body", "", [])
        comment = Comment()
        score = 0.5
        self.match = MatchedQuote(comment, quote, score)

    def test_eq(self):
        quote = Quote("body", "", [])
        self.assertEqual(self.match, quote)

    def test_ne(self):
        quote = Quote("body2", "", [])
        self.assertNotEqual(self.match, quote)


class OperatorsComment(unittest.TestCase):
    def setUp(self):
        quote = Quote("body", "", [])
        comment = Comment()
        comment.uid = "1234"
        score = 0.5
        self.match = MatchedQuote(comment, quote, score)

    def test_eq(self):
        comment = Comment()
        comment.uid = "1234"
        self.assertEqual(self.match, comment)

    def test_ne(self):
        comment = Comment()
        comment.uid = "asdf"
        self.assertNotEqual(self.match, comment)
