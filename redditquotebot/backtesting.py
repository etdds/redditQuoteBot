from redditquotebot.utilities import RecordKeeper, RecordLoader, RecordStorer
from redditquotebot.reddit import Comment, Reply, CommentUIDFilter
from redditquotebot.nlp import MatchedQuote, QuoteNLPDetector, QuoteCommentNLPMatcher
from redditquotebot.quotes import Quote
from typing import List, Union, Type


def combine_records(records: List[RecordKeeper]) -> RecordKeeper:
    """Combine multiple records together into a single record, skipping duplicates.

    Args:
        records (List[RecordKeeper]): A list of records to combine.

    Returns:
        RecordKeeper: The records combined into a single entity.
    """
    full_records = RecordKeeper()
    for record in records:
        full_comments = full_records.logged_comments()
        full_matches = full_records.logged_matches()
        full_replies = full_records.logged_replies()
        comments = record.logged_comments()
        for comment in comments:
            if comment not in full_comments:
                full_records.log_comments(comment)
        matches = record.logged_matches()
        for match in matches:
            if match.comment not in [m.comment for m in full_matches]:
                full_records.log_matched_quote(match)
        replies = record.logged_replies()
        for reply in replies:
            if reply.comment not in [r.comment for r in full_replies]:
                full_records.log_reply(reply)
    return full_records


class Backtester():
    """A utility class used for backtesting quote to comment matches.
    """

    def __init__(self, quotes: List[Quote], detector: Type[QuoteNLPDetector]):
        self.detector = detector(quotes)
        self._matcher = QuoteCommentNLPMatcher(0, 0)
        self._threshold = 0.5
        self._store_count = 1

    def _worker(self, comments: List[Comment]):
        self.detector.apply(self._matcher, self._threshold, comments)
        all_matches = []
        for comment in comments:
            matches = self.detector.get_matches(comment, self._store_count)
            if len(matches):
                all_matches.append(matches)
        return all_matches

    def get_matches(self, comments: List[Comment]) -> List[List[MatchedQuote]]:
        """Get quote matches for a list of comments.

        Args:
            comments (List[Comment]): The list of comments to process

        Returns:
            List[List[MatchedQuote]]: A nested list of matches.
        """
        return self._worker(comments)

    def set_parameters(self, matcher: QuoteCommentNLPMatcher, threshold: float, store_count: int):
        """Set the parameters used for get_matches

        Args:
            matcher (QuoteCommentNLPMatcher): The quote comment matcher to use
            threshold (float): The threshold to use for accepting that a quote matches a comment
            store_count (int): The number of matches to store for a single comment.
        """
        self._matcher = matcher
        self._store_count = store_count
        self._threshold = threshold
