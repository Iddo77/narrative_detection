import re
from datetime import date

from dateutil import parser
from youtube_transcript_api import YouTubeTranscriptApi


class Video:
    def __init__(self):
        self.url: str | None = None
        self.video_id: str | None = None
        self.description: str | None = None
        self.duration: str | None = None
        self.published_date: date | None = None
        self.publisher: str | None = None
        self.statistics: dict | None = None
        self.title: str | None = None
        self.uploader: str | None = None
        self.transcript: str | None = None

    @classmethod
    def from_search_data(cls, search_data: dict) -> 'Video':
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
    def from_json_data(cls, json_data: dict) -> 'Video':
        """
        Initialize a Video object from JSON data (deserialization).

        Args:
        json_data (dict): A dictionary containing video data in JSON format.
        """
        video = cls()
        video.__dict__.update(json_data)
        return video

    @staticmethod
    def is_youtube_video(url: str) -> bool:
        """
        Checks if the given URL is a YouTube video URL.

        Args:
        url (str): The video URL.

        Returns:
        bool: True if the URL is a YouTube URL, False otherwise.
        """
        return 'youtube' in url or 'youtu.be' in url

    @staticmethod
    def extract_youtube_id(url: str) -> str:
        """
        Extracts the YouTube video ID from the URL if it's a YouTube URL.
        Returns the original URL otherwise.

        Args:
        url (str): The video URL.

        Returns:
        str: The YouTube video ID or the original URL.
        """
        if Video.is_youtube_video(url):
            match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11})', url)
            return match.group(1) if match else url
        return url

    def fetch_transcript(self) -> None:
        """
        Fetches the transcript for the video and updates the transcript attribute.
        If fetching fails, sets the transcript to an empty string.
        """
        if self.is_youtube_video(self.url):
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(self.video_id)
                self.transcript = ' '.join([entry['text'] for entry in transcript_list])
            except Exception:
                self.transcript = ""
        else:
            self.transcript = ""

    def __repr__(self) -> str:
        return f"Video(title='{self.title}', uploader='{self.uploader}', published_date='{self.published_date}')"
