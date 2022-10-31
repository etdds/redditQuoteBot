from redditquotebot.reddit import Comment
from redditquotebot.quotes import Quote


class QuoteCommentMatcher():

    def __init__(self):
        self._score = 0

    def compare(self, comment: Comment, quote: Quote):
        raise NotImplementedError()

    def score(self) -> int:
        return self._score


class QuoteCommentLengthMatcher(QuoteCommentMatcher):

    def __init__(self):
        QuoteCommentMatcher.__init__(self)

    def compare(self, comment: Comment, quote: Quote):
        comment_length = len(comment.body)
        quote_length = len(quote.body)
        if comment_length > quote_length:
            self._score = quote_length / comment_length
        else:
            self._score = comment_length / quote_length
