from redditquotebot.utilities import Configuration, CredentialStore


class IReddit():
    def __init__(self, configuration: Configuration, credentials: CredentialStore):
        self.configuration = configuration
        self.credentials = credentials

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()
