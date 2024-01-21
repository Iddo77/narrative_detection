import os
import logging
from datetime import datetime

from content_manager import ContentManager
from marvin_ai import extract_narratives
from utils import write_to_file, read_from_file
from yt_searcher import search_videos


# Configure logging
logging.basicConfig(
    filename='./data/application.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    start_date_ = datetime(2023, 10, 7)
    content_manager = ContentManager()
    logging.info("ContentManager initialized")

    json_path = './data/content.json'
    if os.path.exists(json_path):
        content_json = read_from_file(json_path)
        content_manager.deserialize(content_json)

    search_and_process_videos(content_manager, 'Palestine', start_date_, max_results=100)

    # serialize
    content_json = content_manager.serialize()
    write_to_file(json_path, content_json)


def search_and_process_videos(content_manager: ContentManager,
                              search_term: str,
                              start_date: datetime,
                              max_results: int) -> None:
    videos = search_videos(search_term, start_date, max_results)
    for video in videos:
        if not content_manager.contains_video(video):
            process_video(content_manager, video)


def process_video(content_manager: ContentManager, video, max_retries=1, max_skips=3):
    """
    Processes a single video, extracting narratives and linking them to the video.
    """
    consecutive_skips = 0
    last_exception = None

    for _ in range(max_retries + 1):
        try:
            video.fetch_transcript()
            if not video.transcript:
                logging.info(f"Video {video.video_id} has no transcript and is skipped.")
                return

            content_manager.add_video(video)
            for narrative_description in extract_narratives(video.transcript):
                content_manager.create_video_narrative(video.video_id, narrative_description)

            consecutive_skips = 0
            break
        except Exception as e:
            consecutive_skips += 1
            last_exception = e
            logging.error(f"Error processing video {video.video_id}: {e}", exc_info=True)
            if consecutive_skips >= max_skips:
                logging.warning(f"Skipped video {video.video_id} after {consecutive_skips} failures: {last_exception}")
                raise last_exception


if __name__ == '__main__':
    main()

