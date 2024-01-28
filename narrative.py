class Narrative:
    def __init__(self, narrative_id: int, description: str, iteration: int, search_term=None, based_on=None):
        self.narrative_id: int = narrative_id
        self.description: str = description
        self.search_term: str | None = search_term
        self.iteration = iteration
        self.based_on: list[int] = based_on if based_on else []

    def __repr__(self):
        return f"Narrative(description='{self.description}'"
