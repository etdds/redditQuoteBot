from redditquotebot.quotes import Quote


class QuoteAuthorFilter():
    """Filter a quote by author
    """

    def __init__(self, quote: Quote):
        self._quote = quote

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Quote):
            return self._quote.author == other.author
        else:
            return self._quote.author == other

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
