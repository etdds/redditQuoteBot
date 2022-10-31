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


class QuoteLengthFilter():
    """Filter a quote by the length of its body
    """

    def __init__(self, quote: Quote):
        self._quote = quote

    def __gt__(self, other) -> bool:
        return len(self._quote.body) > other

    def __ge__(self, other) -> bool:
        return len(self._quote.body) >= other

    def __lt__(self, other) -> bool:
        return len(self._quote.body) < other

    def __le__(self, other) -> bool:
        return len(self._quote.body) <= other

    def __eq__(self, other) -> bool:
        return len(self._quote.body) == other

    def __ne__(self, other) -> bool:
        return len(self._quote.body) != other
