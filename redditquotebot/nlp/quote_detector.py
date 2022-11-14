from redditquotebot.reddit import Comment
from redditquotebot.quotes import Quote
from redditquotebot.nlp import MatchedQuote, QuoteCommentMatcher, QuoteCommentNLPMatcher
from typing import List, Optional
import spacy


class QuoteDetector():
    """Main driver for matching comment with quotes.

    Compares a list of comments, and a list of quotes with a given matcher, and pass score.
    Returns the results, up to an optional maximum, sorted from best match to worse.
    """

    def __init__(self, quotes: List[Quote]):
        """
        Args:
            quotes (List[Quote]): List of quotes to use.
        """
        self.quotes = quotes
        self.stored_matches = []

    def apply(self, matcher: QuoteCommentMatcher, score_threshold: float, filter_author: bool,  comments: List[Comment]):
        """Apply a quote comment matcher to the list of quotes and comments.

        Args:
            matcher (QuoteCommentMatcher): The matcher to user.
            score_threshold (float): The pass score, of the matcher has a score above this threshold, the comment / quote combination is stored internally.
            filter_author (bool): If true, comments which contain the author of the quote are discarded. (Not implemented)
            comments (List[Comment]): The list of comments to process
        """
        if filter_author is True:
            raise NotImplementedError("Filter by author is not currently implemented for this quote detector.")
        for comment in comments:
            for quote in self.quotes:
                matcher.compare(comment, quote)
                if matcher.score() >= score_threshold:
                    self.stored_matches.append(MatchedQuote(comment, quote, matcher.score()))

    def get_matches(self, comment: Comment, maximum: Optional[int] = None) -> List[MatchedQuote]:
        """Get the quote matches for a given comment.

        Return up the to maximum count, sorted from best match to worst.

        Args:
            comment (Comment): The comment to search for.
            maximum (Optional[int], optional): The maximum number of comments, if not used, all matches are returned. Defaults to None.

        Returns:
            List[MatchedQuote]: List of matched quote and comments.
        """
        target_matches = [match for match in self.stored_matches if match.comment == comment]
        target_matches = sorted(target_matches, key=lambda match: match.score, reverse=True)
        if maximum is None:
            return target_matches
        else:
            return target_matches[0:maximum]

    def reset(self):
        """Reset the internal list of matches. Should be used between calls to apply
        """
        self.stored_matches = []


class QuoteNLPDetector(QuoteDetector):
    """Quote detecter which operates with natural language proccessing (NLP) with spacy
    """

    def __init__(self, quotes: List[Quote]):
        """
        Args:
            quotes (List[Quote]): List of quotes to use.
        """
        super().__init__(quotes)
        self.nlp = spacy.load("en_core_web_md")
        self.nlp_quotes = []
        for q in [self.nlp(q.body) for q in self.quotes]:
            self.nlp_quotes.append(self._get_sentences(q))

    def _get_sentences(self, body):
        cleaned_sentences = []
        sentences = [s for s in body.sents]
        for sentence in sentences:
            cleaned_sentences.append(self._clean_sentence(sentence))
        return cleaned_sentences

    def _clean_sentence(self, sentence):
        cleaned = []
        for word in sentence:
            # Remove proper nouns
            if word.pos_ == "PROPN":
                continue
            # Remove punctuation
            elif word.is_punct:
                continue
            # Remove short words
            elif len(word) < 2:
                continue
            else:
                cleaned.append(word)
        return self.nlp(" ".join([c.text for c in cleaned]))

    def _get_only_ascii(self, comment: str) -> str:
        return ''.join([i if (ord(i) < 128) and (ord(i) >= 32) and i not in ["-", ":", "?"] else ' ' for i in comment])

    def _contains_author(self, body: str, author: str) -> bool:
        word_list = self._get_only_ascii(body).replace(".", "").replace(",", "").split(" ")
        for name in author.split(" "):
            if len(name) > 2 and name in word_list:
                return True
        return False

    def apply(self, matcher: QuoteCommentNLPMatcher, score_threshold: float, filter_author: bool, comments: List[Comment]):
        """Apply a NLP based quote comment matcher to the list of quotes and comments.

        Args:
            matcher (QuoteCommentNLPMatcher): The matcher to user.
            score_threshold (float): The pass score, of the matcher has a score above this threshold, the comment / quote combination is stored internally.
            filter_author (bool): If true, comments which contain the author of the quote are discarded.
            comments (List[Comment]): The list of comments to process
        """
        for comment in comments:
            comment.body = self._get_only_ascii(comment.body)
            sentences = self._get_sentences(self.nlp(comment.body))
            for iq, nlp_quote in enumerate(self.nlp_quotes):
                matcher.compare(sentences, nlp_quote)
                if matcher.score() >= score_threshold:
                    if not self._contains_author(comment.body, self.quotes[iq].author) or not filter_author:
                        self.stored_matches.append(MatchedQuote(comment, self.quotes[iq], matcher.score()))
