from io import TextIOWrapper
from types import SimpleNamespace
from typing import Optional
import json


class Configuration():
    """Provides access to possible configuration options.
    """

    def __init__(self):
        self.reddit = SimpleNamespace(
            subreddits=[
                "test"
            ]
        )

    def to_dict(self) -> dict:
        """Get the configuration as a dictionary"""
        return {
            "reddit": {
                "subreddits": self.reddit.subreddits,
            }
        }


class ConfigurationLoader():
    """Provides static methods for loading configuration from various sources.
    """
    @staticmethod
    def from_json(file_handler: TextIOWrapper) -> Configuration:
        """Load configuration from a JSON file

        Args:
            file_handler (TextIOWrapper): Open file handler for the target configuration file.

        Raises:
            KeyError: The configuration file doesn't contain expected keys, try regenerating.

        Returns:
            Configuration: Loaded configuration
        """
        loaded = json.load(file_handler)
        config = Configuration()
        try:
            config.reddit.subreddits = loaded["reddit"]["subreddits"]
        except KeyError as exp:
            raise KeyError("Cannot load given configuration.") from exp
        return config


class ConfigurationGenerator():
    """Provides static methods for generating configuration file templates
    """
    @staticmethod
    def to_json(file_handler: TextIOWrapper, configuration: Optional[Configuration] = None):
        """Save configuration to JSON

        Args:
            file_handler (TextIOWrapper): Open write enabled file handler
            configuration (Optional[Configuration], optional): Configuration to save, if not supplied default configuration is generated. Defaults to None.
        """
        if not configuration:
            configuration = Configuration()
        json.dump(configuration.to_dict(), file_handler, indent=2)
