from io import TextIOWrapper
from types import SimpleNamespace
from typing import Optional
import json


class CredentialStore():
    """Source of private credentials used throughout the application
    """

    def __init__(self):
        self.reddit = SimpleNamespace(
            user_agent="",
            client_id="",
            client_secret="",
            username="",
            password="",
        )

    def to_dict(self) -> dict:
        """Get the credentials as a dictionary"""
        return {
            "reddit": {
                "user_agent": self.reddit.user_agent,
                "client_id": self.reddit.client_id,
                "client_secret": self.reddit.client_secret,
                "username": self.reddit.username,
                "password": self.reddit.password
            }
        }


class CredentialLoader():
    """Provides static methods for loading credentials from external sources
    """
    @staticmethod
    def from_json(file_handler: TextIOWrapper) -> CredentialStore:
        """Load credentials from a json file.

        Args:
            file_handler (str): Open file handler

        Raises:
            KeyError: The given credentials file doesn't contain expected keys. Consider regeneration.
            FileNotFoundError: The given filename cannot be found

        Returns:
            CredentialStore: Credential store object populated from JSON values
        """
        data = json.load(file_handler)
        store = CredentialStore()
        try:
            store.reddit.user_agent = data["reddit"]["user_agent"]
            store.reddit.client_id = data["reddit"]["client_id"]
            store.reddit.client_secret = data["reddit"]["client_secret"]
            store.reddit.username = data["reddit"]["username"]
            store.reddit.password = data["reddit"]["password"]
        except KeyError as exp:
            raise KeyError("Correct keys not found in credentials file. Consider regeneration.") from exp
        return store


class CredentialGenerator():
    """Provides static methods for generating credential file templates
    """
    @staticmethod
    def to_json(file_handler: TextIOWrapper, credentials: Optional[CredentialStore] = None):
        if not credentials:
            credentials = CredentialStore()
        json.dump(credentials.to_dict(), file_handler, indent=2)
