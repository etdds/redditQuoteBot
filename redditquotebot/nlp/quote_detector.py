from redditquotebot.reddit import Comment
from redditquotebot.quotes import Quote
from redditquotebot.nlp import MatchedQuote, QuoteCommentMatcher
from typing import List, Optional


class QuoteDetector():
    """Main driver for matching comment with quotes.

    Compares a list of comments, and a list of quotes with a given matcher, and pass score.
    Returns the results, up to an optional maximum, sorted from best match to worse.
    """

    def __init__(self, quotes: List[Quote], comments: List[Comment]):
        """
        Args:
            quotes (List[Quote]): List of quotes to use.
            comments (List[Comment]): List of comments to use.
        """
        self.quotes = quotes
        self.comments = comments
        self.stored_matches = []

    def apply(self, matcher: QuoteCommentMatcher, score_threshold: float):
        """Apply a quote comment matcher to the list of quotes and comments.

        Args:
            matcher (QuoteCommentMatcher): The matcher to user.
            score_threshold (float): The pass score, of the matcher has a score above this threshold, the comment / quote combination is stored internally.
        """
        for comment in self.comments:
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
