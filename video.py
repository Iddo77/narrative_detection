from dateutil import parser
import re


class Video:
    def __init__(self):
        self.url = None
        self.video_id = None
        self.description = None
        self.duration = None
        self.published_date = None
        self.publisher = None
        self.statistics = None
        self.title = None
        self.uploader = None
        self.transcript = None

    @classmethod
    def from_search_data(cls, search_data):
        """
        Initialize a Video object from DuckDuckGo search data.

        Args:
        search_data (dict): A dictionary containing video search data.
        """
        video = cls()
        video.url = search_data.get('content')
        video.video_id = video.extract_youtube_id(video.url)
        video.description = search_data.get('description')
        video.duration = search_data.get('duration')
        video.published_date = parser.parse(search_data.get('published')).date() if search_data.get('published') else None
        video.publisher = search_data.get('publisher')
        video.statistics = search_data.get('statistics')
        video.title = search_data.get('title')
        video.uploader = search_data.get('uploader')
        return video

    @classmethod
    def from_json_data(cls, json_data):
        """
        Initialize a Video object from JSON data (deserialization).

        Args:
        json_data (dict): A dictionary containing video data in JSON format.
        """
        video = cls()
        video.__dict__.update(json_data)
        return video

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
