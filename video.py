from dateutil import parser
import re


class Video:
    def __init__(self, video_data):
        """
        Initialize the Video object with video data.

        Args:
        video_data (dict): A dictionary containing video information.
        """
        self.url = video_data.get('content')
        self.video_id = self.extract_youtube_id(self.url)
        self.description = video_data.get('description')
        self.duration = video_data.get('duration')
        self.published_date = parser.parse(video_data.get('published')).date()
        self.publisher = video_data.get('publisher')
        self.statistics = video_data.get('statistics')
        self.title = video_data.get('title')
        self.uploader = video_data.get('uploader')
        self.transcript = None

    @staticmethod
    def extract_youtube_id(url):
        """
        Extracts the YouTube video ID from the URL if it's a YouTube URL.
        Returns the original URL otherwise.

        Args:
        url (str): The video URL.

        Returns:
        str: The YouTube video ID or the original URL.
        """
        if 'youtube' in url or 'youtu.be' in url:
            match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11})', url)
            return match.group(1) if match else url
        return url

    def __repr__(self):
        return f"Video(title='{self.title}', uploader='{self.uploader}', published_date='{self.published_date}')"
