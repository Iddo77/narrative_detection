class Narrative:
    def __init__(self, narrative_id: int, description: str):
        self.narrative_id = narrative_id
        self.description = description
        self.search_term = None
        self.video_ids = set()

    def add_video(self, video_id: str):
        self.video_ids.add(video_id)

    def __repr__(self):
        return (f"Narrative(description='{self.description}', "
                f"search_term='{self.search_term}', "
                f"videos={len(self.video_ids)})")
