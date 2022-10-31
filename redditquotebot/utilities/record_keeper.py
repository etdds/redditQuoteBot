from io import TextIOWrapper
from typing import Optional, List, Union
from redditquotebot.reddit import Comment
import json


class RecordKeeper():
    """Contains information on the latest requests and comment dates
    """

    def __init__(self):
        self.records = {
            "comments": []
        }

    def to_dict(self) -> dict:
        """Get the records as a dictionary"""
        return {
            "records": self.records
        }

    def log_comments(self, comments: Union[List[Comment], Comment]):
        """Log comments to the record keeper

        Args:
            comments (Union[List[Comment], Comment]): _description_
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
            return self.records["comments"]
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
        state = RecordKeeper()
        try:
            state.records = data["records"]
        except KeyError as exp:
            raise KeyError("Correct keys not found in records file. Consider removing.") from exp
        return state


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
