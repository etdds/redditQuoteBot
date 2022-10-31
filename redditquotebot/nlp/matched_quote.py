from redditquotebot.reddit import Comment
from redditquotebot.quotes import Quote


class MatchedQuote():
    def __init__(self, comment: Comment, quote: Quote, score: float):
        self.comment = comment
        self.quote = quote
        self.score = score

    def to_dict(self) -> dict:
        return {
            "comment": self.comment.to_dict(),
            "quote": self.quote.to_dict(),
            "score": self.score
        }

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
