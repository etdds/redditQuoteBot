from nis import match
import unittest
from redditquotebot.quotes import Quote
from redditquotebot.reddit import Comment
from redditquotebot.nlp import MatchedQuote, QuoteDetector, QuoteCommentLengthMatcher, QuoteCommentNLPMatcher, QuoteNLPDetector


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

        self.detector = QuoteDetector(self.quotes)

    def test_getting_comments_one_match(self):
        matcher = QuoteCommentLengthMatcher()
        self.detector.apply(matcher, 1, False, self.comments)
        matches = self.detector.get_matches(self.comments[3])
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[3])

    def test_getting_comments_multiple(self):
        matcher = QuoteCommentLengthMatcher()
        self.detector.apply(matcher, 1, False, self.comments)
        matches = self.detector.get_matches(self.comments[2])
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].quote, self.quotes[1])
        self.assertEqual(matches[1].quote, self.quotes[2])

    def test_getting_comments_multiple_limited_to_maximum(self):
        matcher = QuoteCommentLengthMatcher()
        self.detector.apply(matcher, 1, False, self.comments)
        matches = self.detector.get_matches(self.comments[2], 1)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[1])

    def test_getting_comments_multiple_sorted(self):
        matcher = QuoteCommentLengthMatcher()
        self.detector.apply(matcher, 0.5, False, self.comments)
        matches = self.detector.get_matches(self.comments[2])
        self.assertEqual(len(matches), 7)

        self.detector.reset()
        self.detector.apply(matcher, 0.5, False, self.comments)
        matches = self.detector.get_matches(self.comments[2], 2)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].quote, self.quotes[1])
        self.assertEqual(matches[1].quote, self.quotes[2])


class MatchingNLPComments(unittest.TestCase):
    def setUp(self):
        self.quotes = [
            Quote("I has a long dream", "Jimmy", []),
            Quote("Is this really the end. It looks like it.", "", []),
        ]
        comment1 = Comment()
        comment2 = Comment()
        comment1.body = "I had a long dream. Jimmy"
        comment2.body = "I don't know"
        self.comments = [comment1, comment2]
        self.detector = QuoteNLPDetector(self.quotes)

    def test_getting_a_single_match(self):
        matcher = QuoteCommentNLPMatcher(0.5, 2)
        self.detector.apply(matcher, 0.8, False, self.comments)
        matches = self.detector.get_matches(self.comments[0])
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[0])

    def test_sentance_is_cleaned_of_puctuation(self):
        comment_dirty = Comment()
        comment_dirty.body = "I has a long dream."
        matcher = QuoteCommentNLPMatcher(0.5, 2, bonus_coeff=0)
        self.detector.apply(matcher, 1.0, False, [comment_dirty])
        matches = self.detector.get_matches(comment_dirty)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[0])

    def test_sentance_is_cleaned_of_non_ascii(self):
        comment_dirty = Comment()
        comment_dirty.body = "I has a\b \u2019  long dream."
        matcher = QuoteCommentNLPMatcher(0.5, 2, bonus_coeff=0)
        self.detector.apply(matcher, 1.0, False, [comment_dirty])
        matches = self.detector.get_matches(comment_dirty)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[0])

    def test_sentance_is_cleaned_of_proper_nouns(self):
        comment_dirty = Comment()
        comment_dirty.body = "I has a Ryan Ben London long dream."
        matcher = QuoteCommentNLPMatcher(0.5, 2, bonus_coeff=0)
        self.detector.apply(matcher, 1.0, False, [comment_dirty])
        matches = self.detector.get_matches(comment_dirty)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[0])

    def test_sentance_short_words_removed(self):
        comment_dirty = Comment()
        comment_dirty.body = "I has a i long dream."
        matcher = QuoteCommentNLPMatcher(0.5, 2, bonus_coeff=0)
        self.detector.apply(matcher, 1.0, False, [comment_dirty])
        matches = self.detector.get_matches(comment_dirty)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[0])

    def test_sentance_matches_nothing(self):
        comment_dirty = Comment()
        comment_dirty.body = "This sentence doesn't match any quote."
        matcher = QuoteCommentNLPMatcher(0.5, 2, bonus_coeff=0)
        self.detector.apply(matcher, 1.0, False, [comment_dirty])
        matches = self.detector.get_matches(comment_dirty)
        self.assertEqual(len(matches), 0)

    def test_multiple_sentences_comment(self):
        comment = Comment()
        comment.body = "I woke up. I has a long dream. It was great."
        matcher = QuoteCommentNLPMatcher(0.5, 2, bonus_coeff=0)
        self.detector.apply(matcher, 1.0, False, [comment])
        matches = self.detector.get_matches(comment)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[0])

    def test_multiple_sentences_quote(self):
        comment = Comment()
        comment.body = "It looks like it"
        matcher = QuoteCommentNLPMatcher(0.5, 2, bonus_coeff=0)
        self.detector.apply(matcher, 1.0, False, [comment])
        matches = self.detector.get_matches(comment)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].quote, self.quotes[1])

    def test_getting_a_single_match_with_author_filter(self):
        matcher = QuoteCommentNLPMatcher(0.5, 2)
        self.detector.apply(matcher, 0.8, True, self.comments)
        matches = self.detector.get_matches(self.comments[0])
        self.assertEqual(len(matches), 0)
