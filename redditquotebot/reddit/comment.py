

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
