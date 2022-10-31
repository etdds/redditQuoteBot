
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

    def __repr__(self):
        return f"Author: {self.author}, utc: {self.utc}, subreddit: {self.subreddit}, edited: {self.edited}, url: {self.url}, id: {self.uid}, body: {self.body}"

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
        }

    def from_dict(self, comment_dict: dict):
        """Populate comment contents from a dictionary

        Parameters:
            comment_dict (dict): The comment contents as a dictionary
        """
        self.body = comment_dict["body"]
        self.utc = comment_dict["utc"]
        self.author = comment_dict["author"]
        self.url = comment_dict["url"]
        self.subreddit = comment_dict["subreddit"]
        self.edited = comment_dict["edited"]
        self.uid = comment_dict["uid"]
        return self

    def __eq__(self, other):
        return self.uid == other.uid

    def __ne__(self, other):
        return self.uid != other.uid
