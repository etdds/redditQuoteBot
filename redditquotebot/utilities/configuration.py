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
            ],
            new_submissions_per_request=10,
            max_comments_per_request=100,
            minimum_comment_length=15
        )
        self.bot = SimpleNamespace(
            reply_to_comments=False,
            matched_quotes_to_log=3,
            reply_threshold=0.99
        )
        self.nlp = SimpleNamespace(
            match_store_threshold=0.97,
            quote_comment_length_delta=0.7,
            minimum_comment_sentence_word_length=5,
            quote_length_bonus_coefficient=0.0008,
            quote_length_bonus_start=6,
            quote_length_bonus_end=10,
            matched_sentence_coefficient=0.5
        )

    def to_dict(self) -> dict:
        """Get the configuration as a dictionary"""
        return {
            "reddit": {
                "subreddits": self.reddit.subreddits,
                "new_submissions_per_request": self.reddit.new_submissions_per_request,
                "max_comments_per_request": self.reddit.max_comments_per_request,
                "minimum_comment_length": self.reddit.minimum_comment_length,
            },
            "bot": {
                "reply_to_comments": self.bot.reply_to_comments,
                "reply_threshold": self.bot.reply_threshold,
                "matched_quotes_to_log": self.bot.matched_quotes_to_log
            },
            "nlp": {
                "match_store_threshold": self.nlp.match_store_threshold,
                "quote_comment_length_delta": self.nlp.quote_comment_length_delta,
                "minimum_comment_sentence_word_length": self.nlp.minimum_comment_sentence_word_length,
                "quote_length_bonus_coefficient": self.nlp.quote_length_bonus_coefficient,
                "quote_length_bonus_start": self.nlp.quote_length_bonus_start,
                "quote_length_bonus_end": self.nlp.quote_length_bonus_end,
                "matched_sentence_coefficient": self.nlp.matched_sentence_coefficient
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
            config.reddit.new_submissions_per_request = loaded["reddit"]["new_submissions_per_request"]
            config.reddit.max_comments_per_request = loaded["reddit"]["max_comments_per_request"]
            config.reddit.minimum_comment_length = loaded["reddit"]["minimum_comment_length"]
            config.bot.reply_to_comments = loaded["bot"]["reply_to_comments"]
            config.bot.reply_threshold = loaded["bot"]["reply_threshold"]
            config.bot.matched_quotes_to_log = loaded["bot"]["matched_quotes_to_log"]
            config.nlp.match_store_threshold = loaded["nlp"]["match_store_threshold"]
            config.nlp.quote_comment_length_delta = loaded["nlp"]["quote_comment_length_delta"]
            config.nlp.minimum_comment_sentence_word_length = loaded["nlp"]["minimum_comment_sentence_word_length"]
            config.nlp.quote_length_bonus_coefficient = loaded["nlp"]["quote_length_bonus_coefficient"]
            config.nlp.quote_length_bonus_start = loaded["nlp"]["quote_length_bonus_start"]
            config.nlp.quote_length_bonus_end = loaded["nlp"]["quote_length_bonus_end"]
            config.nlp.matched_sentence_coefficient = loaded["nlp"]["matched_sentence_coefficient"]
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
