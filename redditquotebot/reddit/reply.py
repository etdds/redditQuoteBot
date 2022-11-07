from redditquotebot.quotes import Quote
from redditquotebot.reddit import Comment


class Reply():
    """An object represeting a reddit reply.
    The comment and quote objects are used to generate the reply contents (body)
    """

    def __init__(self, comment: Comment, quote: Quote):
        self.quote = quote
        self.comment = comment

    def to_dict(self) -> dict:
        """Generate a dictionary from the reply

        Returns:
            dict: The reply contents as a dictionary
        """
        return {
            "quote": self.quote.to_dict(),
            "comment": self.comment.to_dict(),
            "body": self.body()
        }

    @staticmethod
    def from_dict(reply_dict: dict):
        """Generate a reply object form a dictionary.

        Args:
            reply_dict (dict): The dictionary containing the reply conents.

        Returns:
            Reply: A reply object with the contents.
        """
        return Reply(Comment.from_dict(reply_dict["comment"]), Quote.from_dict(reply_dict["quote"]))

    def __repr__(self):
        return self.body()

    def __str__(self) -> str:
        return self.body()

    def body(self) -> str:
        """Get the reply body, generated from the comment and quote

        Returns:
            str: body of the reply
        """
        body = f"""Hi {self.comment.author},

It looks like your comment closely matches the famous quote:

"{self.quote.body}" - {self.quote.author}

*I'm a bot and this action was automatic [Project source](https://github.com/etdds/redditQuoteBot).*"""
        return body
