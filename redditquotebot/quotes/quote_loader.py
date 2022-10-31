from io import TextIOWrapper
import csv
from redditquotebot.quotes import QuoteDB, Quote
import string


class QuoteLoader():
    """Provides static methods for loading quotes from different data sources
    """
    @staticmethod
    def from_csv(file_handler: TextIOWrapper) -> QuoteDB:
        """Load a quoteDB from a CSV file.

        Expects csv with at least headings quote,author,category and comma delimiter. An optional index column at position 0 is ignored, if found.

        Args:
            file_handler (str): Open file handler

        Raises:
            FileNotFoundError: The given filename cannot be found

        Returns:
            QuoteDB: A database of quotes.
        """
        quotes = []
        reader = csv.reader(file_handler, delimiter=",")
        index = 0
        for row in reader:
            if index != 0:
                try:
                    body = ''.join(c for c in row[-3] if c in string.printable)
                    author = row[-2]
                    category_list = row[-1].replace("[", "").replace("]", "").split(",")
                    category = [c.strip() for c in category_list]
                except IndexError as exp:
                    raise IndexError("Error loading three columns from CSV") from exp
                quotes.append(Quote(body=body, author=author, category=category))
            index += 1
        return QuoteDB(quotes)
