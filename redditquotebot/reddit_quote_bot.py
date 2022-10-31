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

from redditquotebot.utilities import CredentialStore, Configuration


class RedditQuoteBot():
    """A reddit quote bot used for detecting and automatically replying to comments which closely match famous quotes.
    """

    def __init__(self):
        self.credentials = CredentialStore()
        self.configuration = Configuration()
