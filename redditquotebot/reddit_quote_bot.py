# The 'main' runner

# Setup as a class with a builder to populate all the required configuration field

# Runner would do:
# Initialise
# Then
# Get new comments based on last request time
# Save last request time
# Find quotes which best match the each comment
# Save the pre-selection list for analysis later
# Build a reply for the best match (above a threshold)
# Post a reply
# Repeat

from typing import List
from redditquotebot.reddit import IReddit, CommentUTCFilter, CommentFilter, Comment, CommentAuthorFilter
from redditquotebot.utilities import *
from redditquotebot.quotes import *
from redditquotebot import QuoteCommentMatcher


class RedditQuoteBot():
    """A reddit quote bot used for detecting and automatically replying to comments which closely match famous quotes.
    """

    def __init__(self):
        self.credentials = CredentialStore()
        self.configuration = Configuration()
        self.scrape_state_loader = {
            "handler": ScrapeStateLoader.from_json,
            "filepath": ""
        }
        self.scrape_state_storer = {
            "handler": ScrapeStateStorer.to_json,
            "filepath": ""
        }
        self.record_keeper_loader = {
            "handler": RecordLoader.from_json,
            "filepath": ""
        }
        self.record_keeper_storer = {
            "handler": RecordStorer.to_json,
            "filepath": ""
        }
        self.reddit = IReddit(self.configuration, self.credentials)
        self.quotes = QuoteDB([])
        self.matcher = QuoteCommentMatcher()

    def get_latest_comments(self, subreddit: str) -> List[Comment]:
        """Get the latest comments from a given subreddit.

        Uses the scrape state and recored keeper files to filter out comments which have already been stored. Only returns and stores new comments.

        Args:
            subreddit (str): The subreddit to qurey

        Returns:
            List[Comment]: A list of new comment, which have not previously been fetched.
        """
        scrape_state = self.scrape_state_loader["handler"](self.scrape_state_loader["filepath"])
        records = self.record_keeper_loader["handler"](self.record_keeper_loader["filepath"])

        comments = self.reddit.get_comments(subreddit)

        latest_stored_utc = scrape_state.latest_subreddit_utc(subreddit)
        comment_filter = CommentFilter(comments)
        comment_filter.apply(lambda comment: CommentUTCFilter(comment) > latest_stored_utc)
        comment_filter.apply(lambda comment: CommentAuthorFilter(comment) != self.credentials.reddit.username)
        filtered_comments = comment_filter.result()
        if len(filtered_comments):
            latest_fetched_utc = comment_filter.latest()

            records.log_comments(filtered_comments)
            self.record_keeper_storer["handler"](self.record_keeper_storer["filepath"], records)

            scrape_state.update_latest_subreddit_utc(subreddit, latest_fetched_utc)
            self.scrape_state_storer["handler"](self.scrape_state_storer["filepath"], scrape_state)
        return filtered_comments

    def connect(self):
        """Connect (login) to reddit
        """
        self.reddit.connect()
