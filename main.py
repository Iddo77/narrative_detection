import os
from datetime import datetime

from content_manager import ContentManager
from marvin_ai import extract_narratives
from utils import write_to_file, read_from_file
from yt_searcher import search_videos


def main():
    start_date_ = datetime(2023, 10, 7)
    content_manager = ContentManager()

    json_path = './data/content.json'
    if os.path.exists(json_path):
        content_json = read_from_file(json_path)
        content_manager.deserialize(content_json)

    videos = search_videos('Palestine', start_date_, max_results=3)  # TODO move searching and getting transcripts and narratives to separate function
    for v in videos:
        if not content_manager.contains_video(v):
            v.fetch_transcript()
            if v.transcript:  # skip videos without transcript
                content_manager.add_video(v)
                for narrative_description in extract_narratives(v.transcript):
                    content_manager.create_video_narrative(v.video_id, narrative_description)

    # Update transcripts for all videos in the store
    # video_store.update_transcripts()

    # serialize
    content_json = content_manager.serialize()
    write_to_file(json_path, content_json)


if __name__ == '__main__':
    main()

