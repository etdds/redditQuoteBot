from redditquotebot.quotes import Quote
from typing import List, Callable


class QuoteDB():
    def __init__(self, quotes: List[Quote]):
        self._quotes = quotes

    def __len__(self):
        return len(self._quotes)

    def __getitem__(self, index):
        return self._quotes[index]

    def apply(self, operator: Callable):
        """Apply a filter to the quote DB

        Expected usage:
            quote_db.apply(lambda quote: QuoteAuthorFilter(quote) == "ben")

        Args:
            operator (Callable): labda function description for the filter to apply
        """
        new_db = QuoteDB(list(filter(operator, self._quotes)))
        return new_db
