
class Comment():
    """Definition of a single Reddit comment
    """

    def __init__(self):
        self.body = ""
        self.utc = 0
        self.author = ""
        self.url = ""
        self.subreddit = ""
        self.edited = False
        self.uid = ""
        self.score = 0

    def __repr__(self):
        return f"Author: {self.author}, utc: {self.utc}, subreddit: {self.subreddit}, edited: {self.edited}, url: {self.url}, id: {self.uid}, body: {self.body}, score: {self.score}"

    def to_dict(self) -> dict:
        """Return the contents of the comment as a dictionary.

        Returns:
            dict: Dictionary conatining comment contents
        """
        return {
            "body": self.body,
            "utc": self.utc,
            "author": self.author,
            "url": self.url,
            "subreddit": self.subreddit,
            "edited": self.edited,
            "uid": self.uid,
            "score": self.score,
        }

    @staticmethod
    def from_dict(comment_dict: dict):
        """Populate comment contents from a dictionary

        Parameters:
            comment_dict (dict): The comment contents as a dictionary
        """
        comment = Comment()
        comment.body = comment_dict["body"]
        comment.utc = comment_dict["utc"]
        comment.author = comment_dict["author"]
        comment.url = comment_dict["url"]
        comment.subreddit = comment_dict["subreddit"]
        comment.edited = comment_dict["edited"]
        comment.uid = comment_dict["uid"]
        # Adding in a try block keeps backwards compatibility.
        try:
            comment.score = comment_dict["score"]
        except KeyError:
            comment.score = 1
        return comment

    def __eq__(self, other):
        return self.uid == other.uid

    def __ne__(self, other):
        return self.uid != other.uid
