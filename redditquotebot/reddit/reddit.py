from redditquotebot.reddit import RedditConnectionError, RedditReplyError, RedditUserAuthenticationError
from redditquotebot.utilities import Configuration, CredentialStore
from redditquotebot.reddit import Comment, Reply
from typing import List
import praw
from prawcore.exceptions import Forbidden


class Reddit():
    """Interface around praw, for interacting with Reddit
    """

    def __init__(self, configuration: Configuration, credentials: CredentialStore):
        """Initialise module

        Args:
            configuration (Configuration): The configuration to use.
            credentials (CredentialStore): Credentials to use for connecting to Reddit.
        """
        self.configuration = configuration
        self.credentials = credentials
        self._reddit = None

    def connect(self):
        """Connect to Reddit

        Raises:
            exp: An unknown exception occured. Could be one of https://praw.readthedocs.io/en/v3.6.2/pages/exceptions.html
            RedditConnectionError: The username supplied did not match that associated with praw, after connection.
        """
        try:
            self._reddit = praw.Reddit(
                user_agent=self.credentials.reddit.user_agent,
                client_id=self.credentials.reddit.client_id,
                client_secret=self.credentials.reddit.client_secret,
                username=self.credentials.reddit.username,
                password=self.credentials.reddit.password,
                ratelimit_minutes=60
            )
        except Exception as exp:
            raise exp from exp

        if self._reddit.user.me() != self.credentials.reddit.username:
            raise RedditConnectionError("Unexpected username occurred after connecting to Reddit.")

    def disconnect(self):
        # No special handling required
        pass

    def get_comments(self, subreddit: str) -> List[Comment]:
        """Get comments from a particular subreddit.

        The ammount of submissions queried is controlled by the configuration.reddit.new_submissions_per_request field.

        Args:
            subreddit (str): The subreddit to query

        Returns:
            List[Comment]: The list of comments found
        """
        subreddit = self._reddit.subreddit(subreddit)
        max_comments = self.configuration.reddit.max_comments_per_request
        comments = []

        count = self.configuration.reddit.new_submissions_per_request
        for submission in subreddit.new(limit=count):
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comments.append(self._extract_comment(comment))
                if (len(comments) >= max_comments):
                    return comments

        return comments

    def get_user_comments(self, user_name: str) -> List[Comment]:
        """Get a list of comments posted by a given user.

        Args:
            user_name (str): The username to query.

        Returns:
            List[Comment]: List of found comments.
        """
        comments = []
        redditor = self._reddit.redditor(user_name)
        for comment in redditor.comments.new(limit=None):
            comments.append(self._extract_comment(comment))
        return comments

    def remove_comment(self, comment: Comment):
        """Remove a comment.

        Args:
            comment (Comment): The comment to remove. The UID field is used to lookup the comment.

        Raises:
            RedditUserAuthenticationError: Raised if an authentication error is thrown by reddit.
        """
        c = self._reddit.comment(comment.uid)
        try:
            c.delete()
        except Forbidden as exc:
            raise RedditUserAuthenticationError("Cannot remove comment, access denied.") from exc

    def reply_to_comment(self, comment: Comment, reply: Reply):
        """Post a reply to a comment.

        Args:
            comment (Comment): The comment to reply too
            reply (Reply): The reply to use.

        Raises:
            RedditReplyError: An error occured when posting the reply.
        """
        comment = self._reddit.comment(comment.uid)
        try:
            comment.reply(reply.body())
        except Forbidden as exc:
            raise RedditReplyError("Cannot post reply, got internal forbidden exception") from exc

    def _extract_comment(self, comment) -> Comment:
        new_comment = Comment()
        new_comment.body = comment.body
        new_comment.utc = comment.created_utc
        new_comment.edited = comment.edited
        new_comment.subreddit = comment.subreddit_name_prefixed
        new_comment.url = f"https://reddit.com{comment.permalink}"
        new_comment.uid = comment.id
        new_comment.score = comment.score
        try:
            new_comment.author = comment.author.name
        except AttributeError:
            new_comment.author = "unknown"
        return new_comment
