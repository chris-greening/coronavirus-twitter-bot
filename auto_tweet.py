class AutoTweet:
    @classmethod
    def connect_to_api(cls, api):
        """Connect AutoTweetTask to Twitter API"""
        cls.api = api