class Tweet:
    def __init__(self):
        self.image_filepath = None
        self.tweet_text = None

    def attach_image(self, fpath: str):
        """Attach an image to the tweet"""
        self.image_filepath = fpath

    def attach_text(self, tweet_text: str):
        self.tweet_text = tweet_text