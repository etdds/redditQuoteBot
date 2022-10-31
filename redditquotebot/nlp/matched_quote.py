from redditquotebot.reddit import Comment
from redditquotebot.quotes import Quote


class MatchedQuote():
    """Object representing a comment to quote match.
    """

    def __init__(self, comment: Comment, quote: Quote, score: float):
        """
        Args:
            comment (Comment): The comment.
            quote (Quote): The quote.
            score (float): The score of the comment to quote match.
        """
        self.comment = comment
        self.quote = quote
        self.score = score

    def to_dict(self) -> dict:
        """Get the contents of the matched quote as a dictionary

        Returns:
            dict: Contents as a dictionary.
        """
        return {
            "comment": self.comment.to_dict(),
            "quote": self.quote.to_dict(),
            "score": self.score
        }

    @staticmethod
    def from_dict(match_dict: dict):
        """Get the contents of the matched quote from a dictionary

        Parameters:
            match_dict (dict): The match contents as a dictionary

        Returns:
            The constructed object.
        """
        comment = Comment().from_dict(match_dict["comment"])
        quote = Quote.from_dict(match_dict["quote"])
        score = match_dict["score"]
        return MatchedQuote(comment, quote, score)

    def __repr__(self):
        return f"Score: {self.score}, Comment: {self.comment}, Quote: {self.quote}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Quote):
            return self.quote == other
        elif isinstance(other, Comment):
            return self.comment == other
        return self.score == other

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Quote):
            return self.quote != other
        elif isinstance(other, Comment):
            return self.comment != other
        return self.score != other

    def __gt__(self, score: int) -> bool:
        return self.score > score

    def __ge__(self, score: int) -> bool:
        return self.score >= score

    def __lt__(self, score: int) -> bool:
        return self.score < score

    def __le__(self, score: int) -> bool:
        return self.score <= score
