from redditquotebot.reddit import Comment
from redditquotebot.quotes import Quote
from spacy.tokens.doc import Doc
from typing import List
from math import floor
from statistics import mean


class QuoteCommentMatcher():
    """Base class which defines a matcher for a single quote and comment.
    """

    def __init__(self):
        self._score = 0

    def compare(self, comment: Comment, quote: Quote):
        """Compare a comment and quote. Any derived compare operator should set the score between 0 and 1.

        Args:
            comment (Comment): The comment to use.
            quote (Quote): The quote to use.

        Raises:
            NotImplementedError: This is intentialy setup as a base class.
        """
        raise NotImplementedError()

    def score(self) -> float:
        """Get the resulting score of a compare operation.

        Raises:
            ValueError: The score is outside the 0-1 range.

        Returns:
            float: The score of the comparion. Must be between 0 and 1
        """
        if self._score > 1 or self._score < 0:
            raise ValueError(f"Score is expected to be between 0 and 1, got value {self._score}")
        return self._score


class QuoteCommentLengthMatcher(QuoteCommentMatcher):
    """A simple demonstration matcher which compares the character length of the quote's body to the character length of the comment's body.
    """

    def __init__(self):
        QuoteCommentMatcher.__init__(self)

    def compare(self, comment: Comment, quote: Quote):
        """Compare character length of the quote's body to the character length of the comment's body.

        Args:
            comment (Comment): The comment to use.
            quote (Quote): The quote to use.
        """
        comment_length = len(comment.body)
        quote_length = len(quote.body)
        if comment_length > quote_length:
            self._score = quote_length / comment_length
        else:
            self._score = comment_length / quote_length


class QuoteCommentNLPMatcher(QuoteCommentMatcher):
    def __init__(self, quote_comment_delta: float, minimum_sentence_word_length: int, bonus_coeff: float = 0.0000, bonus_start: int = 6, bonus_end: int = 10, match_sentence_coeff: float = 0):
        """A quote comment matches which uses NLP.

        The bonus_coeff, bonus_start and bonus_end is used to apply a bonus to the simularity match of the comment to float, based on the length of the comment.
        The application is as follows: 
            bonus_words = quote_word_length - bonus_start
            bonus_words = bonus_words if bonus_words < bonus_end else bonus_end
            score *= 1 + (bonus_coeff * bonus_words)

        The match sentence coefficient determins how many sentences of the quote need to match.
        Applied as follows
            sentence_count = floor(quote_sentence_count * match_sentence_coeff) + 1
            i.e: A match_sentence_coeff of 0 will result in 1 sentence, a coefficient of 0.5 for a 4 sentence quote will require 3 of 4 sentences to match

        The mean of the highest sentence_count number of scores is used to determine the final score.

        Args:
            quote_comment_delta (float): The maximum difference between the lengths of the comment and quote
            minimum_sentence_word_length (int): The minimum number of words a comment sentence must contain to be used.
            bonus_coeff (float): The bonus coefficient applied to comments with word counts: bonus_start < count < bonus_end
            bonus_start (int): The minimum word cound where the bonus is applied
            bonus_end (int): The maximum word cound where the bonus is applied
            match_sentenct_coeff (float): The coeffiecient used to determine how many sentences of a quote need to be matched.
        """
        QuoteCommentMatcher.__init__(self)
        self.minimum_sentence_word_length = minimum_sentence_word_length
        self.quote_comment_delta = quote_comment_delta
        self.bonus_start = bonus_start
        self.bonus_end = bonus_end
        self.bonus_coeff = bonus_coeff
        self.match_sentence_coeff = match_sentence_coeff

    def _compared_lengths_similar(self, comment: Doc, quote: Doc) -> bool:
        comment_length = len(comment.text)
        quote_length = len(quote.text)
        if comment_length > quote_length:
            score = quote_length / comment_length
        else:
            score = comment_length / quote_length
        return score > self.quote_comment_delta

    def _minimum_length_met(self, sentence: Doc) -> bool:
        return self._word_count(sentence) > self.minimum_sentence_word_length

    def _word_count(self, sentence: Doc) -> int:
        return len(sentence.text.split(" "))

    def _apply_length_bonus(self, sentence: Doc, score: float) -> float:
        bonus = (self._word_count(sentence) - self.bonus_start)
        bonus = self.bonus_end if bonus > self.bonus_end else bonus
        score *= 1 + bonus * self.bonus_coeff
        return 1.0 if score > 1.0 else score

    def compare(self, comment: List[Doc], quote: List[Doc]):
        min_matched_sentence = floor(len(quote) * self.match_sentence_coeff) + 1
        max_scores = [0.0 for _ in range(min_matched_sentence)]
        for csent in comment:
            if not self._minimum_length_met(csent):
                continue
            for qsent in quote:
                if not self._minimum_length_met(qsent) or not self._compared_lengths_similar(csent, qsent):
                    continue
                if qsent and qsent.vector_norm and csent and csent.vector_norm:
                    score = qsent.similarity(csent)
                    score = self._apply_length_bonus(qsent, score)
                    if score > max_scores[0]:
                        for i in range(min_matched_sentence - 1):
                            max_scores[i + 1] = max_scores[i]
                        max_scores[0] = score
        self._score = mean(max_scores)
