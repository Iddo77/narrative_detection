import os
from datetime import datetime

from utils import write_to_file, read_from_file
from video_store import VideoStore
from yt_searcher import search_videos


def main():
    start_date_ = datetime(2023, 10, 7)
    video_store = VideoStore()

    json_path = './data/videos.json'
    if os.path.exists(json_path):
        videos_json = read_from_file(json_path)
        video_store.deserialize(videos_json)

    videos = search_videos('Palestine', start_date_)
    for v in videos:
        video_store.add_video(v)

    # Update transcripts for all videos in the store
    video_store.update_transcripts()

    videos_json = video_store.serialize()
    write_to_file(json_path, videos_json)


if __name__ == '__main__':
    main()

