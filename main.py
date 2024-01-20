import os
from datetime import datetime

from marvin_ai import extract_narratives
from narrative_store import NarrativeStore
from utils import write_to_file, read_from_file
from video import Video
from video_store import VideoStore
from yt_searcher import search_videos


def main():
    start_date_ = datetime(2023, 10, 7)
    video_store = VideoStore()
    narrative_store = NarrativeStore()

    videos_json_path = './data/videos.json'
    if os.path.exists(videos_json_path):
        videos_json = read_from_file(videos_json_path)
        video_store.deserialize(videos_json)

    narratives_json_path = './data/narratives.json'
    if os.path.exists(narratives_json_path):
        narratives_json = read_from_file(narratives_json_path)
        narrative_store.deserialize(narratives_json)

    videos = search_videos('Palestine', start_date_)  # TODO move searching and getting transcripts and narratives to separate function
    for v in videos:
        if not video_store.get_video(v.video_id):  # TODO make this line more readable
            v.fetch_transcript()
            for narrative_description in extract_narratives(v.transcript):
                narrative = narrative_store.create_narrative(narrative_description)
                narrative.add_video(v.video_id)
                v.narratives.add(narrative)
            video_store.add_video(v)

    # Update transcripts for all videos in the store
    # video_store.update_transcripts()

    # serialize
    videos_json = video_store.serialize()
    write_to_file(videos_json_path, videos_json)
    narratives_json = narrative_store.serialize()
    write_to_file(narratives_json_path, narratives_json)


if __name__ == '__main__':
    main()

