from io import TextIOWrapper
import csv
from redditquotebot.quotes import QuoteDB, Quote


class QuoteLoader():
    """Provides static methods for loading quotes from different data sources
    """
    @staticmethod
    def from_csv(file_handler: TextIOWrapper) -> QuoteDB:
        """Load a quoteDB from a CSV file.

        Expects csv with headings quote,author,category and comma delimiter

        Args:
            file_handler (str): Open file handler

        Raises:
            FileNotFoundError: The given filename cannot be found

        Returns:
            ScrapeState: Scrape state object populated from JSON values
        """
        quotes = []
        reader = csv.reader(file_handler, delimiter=",")
        index = 0
        for row in reader:
            if index != 0:
                try:
                    body = row[0]
                    author = row[1]
                    category = row[2].split(",")
                except IndexError as exp:
                    raise IndexError("Error loading three columns from CSV") from exp
                quotes.append(Quote(body=body, author=author, category=category))
            index += 1
        return QuoteDB(quotes)
