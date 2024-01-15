import json
from typing import Optional
from video import Video


class VideoStore:
    def __init__(self):
        self._videos: dict[str, Video] = {}

    def add_video(self, video: Video) -> bool:
        """
        Adds a unique video to the store.

        Args:
        video (Video): The video object to be added.

        Returns:
        bool: True if the video was added, False if it already exists.
        """
        if video.video_id not in self._videos:
            self._videos[video.video_id] = video
            return True
        return False

    def get_video(self, video_id: str) -> Optional[Video]:
        """
        Retrieves a video by its ID.

        Args:
        video_id (str): The ID of the video to retrieve.

        Returns:
        Optional[Video]: The video if found, None otherwise.
        """
        return self._videos.get(video_id)

    def remove_video(self, video_id: str) -> bool:
        """
        Removes a video by its ID.

        Args:
        video_id (str): The ID of the video to remove.

        Returns:
        bool: True if the video was removed, False if not found.
        """
        if video_id in self._videos:
            del self._videos[video_id]
            return True
        return False

    def update_transcripts(self):
        """
        Updates the transcripts for all videos in the store where it's None.
        """
        for video in self._videos.values():
            if video.transcript is None:
                video.fetch_transcript()

    def serialize(self) -> str:
        """
        Serializes the video store to a JSON string.

        Returns:
        str: JSON string representation of the video store.
        """
        return json.dumps({vid: vars(self._videos[vid]) for vid in self._videos}, default=str)

    def deserialize(self, json_string):
        """
        Deserializes a JSON string to populate the video store.

        Args:
        json_string (str): JSON string representation of the video store.
        """
        video_data = json.loads(json_string)
        for vid in video_data:
            video = Video.from_json_data(video_data[vid])
            self.add_video(video)

    def __repr__(self) -> str:
        return f"VideoStore with {len(self._videos)} videos"
