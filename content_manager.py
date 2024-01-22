import json
from datetime import date, datetime

from marvin_ai import merge_narratives
from narrative import Narrative
from narrative_clusterer import NarrativeClusterer
from video import Video


class ContentManager:
    def __init__(self):
        self.videos: dict[str, Video] = dict()
        self.narratives: dict[int, Narrative] = dict()
        self.video_to_narratives = {}  # Maps video IDs to sets of narrative IDs
        self.narrative_to_videos = {}  # Maps narrative IDs to sets of video IDs
        self.next_narrative_id = 1  # Auto-incrementing ID for Narratives
        self.narrative_clusterer = NarrativeClusterer()

    def add_video(self, video: Video) -> bool:
        if not self.contains_video(video):
            self.videos[video.video_id] = video
            return True
        return False

    def contains_video(self, video: Video) -> bool:
        return video.video_id in self.videos

    def create_video_narrative(self, video_id: str, narrative_description: str) -> Narrative:
        """
        Creates a Narrative object with a given description, assigns an ID to it, registers it in the
        NarrativeStore, and links it to the specified video.

        Args:
        video_id (str): The ID of the video to link the narrative to.
        narrative_description (str): The description of the narrative.

        Returns:
        Narrative: The created Narrative object.
        """
        # Create and set up the Narrative object
        narrative = Narrative(self.next_narrative_id, narrative_description)
        self.next_narrative_id += 1

        # Register the narrative and link it with the video
        self.narratives[narrative.narrative_id] = narrative
        self.link_video_narrative(video_id, narrative.narrative_id)

        return narrative

    def link_video_narrative(self, video_id: str, narrative_id: int):
        self.video_to_narratives[video_id] = narrative_id
        self.narrative_to_videos[narrative_id] = video_id

    def get_video(self, video_id: str) -> Video:
        return self.videos.get(video_id)

    def get_narrative(self, narrative_id: int) -> Narrative:
        return self.narratives.get(narrative_id)

    def get_videos_for_narrative(self, narrative_id: int):
        return [self.get_video(video_id) for video_id in self.narrative_to_videos.get(narrative_id, set())]

    def get_narratives_for_video(self, video_id: str):
        return [self.get_narrative(narrative_id) for narrative_id in self.video_to_narratives.get(video_id, set())]

    def remove_narrative(self, narrative_id: int):
        for video in self.get_videos_for_narrative(narrative_id):
            self.video_to_narratives[video.video_id].remove(narrative_id)
        del self.narratives[narrative_id]
        del self.narrative_to_videos[narrative_id]

    def cluster_and_merge_narratives(self):
        """
        Clusters and merges narratives using the NarrativeClusterer.
        """
        narratives = set(self.narratives.values())
        clusters = self.narrative_clusterer.cluster_narratives(narratives)

        # merge each cluster into a new narrative
        for cluster in clusters:
            # merge and create new narrative
            narrative_descriptions = [narr.description for narr in cluster]
            new_narrative_description = merge_narratives(narrative_descriptions)
            new_narrative = Narrative(self.next_narrative_id, new_narrative_description)
            self.next_narrative_id += 1
            # link new narrative and remove old narratives
            for narr in cluster:
                videos = self.get_videos_for_narrative(narr.narrative_id)
                for video in videos:
                    self.link_video_narrative(video.video_id, new_narrative.narrative_id)
                self.remove_narrative(narr.narrative_id)

    def serialize(self) -> str:
        """
        Serializes the content manager's state to a JSON string.
        """
        data = {
            "videos": {vid: self._convert_video_to_dict(video) for vid, video in self.videos.items()},
            "narratives": {nid: vars(narrative) for nid, narrative in self.narratives.items()},
            "video_to_narratives": self.video_to_narratives,
            "narrative_to_videos": self.narrative_to_videos,
            "next_narrative_id": self.next_narrative_id
        }
        return json.dumps(data, default=self._json_serialize)

    def deserialize(self, json_string: str):
        """
        Deserializes a JSON string to restore the content manager's state.
        """
        data = json.loads(json_string)

        # Reconstruct Video objects
        self.videos = {}
        for vid, v_data in data["videos"].items():
            video = Video()
            video.__dict__.update(v_data)
            if 'published_date' in v_data and v_data['published_date']:
                video.published_date = datetime.fromisoformat(v_data['published_date'])
            self.videos[vid] = video

        # Reconstruct Narrative objects
        self.narratives = {nid: Narrative(**n_data) for nid, n_data in data["narratives"].items()}

        # Restore relationships
        self.video_to_narratives = data["video_to_narratives"]
        self.narrative_to_videos = data["narrative_to_videos"]

        # Restore the next narrative ID
        self.next_narrative_id = data["next_narrative_id"]

    @staticmethod
    def _convert_video_to_dict(video: Video) -> dict:
        video_dict = vars(video)
        if video.published_date:
            video_dict['published_date'] = video.published_date.isoformat()
        return video_dict

    @staticmethod
    def _json_serialize(obj):
        """
        Custom JSON serializer for objects not serializable by default json code.
        """
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
