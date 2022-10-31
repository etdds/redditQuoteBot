from redditquotebot.quotes import Quote
from redditquotebot.reddit import Comment


class Reply():
    def __init__(self, comment: Comment, quote: Quote):
        self.quote = quote
        self.comment = comment

    def to_dict(self):
        return {
            "quote": self.quote.to_dict(),
            "comment": self.comment.to_dict(),
            "body": self.body()
        }

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
        
"{self.quote.body}"

{self.quote.author}

I'm a bot and this action was automatic.
        """
        return body
