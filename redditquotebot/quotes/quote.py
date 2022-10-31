from typing import List


class Quote():
    """Represents a single quote
    """

    def __init__(self, body: str, author: str, category: List[str]):
        """Create a quote object

        Args:
            body (str): The body, text of the quote.
            author (str): The author of the quote
            category (List[str]): A list of keywords which describe the quote.
        """
        self.body = body
        self.author = author
        self.category = category

    def __repr__(self):
        return f"body: {self.body}, author: {self.author}, category: {', '.join(self.category)}"

    def to_dict(self) -> dict:
        """Return the contents of the quote as a dictionary

        Returns:
            dict: Dictionary conatining comment contents
        """
        return {
            "body": self.body,
            "author": self.author,
            "category": self.category
        }
