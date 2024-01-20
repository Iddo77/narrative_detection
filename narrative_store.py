import json

from narrative import Narrative


class NarrativeStore:
    def __init__(self):
        self.narratives = set()

    def add_narrative(self, narrative: Narrative):
        self.narratives.add(narrative)

    def create_narrative(self, description: str):
        narrative_id = len(self.narratives) + 1
        narrative = Narrative(narrative_id, description)
        self.narratives.add(narrative)

    def serialize(self) -> str:
        """
        Serializes the narrative store to a JSON string.
        """
        narrative_data = [vars(narr) for narr in self.narratives]
        return json.dumps(narrative_data)

    def deserialize(self, json_string: str):
        """
        Deserializes a JSON string to populate the narrative store.
        """
        narrative_data = json.loads(json_string)
        for data in narrative_data:
            narr = Narrative(narrative_id=int(data['narrative_id']), description=data['description'])
            narr.__dict__.update(data)
            self.narratives.add(narr)

    def __repr__(self):
        return f"NarrativeStore with {len(self.narratives)} narratives"
