class Tweet:
    def __init__(self):
        self.image_filepath = ''
        self.tweet_text = ''

    def attach_image(self, fpath: str):
        """Attach an image to the tweet"""
        self.image_filepath = fpath

    def attach_text(self, tweet_text: str):
        self.tweet_text = tweet_text