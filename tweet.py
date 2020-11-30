class Tweet:
    def __init__(self):
        self.image_filepath = ''
        self.tweet_text = ''

    def attach_image(self, fpath: str):
        """Attach an image to the tweet"""
        self.image_filepath = fpath

    def attach_text(self, tweet_text: str):
        self.tweet_text = tweet_text

    def __repr__(self):
        tweet_str = self.tweet_text if self.tweet_text != "" else "N/A"
        img_str = self.image_filepath if self.image_filepath != "" else "N/A"

        output_str = "Tweet\n-----\n"
        output_str += f"{tweet_str}"
        output_str += "\n-----\nPhoto\n-----\n"
        output_str += f"{img_str}"
        return output_str