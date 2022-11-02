import sys
from typing import List
from redditquotebot.reddit import *
from redditquotebot.utilities import *
from redditquotebot.quotes import *
from redditquotebot.nlp import *
import logging

logger = logging.getLogger(__name__)


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
        self.ram_based_records = False
        self.ram_based_scrape_state = False
        self.reddit = IReddit(self.configuration, self.credentials)
        self.quote_matcher = QuoteCommentMatcher()
        self.quote_threshold = 1.0
        self.detector = QuoteDetector([])

    def get_latest_comments(self, subreddit: str, scrape_state: ScrapeState, records: RecordKeeper) -> List[Comment]:
        """Get the latest comments from a given subreddit.

        Uses the scrape state and recored keeper files to filter out comments which have already been stored. Only returns and stores new comments.

        Args:
            subreddit (str): The subreddit to qurey
            scrape_state (ScrapeState): Object tracking scrape state
            records (RecordKeeper): Object for record keeping

        Returns:
            List[Comment]: A list of new comment, which have not previously been fetched.
        """

        comments = self.reddit.get_comments(subreddit)
        latest_stored_utc = scrape_state.latest_subreddit_utc(subreddit)
        comment_filter = CommentFilter(comments)
        comment_filter.apply(lambda comment: CommentUTCFilter(comment) > latest_stored_utc)
        comment_filter.apply(lambda comment: CommentAuthorFilter(comment) != self.credentials.reddit.username)
        comment_filter.apply(lambda comment: CommentEdditedFilter(comment) == False)
        comment_filter.apply(lambda comment: CommentLengthFilter(comment) >=
                             self.configuration.reddit.minimum_comment_length)
        filtered_comments = comment_filter.result()

        if len(filtered_comments):
            latest_fetched_utc = comment_filter.latest()
            records.log_comments(filtered_comments)
            scrape_state.update_latest_subreddit_utc(subreddit, latest_fetched_utc)
        return filtered_comments

    def get_matching_quotes(self, comments: List[Comment], records: RecordKeeper) -> List[List[MatchedQuote]]:
        """Get matching quotes for a list of comments. Uses internal quote database

        Args:
            comments (List[Comment]): The list of comments to compare.
            records (RecordKeeper): Object for record keeping

        Returns:
            List[MatchedQuote]: A list of matched quotes, each comment may appear up to configuration.reddit.matched_quotes_to_log times.
        """
        self.detector.apply(self.quote_matcher, self.quote_threshold, comments)
        matches = []

        # TODO This should be a configuration option.
        matched_quotes_to_log = 5

        for comment in comments:
            found = self.detector.get_matches(comment, matched_quotes_to_log)
            if len(found):
                matches.append(found)
                records.log_matched_quote(found)
        return matches

    def reply_to_comments(self, matches: List[List[MatchedQuote]], threshold: float, records: RecordKeeper) -> List[Reply]:
        """Reply to each comment of the best quote match from a list of quotes.

        Args:
            matches (List[List[MatchedQuote]]): A nested list of comment matches.
            threshold (float): Only matches with a score higher or equal to this number are actually replied to.
            records (RecordKeeper): Object for record keeping.

        Returns:
            List[Reply]: List of all replies sent
        """
        replies = []
        for match_list in matches:
            match = match_list[0]
            if match.score >= threshold:
                reply = Reply(match.comment, match.quote)
                replies.append(reply)

        # TODO guard this by configuration, we aren't ready to post yet!
        # for reply in replies:
        #     self.reddit.reply_to_comment(reply.comment, reply)

        records.log_reply(replies)
        return replies

    def connect(self):
        """Connect (login) to reddit
        """
        self.reddit.connect()

    def start(self):
        """Start up the bot!
        """
        subreddits = self.configuration.reddit.subreddits
        logger.info("Start up new bot main loop.")

        while (True):
            try:
                for subreddit in subreddits:
                    scrape_state = self._load_scrape_state()
                    records = self._load_records()

                    subreddit_timer = TimeDelta()
                    new_comments = self.get_latest_comments(subreddit, scrape_state, records)
                    comment_time = round(subreddit_timer.elapsed(), 2)
                    matches = self.get_matching_quotes(new_comments, records)
                    match_time = round(subreddit_timer.elapsed(), 2)

                    # TODO Score should be set via configuration.
                    replies = self.reply_to_comments(matches, 0.98, records)
                    reply_time = round(subreddit_timer.elapsed(), 2)
                    logger.info(
                        f"Subreddit {subreddit}: {len(new_comments)} comments in {comment_time}s, {len(matches)} matches in {match_time}s, {len(replies)} replies in {reply_time}s")
                    with DelayedKeyboardInterrupt():
                        self._save_records(records)
                        self._save_scrape_state(scrape_state)
            except KeyboardInterrupt:
                print()
                sys.exit()

    def _load_scrape_state(self) -> ScrapeState:
        if not self.ram_based_scrape_state:
            return self.scrape_state_loader["handler"](self.scrape_state_loader["filepath"])
        else:
            try:
                return self.scrape_state
            except AttributeError:
                self.scrape_state = ScrapeState()
                return self.scrape_state

    def _load_records(self) -> RecordKeeper:
        if not self.ram_based_records:
            return self.record_keeper_loader["handler"](self.record_keeper_loader["filepath"])
        else:
            try:
                return self.records
            except AttributeError:
                self.records = RecordKeeper()
                return self.records

    def _save_scrape_state(self, scrape_state: ScrapeState):
        if not self.ram_based_scrape_state:
            self.scrape_state_storer["handler"](self.scrape_state_storer["filepath"], scrape_state)

    def _save_records(self, records: RecordKeeper):
        if not self.ram_based_records:
            self.record_keeper_storer["handler"](self.record_keeper_storer["filepath"], records)
