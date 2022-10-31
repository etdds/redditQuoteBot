from redditquotebot.reddit import Comment
from redditquotebot.quotes import Quote


class QuoteCommentMatcher():

    def __init__(self):
        self._matches = False
        self._score = 0

    def compare(self, comment: Comment, quote: Quote):
        raise NotImplementedError()

    def matches(self) -> bool:
        return self._matches

    def score(self) -> int:
        return self._score
