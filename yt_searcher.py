from duckduckgo_search import DDGS
from datetime import datetime
from dateutil import parser

from video import Video


def search_videos(search_term: str, start_date: datetime, max_results=300):
    """
    Generator function to search for videos based on a search term, starting from a specified date.
    Yields a dictionary of video information if the video is published by YouTube, has a description,
    and is published on or after the start date.

    Args:
    search_term (str): The search term to query for videos.
    start_date (datetime): The starting date to filter videos.
    max_results (int, optional): The maximum number of results to return. Defaults to 300.

    Yields:
    dict: A dictionary containing information about each video that meets the criteria.
    """
    with DDGS() as ddgs:
        ddgs_videos_gen = ddgs.videos(
            search_term,
            safesearch="off",
            duration="medium",  # exclude shorts; longer videos are rare anyway, so no problem they are excluded as well
            max_results=max_results,
        )
        for r in ddgs_videos_gen:
            published_date = parser.parse(r['published'])
            if published_date >= start_date and r['publisher'] == 'YouTube' and r['description']:
                yield Video.from_search_data(r)


if __name__ == '__main__':
    start_date_ = datetime(2023, 10, 7)
    videos = search_videos('Palestine', start_date_)
    for v in videos:
        print(v)
