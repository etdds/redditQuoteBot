import unittest
from redditquotebot.quotes import Quote
from redditquotebot.reddit import Comment
from redditquotebot.nlp import QuoteCommentMatcher, QuoteCommentLengthMatcher, QuoteCommentNLPMatcher
import spacy

nlp = spacy.load("en_core_web_md")


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


class TestingQuoteCommenNLPMatcher(unittest.TestCase):

    def setUp(self):
        self.quote = Quote("I had a dream! The dream was great.", "", [])
        self.quotes = [
            nlp("I had a dream"),
            nlp("short"),
            nlp("")
        ]

    def test_comment_too_short(self):
        comment = [nlp("I")]
        matcher = QuoteCommentNLPMatcher(quote_comment_delta=0, minimum_sentence_word_length=2)
        matcher.compare(comment, self.quotes[0:1])
        self.assertEqual(matcher.score(), 0)

    def test_quote_too_short(self):
        comment = [nlp("I had a dream")]
        matcher = QuoteCommentNLPMatcher(quote_comment_delta=0, minimum_sentence_word_length=2)
        matcher.compare(comment, self.quotes[2:3])
        self.assertEqual(matcher.score(), 0)

    def test_comment_quote_delta_too_large(self):
        comment = [nlp("I had a dream and it went like this")]
        matcher = QuoteCommentNLPMatcher(quote_comment_delta=0.9, minimum_sentence_word_length=3)
        matcher.compare(comment, self.quotes[0:1])
        self.assertEqual(matcher.score(), 0)

    def test_perfect_match(self):
        comments = [nlp("I had a dream"), nlp("Another sentence which doesn't match")]
        matcher = QuoteCommentNLPMatcher(quote_comment_delta=0.9, minimum_sentence_word_length=3, bonus_coeff=0)
        matcher.compare(comments, self.quotes[0:2])
        self.assertEqual(matcher.score(), 1)

    def test_almost_perfect_match(self):
        comments = [nlp("I has a dream"), nlp("Another sentence which doesn't match")]
        matcher = QuoteCommentNLPMatcher(quote_comment_delta=0.8, minimum_sentence_word_length=3)
        matcher.compare(comments, self.quotes[0:2])
        self.assertEqual(matcher.score() > 0.9, True)

    def test_empty_quote(self):
        comments = [nlp("I has a dream"), nlp("Another sentence which doesn't match")]
        matcher = QuoteCommentNLPMatcher(quote_comment_delta=0.8, minimum_sentence_word_length=3)
        matcher.compare(comments, self.quotes[2:3])
        self.assertEqual(matcher.score(), 0)

    def test_applying_length_bonus(self):
        comments = [nlp("I has a dreams"), nlp("Another sentence which doesn't match")]
        matcher = QuoteCommentNLPMatcher(quote_comment_delta=0.8, minimum_sentence_word_length=3, bonus_coeff=0)
        matcher.compare(comments, self.quotes[0:2])
        no_bonus_score = matcher.score()
        bonus_matcher = QuoteCommentNLPMatcher(
            quote_comment_delta=0.8, minimum_sentence_word_length=3, bonus_coeff=0.001, bonus_start=0, bonus_end=10)
        bonus_matcher.compare(comments, self.quotes[0:2])
        bonus_score = bonus_matcher.score()
        # Bonus = 1 + (4 words * 0.001)
        self.assertEqual(bonus_score, no_bonus_score * 1.004)

    def test_empty_comment(self):
        comments = [nlp("")]
        matcher = QuoteCommentNLPMatcher(quote_comment_delta=0.0, minimum_sentence_word_length=0)
        matcher.compare(comments, self.quotes[0:1])
        self.assertEqual(matcher.score(), 0)

    def test_multiple_sentence_requirement(self):
        comments = [nlp("I had a dream"), nlp("Another sentence which doesn't match")]
        matcher = QuoteCommentNLPMatcher(
            quote_comment_delta=0.8, minimum_sentence_word_length=3, bonus_coeff=0, match_sentence_coeff=0.5)
        matcher.compare(comments, self.quotes[0:2])
        self.assertEqual(matcher.score(),  0.5)
