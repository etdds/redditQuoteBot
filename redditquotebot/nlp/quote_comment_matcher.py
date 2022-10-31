from redditquotebot.reddit import Comment
from redditquotebot.quotes import Quote


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
