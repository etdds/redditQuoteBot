from io import TextIOWrapper
from typing import Optional
import json


class ScrapeState():
    """Contains information on the latest requests and comment dates
    """

    def __init__(self):
        self.latest_comments = {}

    def update_latest_subreddit_utc(self, subreddit: str, utc: int):
        try:
            if self.latest_comments[subreddit] < utc:
                self.latest_comments[subreddit] = utc
        except KeyError:
            self.latest_comments[subreddit] = utc

    def latest_subreddit_utc(self, subreddit: str):
        try:
            return self.latest_comments[subreddit]
        except KeyError:
            return 0

    def to_dict(self) -> dict:
        """Get the scrape state as a dictionary"""
        return {
            "latest_comments": self.latest_comments
        }


class ScrapeStateLoader():
    """Provides static methods for loading the scrape state from external sources
    """
    @staticmethod
    def from_json(file_handler: TextIOWrapper) -> ScrapeState:
        """Load srape state from a json file.

        Args:
            file_handler (str): Open file handler

        Raises:
            KeyError: The given state file doesn't contain expected keys. Consider removing.
            FileNotFoundError: The given filename cannot be found

        Returns:
            ScrapeState: Scrape state object populated from JSON values
        """
        data = json.load(file_handler)
        state = ScrapeState()
        try:
            state.latest_comments = data["latest_comments"]
        except KeyError as exp:
            raise KeyError("Correct keys not found in state file. Consider removing.") from exp
        return state


class ScrapeStateStorer():
    """Provides static methods for generating and saving scrape state file templates
    """
    @staticmethod
    def to_json(file_handler: TextIOWrapper, scrape_state: Optional[ScrapeState] = None):
        if isinstance(scrape_state, tuple):
            if len(scrape_state) != 0:
                scrape_state = scrape_state[0]
            else:
                scrape_state = None

        if not scrape_state:
            scrape_state = ScrapeState()
        json.dump(scrape_state.to_dict(), file_handler, indent=2)
