from redditquotebot.utilities import Configuration, CredentialStore
from redditquotebot.reddit import Comment, Reply
from typing import List


class IReddit():
    def __init__(self, configuration: Configuration, credentials: CredentialStore):
        self.configuration = configuration
        self.credentials = credentials

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def get_comments(self, subreddit: str) -> List[Comment]:
        raise NotImplementedError()

    def reply_to_comment(self, comment: Comment, reply: Reply):
        raise NotImplementedError()
