import os
import logging
from datetime import datetime

from content_manager import ContentManager
from marvin_ai import extract_narratives, create_search_term
from utils import write_to_file, read_from_file
from yt_searcher import search_videos


# Configure logging
logging.basicConfig(
    filename='./data/application.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class MaxSkipsReachedException(Exception):
    """Exception raised when the maximum number of consecutive skips is reached."""
    pass


def main():
    start_date = datetime(2023, 10, 7)
    content_manager = ContentManager()
    logging.info("ContentManager initialized")

    json_path = './data/content.json'
    if os.path.exists(json_path):
        content_json = read_from_file(json_path)
        content_manager.deserialize(content_json)

    narrative_count = len(content_manager.narratives)
    video_count = len(content_manager.videos)

    try:
        iterative_narrative_expansion(content_manager,
                                      "Palestine",
                                      start_date,
                                      max_iterations=3,
                                      max_total_videos=500)
    except Exception as e:
        logging.error(f"Searching and processing videos is interrupted: {e}", exc_info=True)

    # serialize
    if len(content_manager.narratives) != narrative_count or len(content_manager.videos) != video_count:
        content_json = content_manager.serialize()
        write_to_file(json_path, content_json)


def iterative_narrative_expansion(content_manager: ContentManager,
                                  initial_search_term: str,
                                  start_date: datetime,
                                  max_iterations: int,
                                  max_total_videos: int):
    """
    Iteratively expands the search for videos based on narratives using a BFS approach.
    Narratives are merged after completing each BFS level.

    Args:
    content_manager (ContentManager): The content manager instance.
    initial_search_term (str): The initial search term for videos.
    start_date (datetime): The starting date for video search.
    max_iterations (int): Maximum number of iterations for the BFS loop.
    max_total_videos (int): Maximum total number of videos to process.
    """
    iteration = 1
    search_queue = [(initial_search_term, max_iterations, True)]

    while search_queue and len(content_manager.videos) < max_total_videos:
        current_search_term, current_depth, merge_flag = search_queue.pop(0)

        # Calculate max_results based on the current depth
        max_results = 2 ** (current_depth + 2)  # 32, 16, 8 for 3 iterations

        search_and_process_videos(content_manager, current_search_term, start_date, iteration, max_results)

        # for the first iteration, the search term of the narratives to the initial search term
        if iteration == 1:
            for narrative in content_manager.narratives.values():
                if narrative.iteration == 1:
                    narrative.search_term = initial_search_term

        if merge_flag:
            new_narratives = content_manager.cluster_and_merge_narratives(iteration, iteration)
            iteration += 1
            if iteration > max_iterations:
                break

            for idx, narrative in enumerate(new_narratives):
                narrative.search_term = create_search_term(narrative.description)
                merge_flag = idx == len(new_narratives) - 1  # Set merge_flag to True for the last narrative
                search_queue.append((narrative.search_term, current_depth - 1, merge_flag))

    # do a final merge of all narratives except the first iteration
    content_manager.cluster_and_merge_narratives(2, iteration)


def search_and_process_videos(content_manager: ContentManager,
                              search_term: str,
                              start_date: datetime,
                              iteration: int,
                              max_results: int,
                              max_skips: int = 3) -> None:
    videos = search_videos(search_term, start_date, max_results)
    consecutive_skips = 0

    for video in videos:
        if not content_manager.contains_video(video):
            try:
                if process_video(content_manager, video, iteration):
                    consecutive_skips = 0  # Reset skip count on success
                # Else: video is skipped because transcript is missing -> consecutive_skips stays the same
            except Exception:
                consecutive_skips += 1  # Increment skip count on processing failure
                if consecutive_skips == max_skips:
                    raise MaxSkipsReachedException(f"{max_skips} consecutive videos are skipped due to errors. "
                                                   f"Stopping video processing.")


def process_video(content_manager: ContentManager, video, iteration, max_retries=1) -> bool:
    """
    Processes a single video, extracting narratives and linking them to the video.

    Returns:
    bool: True if the video was processed successfully, False otherwise.
    """
    for attempt in range(max_retries + 1):
        try:
            video.fetch_transcript()
            if not video.transcript:
                logging.info(f"Video {video.video_id} has no transcript and is skipped.")
                return False

            content_manager.add_video(video)
            for narrative_description in extract_narratives(video.transcript):
                content_manager.create_video_narrative(video.video_id, narrative_description, iteration)

            return True  # Successfully processed
        except Exception as e:
            if attempt == max_retries:
                logging.error(f"Error processing video {video.url}: {e}", exc_info=True)
                raise  # Reraise the exception after final attempt
    return False


if __name__ == '__main__':
    main()

