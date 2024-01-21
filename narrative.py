class Narrative:
    def __init__(self, narrative_id: int, description: str, search_term=None):
        self.narrative_id: int = narrative_id
        self.description: str = description
        self.search_term: str | None = search_term

    def __repr__(self):
        return f"Narrative(description='{self.description}'"
