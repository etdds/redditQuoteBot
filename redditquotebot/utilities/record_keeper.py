from io import TextIOWrapper
from typing import Optional, List, Union
from redditquotebot.reddit import Comment, Reply
from redditquotebot.nlp import MatchedQuote
from collections import deque
import json


class RecordKeeper():
    """Contains information on the latest comments, matches and replies.
    """

    def __init__(self):
        self._maximum_comments = None
        self._maximum_matches = None
        self._maximum_replies = None
        self._maximum_removed = None
        self.records = {
            "comments": deque(maxlen=self._maximum_comments),
            "matches": deque(maxlen=self._maximum_matches),
            "replies": deque(maxlen=self._maximum_replies),
            "removed": deque(maxlen=self._maximum_removed),
            "banned_subreddits": []
        }

    def maximum_comments(self, count: Union[None, int]) -> None:
        """Set the maximum amount of comments which can exist in a record.

        Oldest comments are discarded.

        Args:
            count (Union[None, int]): maximum count
        """
        self._maximum_comments = count
        new_comments = deque(self.records["comments"], maxlen=count)
        self.records["comments"] = new_comments

    def maximum_matches(self, count: Union[None, int]) -> None:
        """Set the maximum amount of matches which can exist in a record.

        Oldest matches are discarded.

        Args:
            count (Union[None, int]): maximum count
        """
        self._maximum_matches = count
        new_matches = deque(self.records["matches"], maxlen=count)
        self.records["matches"] = new_matches

    def maximum_replies(self, count: Union[None, int]) -> None:
        """Set the maximum amount of replies which can exist in a record.

        Oldest replies are discarded.

        Args:
            count (Union[None, int]): maximum count
        """
        self._maximum_replies = count
        new_replies = deque(self.records["replies"], maxlen=count)
        self.records["replies"] = new_replies

    def maximum_removed_comments(self, count: Union[None, int]) -> None:
        """Set the maximum amount of removed comments which can exist in a record.

        Oldest removed comments recorded are discarded.

        Args:
            count (Union[None, int]): maximum count
        """
        self._maximum_removed = count
        new_removals = deque(self.records["removed"], maxlen=count)
        self.records["removed"] = new_removals

    def banned_subreddits(self) -> List[str]:
        """Get the list of currently banned subreddits.

        Returns:
            List[str]: List of subreddits banned
        """
        return self.records["banned_subreddits"]

    def add_banned_subreddit(self, subreddit: str) -> None:
        """Add a subreddit to the list of banned subreddits.

        Args:
            subreddit (str): The subreddit to add. Duplicates are ignored.
        """
        if subreddit not in self.records["banned_subreddits"]:
            self.records["banned_subreddits"].append(subreddit)

    def to_dict(self) -> dict:
        """Get the records as a dictionary"""
        d = {
            "records": {
                "comments": list(self.records["comments"]),
                "matches": list(self.records["matches"]),
                "replies": list(self.records["replies"]),
                "removed": list(self.records["removed"]),
                "banned_subreddits": self.records["banned_subreddits"]
            }
        }
        return d

    def log_comments(self, comments: Union[List[Comment], Comment]):
        """Log comments to the record keeper

        Args:
            comments (Union[List[Comment], Comment]): Either a list of comments or a comment.
        """
        if isinstance(comments, Comment):
            comments = [comments.to_dict()]
        else:
            comments = [c.to_dict() for c in comments]
        try:
            self.records["comments"] += comments
        except KeyError:
            self.records["comments"] = comments

    def logged_comments(self) -> List[Comment]:
        """Get all comments currently logged

        Returns:
            List[Comment]: All logged comments
        """
        try:
            return [Comment().from_dict(d) for d in self.records["comments"]]
        except KeyError:
            return []

    def log_matched_quote(self, match: Union[List[MatchedQuote], MatchedQuote]):
        """Log matched quotes to the record keeper

        Args:
            matches (Union[List[MatchedQuote], MatchedQuote]): Either a list of matches, or a single match
        """
        if isinstance(match, MatchedQuote):
            match = [match.to_dict()]
        else:
            match = [m.to_dict() for m in match]
        try:
            self.records["matches"] += match
        except KeyError:
            self.records["matches"] = match

    def logged_matches(self) -> List[MatchedQuote]:
        """Get all matches currently logged

        Returns:
            List[MatchedQuote]: All logged matches
        """
        try:
            return [MatchedQuote.from_dict(r) for r in self.records["matches"]]
        except KeyError:
            return []

    def log_reply(self, reply: Union[List[Reply], Reply]):
        """Log reply to the record keeper

        Args:
            reply (Union[List[Reply], Reply]): Either a list of replies, or a single reply
        """
        if isinstance(reply, Reply):
            reply = [reply.to_dict()]
        else:
            reply = [r.to_dict() for r in reply]
        try:
            self.records["replies"] += reply
        except KeyError:
            self.records["replies"] = reply

    def logged_replies(self) -> List[Reply]:
        """Get all replies currently logged

        Returns:
            List[Reply]: All logged replies
        """
        try:
            return [Reply.from_dict(r) for r in self.records["replies"]]
        except KeyError:
            return []

    def log_removed_comment(self, comments: Union[List[Comment], Comment]):
        """Log a removed comment to the record keeper.

        Args:
            comment (Union[List[Comment], Comment]): Either a list or single removed comment
        """
        if isinstance(comments, Comment):
            comments = [comments.to_dict()]
        else:
            comments = [c.to_dict() for c in comments]
        try:
            self.records["removed"] += comments
        except KeyError:
            self.records["removed"] = comments

    def logged_removed_comments(self) -> List[Comment]:
        """Get all comments currently removed.

        Returns:
            List[Comment]: All logged comment removals
        """
        try:
            return [Comment.from_dict(c) for c in self.records["removed"]]
        except KeyError:
            return []


class RecordLoader():
    """Provides static methods for loading records from an external source
    """
    @staticmethod
    def from_json(file_handler: TextIOWrapper) -> RecordKeeper:
        """Load records from a json file.

        Args:
            file_handler (str): Open file handler

        Raises:
            KeyError: The given records file doesn't contain expected keys. Consider removing.
            FileNotFoundError: The given filename cannot be found

        Returns:
            RecordKeeper: instance of records
        """
        data = json.load(file_handler)
        records = RecordKeeper()
        try:
            records.log_comments([Comment.from_dict(c) for c in data["records"]["comments"]])
            records.log_matched_quote([MatchedQuote.from_dict(m) for m in data["records"]["matches"]])
            records.log_reply([Reply.from_dict(r) for r in data["records"]["replies"]])
        except KeyError as exp:
            raise KeyError("Correct keys not found in records file. Consider removing.") from exp
        try:
            for sub in data["records"]["banned_subreddits"]:
                records.add_banned_subreddit(sub)
        except KeyError as exp:
            pass

        try:
            records.log_removed_comment([Comment.from_dict(c) for c in data["records"]["removed"]])
        except KeyError as exp:
            pass
        return records


class RecordStorer():
    """Provides static methods for generating and storing records to external sources
    """
    @staticmethod
    def to_json(file_handler: TextIOWrapper, records: Optional[RecordKeeper] = None):
        if isinstance(records, tuple):
            if len(records) != 0:
                records = records[0]
            else:
                records = None

        if not records:
            records = RecordKeeper()
        json.dump(records.to_dict(), file_handler, indent=2)
